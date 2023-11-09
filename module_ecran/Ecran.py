# **************************************************************#
#                                                              #
#        Python Robot - mdaadoun & aderouba - 2023             #
#                                                              #
# **************************************************************#

import pygame as pg
from .Interface import Interface
from .Visuel import Visuel
import time
import sys
from .data import STATUS

class Ecran:
    def __init__(self, robot, debug=False):
        """
        This method define all variables needed by the program
        """
        self.debug = debug

        # Start of pygame
        pg.init()
        pg.freetype.init()

        self.robot = robot

        # We create the window
        if self.debug:
            self.surface = pg.display.set_mode((800, 600))
        else:
            self.surface = pg.display.set_mode((0, 0), pg.FULLSCREEN)

        # We create the interface
        self.ui = Interface(self, debug)
        self.visuel = Visuel(robot, self, debug)
        self.update_render = True
        self.clock = pg.time.Clock()  # The clock be used to limit our fps
        self.fps = 30
        self.last = time.time()
        self.runMainLoop = True

        self.current_status = STATUS["MENU"]

    def run(self):
        """
        This method is the main loop of the game
        """
        # Game loop
        while self.runMainLoop:
            self.input()
            self.tick()
            self.render()
        self.clock.tick(self.fps)

    def getWidth(self):
        return self.surface.get_width()

    def getHeight(self):
        return self.surface.get_height()

    def getDeltaTime(self):
        return self.clock.tick(self.fps) / 1000.0

    def getStatus(self):
        return self.current_status
    
    def setStatus(self, status):
        self.current_status = status

    def stop(self):
        self.runMainLoop = False

    def input(self):
        """
        The method catch user's inputs, as key presse or a mouse click
        """
        # We check each event
        for event in pg.event.get():
            # If the event it a click on the top right cross, we quit the game
            if event.type == pg.QUIT:
                self.quit()
            self.ui.check_event(event)

        self.keyboardState = pg.key.get_pressed()
        self.mouseState = pg.mouse.get_pressed()
        self.mousePos = pg.mouse.get_pos()

        # Press espace to quit
        if self.keyboardState[pg.K_ESCAPE]:
            self.quit()

    def tick(self):
        """
        This is the method where all calculations will be done
        """
        tmp = time.time()
        delta = str(round(tmp - self.last, 4))
        delta_time = str(round(self.getDeltaTime(), 4))
        fps = str(round(self.clock.get_fps(), 4))
        self.last = tmp

        if self.debug:
            pg.display.set_caption(
                f"fps: {fps} - delta: {delta} - delta_time: {delta_time}")

    def render(self):
        """
        This is the method where all graphic update will be done
        """
        # We clean our screen with one color
        self.surface.fill((0, 0, 0))
        self.ui.draw()
        self.update_render = False
        # We update the drawing.
        # Before the function call, any changes will be not visible
        pg.display.update()

    def quit(self):
        """
        This is the quit method
        """
        self.stop()
        # Pygame quit
        pg.quit()
        sys.exit()
