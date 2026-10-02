import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from mcrae_navigation.coordinate_navigation import CoordinateNavigation
from mcrae_navigation.motion_controller import MotionController


class NavigationNode(Node):

    def __init__(self):
        super().__init__('navigation_node')

        # Goal
        self.goal_x = 2.0
        self.goal_y = 2.0

        # Navigation logic
        self.navigation = CoordinateNavigation(
            goal_x=self.goal_x,
            goal_y=self.goal_y
        )

        # Movement logic
        self.motion = MotionController()

        # ROS publisher
        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # ROS subscriber
        self.odom_subscription = self.create_subscription(
            Odometry,
            '/diff_drive_controller/odom',
            self.odom_callback,
            10
        )

        self.get_logger().info(
            f'Navigation started. Goal: ({self.goal_x}, {self.goal_y})'
        )

    def odom_callback(self, msg):

        # -------------------------
        # 1. Get current position
        # -------------------------

        current_x = msg.pose.pose.position.x
        current_y = msg.pose.pose.position.y

        # -------------------------
        # 2. Get current orientation
        # -------------------------

        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        yaw = self.quaternion_to_yaw(qx, qy, qz, qw)

        # -------------------------
        # 3. Ask navigation logic
        # -------------------------

        decision, distance, goal_angle, heading_error = (
            self.navigation.decide(
                current_x,
                current_y,
                yaw
            )
        )

        # -------------------------
        # 4. Ask movement logic
        # -------------------------

        if decision == "ROTATE_LEFT":

            linear, angular = self.motion.rotate_left()

        elif decision == "ROTATE_RIGHT":

            linear, angular = self.motion.rotate_right()

        elif decision == "MOVE_FORWARD":

            linear, angular = self.motion.move_forward()

        else:

            linear, angular = self.motion.stop()

        # -------------------------
        # 5. Create velocity command
        # -------------------------

        cmd = Twist()

        cmd.linear.x = linear
        cmd.angular.z = angular

        # -------------------------
        # 6. Publish command
        # -------------------------

        self.cmd_vel_publisher.publish(cmd)

        # -------------------------
        # 7. Display information
        # -------------------------

        self.get_logger().info(
            f'Position: ({current_x:.2f}, {current_y:.2f}) | '
            f'Distance: {distance:.2f} | '
            f'Yaw: {math.degrees(yaw):.1f}° | '
            f'Error: {math.degrees(heading_error):.1f}° | '
            f'Decision: {decision}'
        )

    @staticmethod
    def quaternion_to_yaw(x, y, z, w):

        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)

        return math.atan2(siny_cosp, cosy_cosp)


def main(args=None):

    rclpy.init(args=args)

    node = NavigationNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()