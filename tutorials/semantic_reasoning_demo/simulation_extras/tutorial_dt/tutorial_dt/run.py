import time
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from std_srvs.srv import Trigger
from pyrobosim_msgs.srv import RequestWorldState
from pyrobosim_msgs.msg import WorldState
import json

class Dimensions:
    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height

class TutorialDigitalTwin(Node):
    def __init__(self):
        super().__init__('tutorial_digital_twin')

        # TODO, make it avail from yaml file or pyrobosim api
        self._dimensions_map = {
            'table':    Dimensions(width=1.20, length=0.80, height=0.50),
            'storage':  Dimensions(width=1.00, length=0.60, height=0.50),
            'snacks':   Dimensions(width=0.12, length=0.15, height=0.05),
            'soda':     Dimensions(width=0.12, length=0.15, height=0.05),
            'butter':   Dimensions(width=0.10, length=0.15, height=0.05),
            'robot':    Dimensions(width=0.10, length=0.10, height=0.10),
        }
        # Create callback groups for server and client
        self._get_data_service_cb_group   = MutuallyExclusiveCallbackGroup()
        self._world_state_client_cb_group = MutuallyExclusiveCallbackGroup()

        # Create the /dt/get_data service
        self._get_data_srv = self.create_service(
            Trigger,
            '/dt/get_data',
            self._get_data_callback,
            callback_group=self._get_data_service_cb_group
        )

        # Create a client for the /request_world_state service
        self._world_state_client = self.create_client(
            RequestWorldState,
            '/request_world_state',
            callback_group=self._world_state_client_cb_group
        )

        # Wait for the /request_world_state service to be available
        while not self._world_state_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /request_world_state service...')

    def _serialize_world_state(self, world_state: WorldState) -> str:
        """
        Serialize the locations and objects information from a WorldState message into JSON format.

        Args:
            world_state (WorldState): The WorldState message to serialize.

        Returns:
            str: The JSON string containing the serialized locations and objects information.
        """
        # Create a list to hold the flattened data
        flattened_data = []

        # Serialize locations
        for location in world_state.locations:
            dimens_info = self._dimensions_map[location.category]
            flattened_location = {
                'dt_id': location.name,
                'position': [
                    round(location.pose.position.x, 3),
                    round(location.pose.position.y, 3),
                    round(location.pose.position.z, 3)
                ],
                'orientation': [
                    round(location.pose.orientation.x, 3),
                    round(location.pose.orientation.y, 3),
                    round(location.pose.orientation.z, 3),
                    round(location.pose.orientation.w, 3)
                ],
                'bounding_box': {
                    'width' : dimens_info.width,
                    'length': dimens_info.length,
                    'height': dimens_info.height
                },
            }
            flattened_data.append(flattened_location)

        # Serialize objects
        for obj in world_state.objects:
            dimens_info = self._dimensions_map[obj.category]
            flattened_object = {
                'dt_id': obj.name,
#                'type': obj.category,
                'position': [
                    round(obj.pose.position.x, 3),
                    round(obj.pose.position.y, 3),
                    round(obj.pose.position.z, 3)
                ],
                'orientation': [
                    round(obj.pose.orientation.x, 3),
                    round(obj.pose.orientation.y, 3),
                    round(obj.pose.orientation.z, 3),
                    round(obj.pose.orientation.w, 3)
                ],
                'bounding_box': {
                    'width' : dimens_info.width,
                    'length': dimens_info.length,
                    'height': dimens_info.height
                },
            }
            flattened_data.append(flattened_object)

        # Serialize agents
        for robot in world_state.robots:
            dimens_info = self._dimensions_map[robot.name]
            flattened_robot = {
                'dt_id': robot.name,
                'position': [
                    round(robot.pose.position.x, 3),
                    round(robot.pose.position.y, 3),
                    round(robot.pose.position.z, 3)
                ],
                'orientation': [
                    round(robot.pose.orientation.x, 3),
                    round(robot.pose.orientation.y, 3),
                    round(robot.pose.orientation.z, 3),
                    round(robot.pose.orientation.w, 3)
                ],
                'bounding_box': {
                    'width' : dimens_info.width,
                    'length': dimens_info.length,
                    'height': dimens_info.height
                },
            }
            flattened_data.append(flattened_robot)

        # Convert the list to a JSON string
        json_str = json.dumps(flattened_data, indent=2)

        return json_str

    def _get_data_callback(self, request, response):

        # Call the /request_world_state service synchronously
        req = RequestWorldState.Request()
        res = self._world_state_client.call(req)

        # Serialize the world state data to JSON
        json_data = self._serialize_world_state(res.state)

        # Set the response
        response.success = True
        response.message = json_data

        return response

def main(args=None):
    rclpy.init(args=args)

    # Create an instance of the TutorialDigitalTwin node
    node = TutorialDigitalTwin()

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
