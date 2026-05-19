import threading
import time
import random
import json
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.parameter import Parameter
from rclpy.action.server import ServerGoalHandle, GoalStatus
from overarching_msgs.action import Navigate, Detect, Pick, Place
from pyrobosim_msgs.msg import TaskAction, ExecutionResult
from pyrobosim_msgs.action import ExecuteTaskAction
from pyrobosim_msgs.srv import SetLocationState
from pyrobosim_msgs.srv import RequestWorldState
from std_srvs.srv import SetBool, Trigger
from std_msgs.msg import String, Float32

class SkillExecutor(Node):
    def __init__(self):
        super().__init__('tutorial_robot_action_server')

        # Initialize the boolean parameters
        self._place_should_bump = False
        self._navigation_should_fail = False

        # Initialize the last action performed
        self._last_action = 'IDLE'

        # Initialize the pick status flag
        self._pick_performed = False

        # Keep track of last executed place action
        self._last_place_action = None

        # Initialize the last published force effort z value
        self._last_force_effort_z = random.uniform(0.4, 0.6)

        # Create callback groups for the action/service servers and clients
        self._servers_cb_group = MutuallyExclusiveCallbackGroup()
        self._action_cb_group = MutuallyExclusiveCallbackGroup()
        self._service_cb_group = MutuallyExclusiveCallbackGroup()

        # Create the /robot/exec_action_name publisher
        self._exec_action_name_pub = self.create_publisher(
            String,
            '/robot/exec_action_name',
            10
        )

        # Create the /robot/force_effort_z publisher
        self._force_effort_z_pub = self.create_publisher(
            Float32,
            '/robot/force_effort_z',
            10
        )

        # Publish 'IDLE' at initialization
        self._publish_exec_action_name('IDLE')

        # Publish the initial random value on topic /robot/force_effort_z at initialization
        self._publish_force_effort_z(self._last_force_effort_z)

        # Create a timer to regularly broadcast the last published value on topic /robot/force_effort_z
        self._broadcast_timer = self.create_timer(1.0, self._broadcast_last_force_effort_z)

        # Create the /robot/executor/get_info service server
        self._get_info_srv = self.create_service(
            Trigger,
            '/robot/executor/get_info',
            self._get_info_callback,
            callback_group=self._servers_cb_group
        )

        # Create the /robot/navigate action server
        self._navigate_action_server = ActionServer(
            self,
            Navigate,
            '/robot/navigate',
            execute_callback=self._navigate_action_callback,
            cancel_callback=self._cancel_callback,
            callback_group=self._servers_cb_group
        )

        # Create the /robot/detect action server
        self._detect_action_server = ActionServer(
            self,
            Detect,
            '/robot/detect',
            execute_callback=self._detect_action_callback,
            cancel_callback=self._cancel_callback,
            callback_group=self._servers_cb_group
        )

        # Create the /robot/pick action server
        self._pick_action_server = ActionServer(
            self,
            Pick,
            '/robot/pick',
            execute_callback=self._pick_action_callback,
            cancel_callback=self._cancel_callback,
            callback_group=self._servers_cb_group
        )

        # Create the /robot/place action server
        self._place_action_server = ActionServer(
            self,
            Place,
            '/robot/place',
            execute_callback=self._place_action_callback,
            cancel_callback=self._cancel_callback,
            callback_group=self._servers_cb_group
        )

        # Create the /robot/inject/spurious_navigation_bug service server
        self._spurious_navigation_bug_srv = self.create_service(
            SetBool,
            '/robot/inject/spurious_navigation_bug',
            self._spurious_navigation_bug_callback,
            callback_group=self._servers_cb_group
        )

        # Create a client for the /set_location_state service
        self._set_location_state_client = self.create_client(
            SetLocationState,
            '/set_location_state',
            callback_group=self._service_cb_group
        )

        # Wait for the /set_location_state service to be available
        while not self._set_location_state_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info('Waiting for /set_location_state service...')

        # Create the /execute_action action client
        self._execute_action_client = ActionClient(
            self,
            ExecuteTaskAction,
            '/execute_action',
            callback_group=self._action_cb_group
        )

        # Wait for the /execute_action action server to be available
        while not self._execute_action_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().info('Waiting for /execute_action action server...')

        # Create the /request_world_state service client
        self._world_state_client = self.create_client(
            RequestWorldState,
            '/request_world_state',
            callback_group=self._service_cb_group
        )

        # Wait for the /request_world_state service server to be available
        while not self._world_state_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info('Waiting for /request_world_state service server...')

    def _publish_exec_action_name(self, action_name):
        """Publish the current action name to the /robot/exec_action_name topic."""
        msg = String()
        msg.data = action_name
        self._exec_action_name_pub.publish(msg)

        # Update the last action performed
        self._last_action = action_name

    def _publish_force_effort_z(self, value, duration_sec=0.0):
        """Publish the force effort z value to the /robot/force_effort_z topic for the specified duration."""
        msg = Float32()
        msg.data = value
        start_time = time.time()

        if duration_sec > 0.0:
            while time.time() - start_time < duration_sec:
                self._force_effort_z_pub.publish(msg)
                time.sleep(0.01)  # Small sleep to prevent high CPU usage
        else:
            self._force_effort_z_pub.publish(msg)

        # Update the last published force effort z value
        self._last_force_effort_z = value

    def _broadcast_last_force_effort_z(self):
        """Broadcast the last published value on the /robot/force_effort_z topic."""
        # Generate a new random value based on the pick status
        if self._pick_performed:
            random_value = random.uniform(2.4, 2.6)
        else:
            random_value = random.uniform(0.4, 0.6)

        # Publish the new random value
        self._publish_force_effort_z(random_value)

    def _execute_task_async(self, task_action):
        """Send a task goal to the action server asynchronously."""
        if not self._execute_action_client.server_is_ready():
            # Wait for action server
            if not self._execute_action_client.wait_for_server(timeout_sec=2.0):
                self.get_logger().warn('Action server /execute_action not available (yet).')
            else:
                return None

        if not self._execute_action_client.server_is_ready():
            self.get_logger().error('Action server /execute_action is not ready')
            return None

        goal_msg = ExecuteTaskAction.Goal()
        goal_msg.action = task_action  # task_action should be a TaskAction message

        self.get_logger().info(f'\nSending goal: {goal_msg}')
        future = self._execute_action_client.send_goal_async(goal_msg)
        return future

    def _execute_task_sync(self, task_action, cancel_event: threading.Event, timeout_sec=2.0):
        """Send a task goal and wait for completion synchronously."""

        goal_future = self._execute_task_async(task_action)
        if goal_future is None:
            return False, 'Action server not ready'

        # Wait for goal acceptance
        start_time = time.time()
        while not goal_future.done() and (time.time() - start_time) < timeout_sec:
            time.sleep(0.01)

        if not goal_future.done():
            return False, 'Goal acceptance timeout'

        goal_handle: ClientGoalHandle = goal_future.result()
        if not goal_handle.accepted:
            return False, 'Goal was rejected'

        self.get_logger().info('Goal accepted, waiting for result...')

        # Wait for result
        result_future = goal_handle.get_result_async()
        start_time = time.time()
        while not result_future.done() and not cancel_event.is_set():
            time.sleep(0.01)

        if result_future.done():
            result_response = result_future.result()
            status = result_response.status
            actual_result: ExecuteTaskAction.Result = result_response.result
            success = status == GoalStatus.STATUS_SUCCEEDED and actual_result.execution_result.status == ExecutionResult.SUCCESS
            return success, actual_result.execution_result.message
        elif cancel_event.is_set():
            # self.get_logger().info(f"Cancelling action {task_action}")
            goal_handle.cancel_goal()
            return False, 'Cancelled'
        else:
            return False, 'Result timeout'

    def _process_execute_task_action(self, goal_handle: ServerGoalHandle, task_action: TaskAction, result):
        # if self._curr_robot_status and self._curr_robot_status.executing_action:
        #     time.sleep(0.5)

        self._cancel_event = threading.Event()
        self._processed_task_sync_event = threading.Event()
        success, message = self._execute_task_sync(task_action, cancel_event=self._cancel_event)
        self.get_logger().debug(f"Task action execution completed: success={success}, message='{message}'")
        self._processed_task_sync_event.set()

        if goal_handle.is_active:
            goal_handle.succeed() if success else goal_handle.abort()

        # Publish 'IDLE' once again as soon as the action server callback is exited
        self._publish_exec_action_name('IDLE')

        return result

    def _get_world_state(self):
        req = RequestWorldState.Request()
        future = self._world_state_client.call_async(req)

        done_event = threading.Event()

        def cb(_):
            done_event.set()

        future.add_done_callback(cb)
        done_event.wait()

        return future.result()

    def _cancel_callback(self, goal_handle: ServerGoalHandle):
        if goal_handle.is_active:
            self._cancel_event.set()
            self.get_logger().warn(f"Requested to cancel active action with goal id {goal_handle.goal_id} with request {goal_handle.request}")
            self._processed_task_sync_event.wait()
            self.get_logger().warn(f"Cancelled active action with goal id {goal_handle.goal_id} with request {goal_handle.request}")
            return CancelResponse.ACCEPT
        return CancelResponse.REJECT

    def _get_info_callback(self, request, response):
        """Serialize the info regarding the last executed place action."""
        info = []

        if self._last_place_action is not None:
            place_info = {
                "dt_id": f"place{self._last_place_action['id']}",
                "place_def": {
                    "param": {
                        "who"  : "robot",
                        "what" : self._last_place_action['object_id'],
                        "where": self._last_place_action['location_id']
                    },
                    "result": "success" if self._last_place_action['success'] else "failure"
                }
            }
            info.append(place_info)

        response.message = json.dumps(info, indent=2)
        response.success = True

        return response

    def _spurious_navigation_bug_callback(self, request, response):
        # Set the place_should_bump and navigation_should_fail parameters to true
        self._place_should_bump = request.data
        self._navigation_should_fail = request.data

        action = "injected" if request.data else "removed"

        # Set the response
        response.success = True
        response.message = f"Successfully {action} spurious navigation bug"

        return response

    def _navigate_action_callback(self, goal_handle: ServerGoalHandle):
        request: Navigate.Goal = goal_handle.request

        # Publish the current action name
        self._publish_exec_action_name('NAVIGATE')

        # Create TaskAction message properly
        task_action = TaskAction()
        task_action.robot = 'robot'
        task_action.type = 'navigate'
        task_action.target_location = request.location_id if not self._navigation_should_fail else request.location_id + '_left'

        return self._process_execute_task_action(goal_handle, task_action, Navigate.Result())

    def _detect_action_callback(self, goal_handle):
        request: Detect.Goal = goal_handle.request

        # Publish the current action name
        self._publish_exec_action_name('DETECT')

        # Create TaskAction message properly
        task_action = TaskAction()
        task_action.robot = 'robot'
        task_action.type = 'detect'

        return self._process_execute_task_action(goal_handle, task_action, Detect.Result())

    def _pick_action_callback(self, goal_handle):
        request: Pick.Goal = goal_handle.request

        # Publish the current action name
        self._publish_exec_action_name('PICK')

        mapping = {
            0: "soda0",
            1: "butter0",
            2: "snacks0"
        }

        obj = mapping.get(goal_handle.request.object_id)

        if obj is None:
            self.get_logger().error(
                f"Invalid object_id: {goal_handle.request.object_id}"
            )
            goal_handle.abort()
            return result

        # Create TaskAction message properly
        task_action = TaskAction()
        task_action.robot = 'robot'
        task_action.type = 'pick'
        task_action.object = obj

        result = self._process_execute_task_action(goal_handle, task_action, Pick.Result())

        # Set the pick status flag to True
        self._pick_performed = True

        # Generate a random value between 2.4 and 2.6 and publish it on topic /robot/force_effort_z
        random_value = random.uniform(2.4, 2.6)
        self._publish_force_effort_z(random_value)

        return result

    def _place_action_callback(self, goal_handle):
        request: Place.Goal = goal_handle.request
        result: Place.Result = Place.Result()

        # Publish the current action name
        self._publish_exec_action_name('PLACE')

        # Get world state
        world_state = self._get_world_state()
        if world_state is None:
            goal_handle.abort()
            return result
        robot_state = world_state.state.robots[0]
        object_id = robot_state.manipulated_object
        location_id = 'fridge' if 'fridge' in robot_state.last_visited_location else robot_state.last_visited_location

        succ = True
        if self._place_should_bump:
            # Cancel the broadcast timer
            self._broadcast_timer.cancel()

            # Publish a random value between 4.9 and 5.1 on topic /robot/force_effort_z for a duration of 300ms
            random_value_1 = random.uniform(4.9, 5.1)
            self._publish_force_effort_z(random_value_1, 0.3)

            # Publish a random value between 2.4 and 2.6 on topic /robot/force_effort_z for a duration of 100ms
            random_value_2 = random.uniform(2.4, 2.6)
            self._publish_force_effort_z(random_value_2, 0.1)

            # Restart the broadcast timer
            self._broadcast_timer = self.create_timer(1.0, self._broadcast_last_force_effort_z)

            goal_handle.abort()
            succ = False
        else:
            # Create TaskAction message properly
            task_action = TaskAction()
            task_action.robot = 'robot'
            task_action.type = 'place'

            result = self._process_execute_task_action(goal_handle, task_action, Place.Result())

            # Set the pick status flag to False
            self._pick_performed = False

            # Generate a random value between 0.4 and 0.6 and publish it on topic /robot/force_effort_z
            random_value = random.uniform(0.4, 0.6)
            self._publish_force_effort_z(random_value)

        # Store the last executed place action
        self._last_place_action = {
            'id': '44',
            'object_id': object_id,
            'location_id': location_id,
            'success': succ
        }

        self.get_logger().info(
            f"Place --> object={object_id}, location={location_id}, success={succ}"
        )

        return result

def main(args=None):
    rclpy.init(args=args)

    # Create an instance of the SkillExecutor node
    node = SkillExecutor()

    # Use a MultiThreadedExecutor to handle the reentrant callback group
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        # Spin the node using the executor
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
