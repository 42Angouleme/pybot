import pygame as pg
# from .Interface import Interface
# from .Visuel import Visuel
# import time
# import sys


class Ecran:
    def __init__(self, robot, debug=False):
        self.debug = debug
        self.title = "Pybot"
        # main surface
        self.surface = None
        # objects
        self.robot = robot
        self.interface = None
        self.visuel = None
        # update flags
        self.toggle_in_fullscreen = False
        self.toggle_out_fullscreen = False
        self.change_title = False
        # theming colors data
        self.background_color = (0, 0, 0)
        # clock and fps
        self.clock = pg.time.Clock()
        self.fps = 30
        # self.last = time.time()
        # self.runMainLoop = True
        # self.cameraRunning = False
        # self.capturePhoto = False

    def run(self, width, height):
        pg.init()
        self.surface = pg.display.set_mode((width, height))
        pg.display.set_caption(self.title)
        # pg.freetype.init()
        # self.ui = Interface(self.robot, self)
        # self.visuel = Visuel(self.robot, self)
        return self

    # def loop(self):
    #     while self.runMainLoop:
    #         self.input()
    #         self.render()
    #         self.clock.tick(self.fps)

    def getWidth(self):
        return self.surface.get_width()

    def getHeight(self):
        return self.surface.get_height()

    # def getDeltaTime(self):
    #     return self.clock.tick(self.fps) / 1000.0

    # def getStatus(self):
    #     return self.current_status

    # def setStatus(self, status):
    #     self.current_status = status

    def stop(self):
        pg.quit()

    # def input(self):
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             self.quit()
    #         self.ui.check_event(event)

    #     self.keyboardState = pg.key.get_pressed()
    #     self.mouseState = pg.mouse.get_pressed()
    #     self.mousePos = pg.mouse.get_pos()

    #     if self.keyboardState[pg.K_ESCAPE]:
    #         self.quit()

    def update_fullscreen(self, change):
        if change:
            self.toggle_in_fullscreen = True
        else:
            self.toggle_out_fullscreen = True

    def update_title(self, title):
        self.title = title
        self.change_title = True

    def check_flags(self):
        if self.toggle_in_fullscreen:
            pg.display.set_mode((self.getWidth(), self.getHeight()), pg.FULLSCREEN | pg.SCALED)
            self.toggle_in_fullscreen = False
        elif self.toggle_out_fullscreen:
            pg.display.set_mode((self.getWidth(), self.getHeight()))
            self.toggle_out_fullscreen = False
        if self.change_title:
            pg.display.set_caption(self.title)

    def set_background_color(self, R, G, B):
        self.background_color = (R, G, B)

    def render(self):
        self.check_flags()
        self.surface.fill(self.background_color)
        # self.ui.draw()
        # self.visuel.afficher()
        pg.display.update()
        self.clock.tick(self.fps)

    # def quit(self):
    #     self.stop()
    #     # pg.quit()
    #     sys.exit()

    # def ajouter_bouton(self, titre, function):
    #     self.ui.add_button(titre, function)

    # def supprimer_bouton(self, titre):
    #     self.ui.delete_button(titre)

    # def afficher_camera(self):
    #     self.cameraRunning = True
    #     self.visuel.afficher_camera(self.ui)

    # def eteindre_camera(self):
    #     self.cameraRunning = False

    # def get_camera_running(self):
    #     return self.cameraRunning

    # def enregistrer_photo(self):
    #     self.capturePhoto = True

    # def check_capture(self):
    #     if self.capturePhoto:
    #         self.capturePhoto = False
    #         return True
    #     return False

    # def afficher_photo(self):
    #     self.visuel.set_visage(False)
    #     self.visuel.charger_photo()

    # def afficher_visage(self):
    #     self.visuel.set_visage(True)

    # def tourner_photo(self):
    #     self.visuel.tourner_photo()
