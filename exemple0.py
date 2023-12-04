#! venv/bin/python3

from pybot import Robot
robot = Robot()


def main():
    # robot.configurer()
    robot.allumer_ecran()
    # robot.allumer_camera()


if __name__ == "__main__":
    print("=" * 12)
    print("Robot Python")
    print("=" * 12)
    main()
