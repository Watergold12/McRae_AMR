class MotionController:

    def __init__(self):
        self.forward_speed = 0.2
        self.rotation_speed = 0.5

    def rotate_left(self):
        return 0.0, self.rotation_speed

    def rotate_right(self):
        return 0.0, -self.rotation_speed

    def move_forward(self):
        return self.forward_speed, 0.0

    def stop(self):
        return 0.0, 0.0


if __name__ == "__main__":

    controller = MotionController()

    print("Rotate left:", controller.rotate_left())
    print("Rotate right:", controller.rotate_right())
    print("Move forward:", controller.move_forward())
    print("Stop:", controller.stop())