from .Ecran import Ecran


def run(robot, width, height):
    win = Ecran(robot)
    return win.run(width, height)
