import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


class CommandSender(Node):

    def __init__(self):
        super().__init__('command_sender')

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_command
        )

    def publish_command(self):

        msg = Twist()

        msg.linear.x = 0.5
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.2

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Publishing: linear.x={msg.linear.x:.2f}, '
            f'angular.z={msg.angular.z:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = CommandSender()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()