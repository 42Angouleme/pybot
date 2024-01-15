from .Fenetre import Fenetre


def run(robot, width, height):
    win = Fenetre(robot)
    return win.run(width, height)
