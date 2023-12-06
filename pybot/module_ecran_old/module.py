from .Ecran import Ecran

def run(robot, debug):
    win = Ecran(robot, debug)
    win.run()
