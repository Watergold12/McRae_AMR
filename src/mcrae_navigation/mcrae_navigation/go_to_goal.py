import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from tf_transformations import euler_from_quaternion

import math


class GoToGoal(Node):

    def __init__(self):
        super().__init__('go_to_goal')

        # Current robot position
        self.x = 0.0
        self.y = 0.0

        # Current robot orientation
        self.yaw = 0.0

        # Goal position
        self.goal_x = 2.0
        self.goal_y = 2.0

        # Subscribe to odometry
        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/diff_drive_controller/odom',
            self.odom_callback,
            10
        )

        # Publish velocity commands
        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Run navigation logic at 10 Hz
        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        self.get_logger().info(
            f'Goal set to ({self.goal_x}, {self.goal_y})'
        )


    def odom_callback(self, msg):

        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        
        orientation = msg.pose.pose.orientation

        quaternion = [
            orientation.x,
            orientation.y,
            orientation.z,
            orientation.w
        ]

        roll, pitch, yaw = euler_from_quaternion(quaternion)

        self.yaw = yaw


    def control_loop(self):

        # Distance to goal
        dx = self.goal_x - self.x
        dy = self.goal_y - self.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )
        
        goal_angle = math.atan2(dy, dx)
        
        heading_error = goal_angle - self.yaw

        heading_error = math.atan2(
            math.sin(heading_error),
            math.cos(heading_error)
        )

        goal_angle_degrees = math.degrees(goal_angle)
        current_yaw_degrees = math.degrees(self.yaw)
        heading_error_degrees = math.degrees(heading_error)

        self.get_logger().info(
            f'Position: ({self.x:.2f}, {self.y:.2f}) '
            f'Distance: {distance:.2f} '
            f'Goal angle: {goal_angle_degrees:.2f}° '
            f'Current yaw: {current_yaw_degrees:.2f}° '
            f'Heading error: {heading_error_degrees:.2f}° '
        )


def main(args=None):

    rclpy.init(args=args)

    node = GoToGoal()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
