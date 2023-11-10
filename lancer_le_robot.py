#!/bin/python
from Robot import Robot
from module_webapp import create_app
import os
import threading

def run():
    debug = True
    webapp = create_app(root_dir=os.path.dirname(os.path.abspath(__file__)))
    robot = Robot(webapp, debug)
    threading.Thread(target=robot.demarrer()).start()
    webapp.run(debug)

if __name__ == "__main__":
    run()