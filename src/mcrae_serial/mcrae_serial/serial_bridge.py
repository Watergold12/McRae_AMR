import rclpy
from rclpy.node import Node


class SerialBridge(Node):

    def __init__(self):
        super().__init__('serial_bridge')
        self.get_logger().info('McRae Serial Bridge is alive!')


def main(args=None):
    rclpy.init(args=args)

    node = SerialBridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
