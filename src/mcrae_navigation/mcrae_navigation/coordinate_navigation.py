import math


class CoordinateNavigation:

    def __init__(self, goal_x, goal_y):

        self.goal_x = goal_x
        self.goal_y = goal_y

        # How close we need to be before considering
        # the goal reached.
        self.goal_tolerance = 0.10

        # How accurately we need to face the goal
        # before moving forward.
        self.angle_tolerance = math.radians(5.0)

    def decide(self, current_x, current_y, current_yaw):

        # Difference between current position and goal
        dx = self.goal_x - current_x
        dy = self.goal_y - current_y

        # Distance to goal
        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        # Goal direction
        goal_angle = math.atan2(dy, dx)

        # Difference between where we need to face
        # and where the robot is currently facing
        heading_error = goal_angle - current_yaw

        # Normalize heading error to [-pi, +pi]
        heading_error = math.atan2(
            math.sin(heading_error),
            math.cos(heading_error)
        )

        # First decision: have we reached the goal?
        if distance <= self.goal_tolerance:
            return "STOP", distance, goal_angle, heading_error

        # Second decision: are we facing the goal?
        if abs(heading_error) > self.angle_tolerance:

            if heading_error > 0:
                return "ROTATE_LEFT", distance, goal_angle, heading_error

            else:
                return "ROTATE_RIGHT", distance, goal_angle, heading_error

        # We are facing the goal, so move forward
        return "MOVE_FORWARD", distance, goal_angle, heading_error
    

if __name__ == "__main__":

    navigation = CoordinateNavigation(
        goal_x=2.0,
        goal_y=2.0
    )

    decision, distance, goal_angle, heading_error = navigation.decide(
        current_x=0.0,
        current_y=0.0,
        current_yaw=math.radians(45)
    )

    print("Decision:", decision)
    print("Distance:", distance)
    print("Goal angle:", math.degrees(goal_angle))
    print("Heading error:", math.degrees(heading_error))