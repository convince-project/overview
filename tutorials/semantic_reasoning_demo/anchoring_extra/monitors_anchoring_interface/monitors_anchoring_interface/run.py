import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile

from std_msgs.msg import String
from anchoring_process_interfaces.action import UpdateState


class MonitorsAnchoringInterface(Node):

    def __init__(self):
        super().__init__('monitors_anchoring_interface')

        # --- Declare parameters ---
        self.declare_parameter('verdict_topics', rclpy.Parameter.Type.STRING_ARRAY)
        self.declare_parameter('anchoring_update_state_action', rclpy.Parameter.Type.STRING)

        # --- Get parameters ---
        self.verdict_topics = self.get_parameter('verdict_topics').value
        self.action_name = self.get_parameter('anchoring_update_state_action').value

        if not self.verdict_topics:
            self.get_logger().error("No verdict_topics provided")
            raise RuntimeError("Missing verdict_topics")

        if not self.action_name:
            self.get_logger().error("No anchoring_update_state_action provided")
            raise RuntimeError("Missing action name")

        # --- QoS ---
        qos = QoSProfile(depth=10)

        # --- Action client ---
        self.action_client = ActionClient(self, UpdateState, self.action_name)

        # --- State tracking ---
        self.previous_states = {}

        # --- Subscriptions ---
        self.subscribers = []
        for topic in self.verdict_topics:
            sub = self.create_subscription(
                String,
                topic,
                lambda msg, t=topic: self.verdict_callback(msg, t),
                qos
            )
            self.subscribers.append(sub)
            self.previous_states[topic] = None

            self.get_logger().info(f"Subscribed to {topic}")

    # -----------------------------------------
    # Callback
    # -----------------------------------------
    def verdict_callback(self, msg: String, topic: str):

        current_value = msg.data.strip().lower()

        if current_value not in ['currently_true', 'currently_false']:
            self.get_logger().warn(
                f"Unexpected value '{msg.data}' on {topic}")
            return

        prev = self.previous_states[topic]

        # --- Detect transition TRUE -> FALSE ---
        if prev == 'currently_true' and current_value == 'currently_false':
            self.get_logger().info(
                f"Transition TRUE->FALSE detected on {topic}")

            # Delay execution instead of immediate call
            self._schedule_double_call(topic)

        self.previous_states[topic] = current_value

    # -----------------------------------------
    # Delayed double call
    # -----------------------------------------
    def _schedule_double_call(self, topic: str):

        # First call after 0.5s
        timer1 = self.create_timer(
            0.5,
            lambda t=topic: self._first_call(t, timer1)
        )

    def _first_call(self, topic: str, timer1):
        timer1.cancel()

        self.get_logger().info(f"Delayed call 1 for {topic}")
        self.send_update_state_goal(topic)

        # Second call after another 0.5s
        timer2 = self.create_timer(
            0.5,
            lambda t=topic: self._second_call(t, timer2)
        )

    def _second_call(self, topic: str, timer2):
        timer2.cancel()

        self.get_logger().info(f"Delayed call 2 for {topic}")
        self.send_update_state_goal(topic)

    # -----------------------------------------
    # Action handling
    # -----------------------------------------
    def send_update_state_goal(self, topic: str):

        if not self.action_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error(
                f"Action server '{self.action_name}' not available")
            return

        goal_msg = UpdateState.Goal()
        goal_msg.knowledge_domain = 'SkrawlMoMa'

        future = self.action_client.send_goal_async(goal_msg)
        future.add_done_callback(self._goal_response_callback)

    def _goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().warn("Goal rejected")
            return

        self.get_logger().info("Goal accepted")

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._result_callback)

    def _result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f"Action result received: {result}")


def main(args=None):
    rclpy.init(args=args)
    node = MonitorsAnchoringInterface()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
