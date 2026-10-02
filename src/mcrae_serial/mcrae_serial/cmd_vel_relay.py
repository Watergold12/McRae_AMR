import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, TwistStamped


class CmdVelRelay(Node):

    def __init__(self):
        super().__init__('cmd_vel_relay')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        self.publisher = self.create_publisher(
            TwistStamped,
            '/diff_drive_controller/cmd_vel',
            10
        )

        self.get_logger().info(
            'Relaying /cmd_vel (Twist) -> '
            '/diff_drive_controller/cmd_vel (TwistStamped)'
        )

    def cmd_vel_callback(self, msg):

        stamped_msg = TwistStamped()

        stamped_msg.header.stamp = self.get_clock().now().to_msg()
        stamped_msg.header.frame_id = 'base_link'

        stamped_msg.twist = msg

        self.publisher.publish(stamped_msg)


def main(args=None):

    rclpy.init(args=args)

    node = CmdVelRelay()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
