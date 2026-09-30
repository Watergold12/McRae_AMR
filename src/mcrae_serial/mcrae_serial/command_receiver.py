import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


class CommandReceiver(Node):

    def __init__(self):
        super().__init__('command_receiver')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.command_callback,
            10
        )

    def command_callback(self, msg):

        self.get_logger().info(
            f'Received: linear.x={msg.linear.x:.2f}, '
            f'angular.z={msg.angular.z:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = CommandReceiver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()