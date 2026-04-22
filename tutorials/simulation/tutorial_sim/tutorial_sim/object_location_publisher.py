import rclpy
from rclpy.node import Node

from pyrobosim_msgs.srv import RequestWorldState
from pyrobosim_msgs.msg import WorldState, RobotState, LocationState, HallwayState, ObjectState
from overarching_msgs.msg import Location


class ObjectLocationPublisher(Node):

    def __init__(self):
        super().__init__('service_client_publisher')

        self.client = self.create_client(RequestWorldState, 'request_world_state')

        # Wait for service to be available
        while not self.client.wait_for_service(timeout_sec=20.0):
            self.get_logger().info('Service not available, waiting...')

        self.publisher = self.create_publisher(Location, 'object_loc', 10)

        self.timer = self.create_timer(1.0, self.send_request)

        self.req = RequestWorldState.Request()

    def send_request(self):
        if not self.client.service_is_ready():
            self.get_logger().error('Service no longer available. Shutting down...')
            self.destroy_node()
            rclpy.shutdown()
            return

        future = self.client.call_async(self.req)
        future.add_done_callback(self.handle_response)

    def handle_response(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
            self.destroy_node()
            rclpy.shutdown()
            return

        objects = response.state.objects
        
        for obj in objects:
            if obj.name == "butter0":
                msg = Location()
                msg.x = obj.pose.position.x
                msg.y = obj.pose.position.y
                msg.parent = obj.parent

                self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = ObjectLocationPublisher()
    try:
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()
    except:
        pass

if __name__ == '__main__':
    main()