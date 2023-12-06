import pygame as pg
from .Interface import Interface
from .Visuel import Visuel
import time
import sys


class Ecran:
    def __init__(self, robot, debug=False):
        self.debug = debug
        pg.init()
        pg.freetype.init()
        self.robot = robot
        self.surface = None
        self.ui = None
        self.visuel = None
        self.clock = pg.time.Clock()
        self.fps = 30
        self.last = time.time()
        self.runMainLoop = True
        self.cameraRunning = False
        self.capturePhoto = False

    def run(self, width=400, height=300):
        self.surface = pg.display.set_mode((width, height))
        self.ui = Interface(self.robot, self)
        self.visuel = Visuel(self.robot, self)
        return self

    def loop(self):
        while self.runMainLoop:
            self.input()
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
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            self.ui.check_event(event)

        self.keyboardState = pg.key.get_pressed()
        self.mouseState = pg.mouse.get_pressed()
        self.mousePos = pg.mouse.get_pos()

        if self.keyboardState[pg.K_ESCAPE]:
            self.quit()

    def title(self, title):
        pg.display.set_caption(title)

    def render(self):
        self.surface.fill((0, 0, 0))
        self.ui.draw()
        self.visuel.afficher()
        pg.display.update()

    def quit(self):
        self.stop()
        # pg.quit()
        sys.exit()

    def ajouter_bouton(self, titre, function):
        self.ui.add_button(titre, function)

    def supprimer_bouton(self, titre):
        self.ui.delete_button(titre)

    def afficher_camera(self):
        self.cameraRunning = True
        self.visuel.afficher_camera(self.ui)

    def eteindre_camera(self):
        self.cameraRunning = False

    def get_camera_running(self):
        return self.cameraRunning

    def enregistrer_photo(self):
        self.capturePhoto = True

    def check_capture(self):
        if self.capturePhoto:
            self.capturePhoto = False
            return True
        return False

    def afficher_photo(self):
        self.visuel.set_visage(False)
        self.visuel.charger_photo()

    def afficher_visage(self):
        self.visuel.set_visage(True)

    def tourner_photo(self):
        self.visuel.tourner_photo()
