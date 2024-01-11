
from .Interface import Interface
from ..module_camera.Camera import Camera
from .filtres import Filtres
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True' # need to be declared before to import pygame
import pygame as pg

class Ecran:
    def __init__(self, robot, debug=False):
        self.debug = debug
        self.title = "Pybot"
        self.is_fullscreen = False
        # main surface
        self.surface = None
        # objects
        self.robot = robot
        self.interface = None
        # update flags
        self.toggle_in_fullscreen = False
        self.toggle_out_fullscreen = False
        self.change_title = False
        # theming colors data
        self.background_color = (0, 0, 0)
        # clock and fps
        self.clock = pg.time.Clock()
        self.fps = 30
        # camera
        self.camera = None
        # filters
        self.filters = None

    def run(self, width, height):
        pg.init()
        self.surface = pg.display.set_mode((width, height))
        pg.display.set_caption(self.title)
        self.interface = Interface(self.surface)
        self.camera = Camera(self.surface)
        self.filters = Filtres()
        return self

    def getWidth(self):
        return self.surface.get_width()

    def getHeight(self):
        return self.surface.get_height()

    def change_background_color(self, R, G, B):
        self.background_color = (R, G, B)

    def stop(self):
        self.camera.stop()
        pg.quit()

    def update_fullscreen(self, change):
        if change == self.is_fullscreen:
            return
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
            self.is_fullscreen = True
        elif self.toggle_out_fullscreen:
            pg.display.set_mode((self.getWidth(), self.getHeight()))
            self.toggle_out_fullscreen = False
            self.is_fullscreen = False
        if self.change_title:
            pg.display.set_caption(self.title)

    def render(self):
        try:
            self.check_flags()
            self.clock.tick(self.fps)
            pg.display.update()
        except:
            pass

    def draw_background(self):
        self.surface.fill(self.background_color)
        pg.display.update()

    def draw_rect(self, w, h, x, y, c):
        rect = pg.Rect(x, y, w, h)
        pg.draw.rect(self.surface, c, rect)

    def draw_text(self, txt, x, y, s, c):
        font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", s)
        surf = font.render(txt, True, c)
        self.surface.blit(surf, (x, y))

    def create_button(self, w, h, x, y, c):
        return self.interface.create_button(w, h, x, y, c)

    def create_text_area(self, w, h, x, y, c):
        return self.interface.create_text_area(w, h, x, y, c)

    def display_camera(self, x, y):
        self.camera.display(x, y)
    
    def capture_photo(self, file_name):
        self.camera.capture(file_name)
    
    def display_image(self, file_path, x, y):
        try:
            img = pg.image.load(os.getcwd() + file_path)
            self.surface.blit(img, (x, y))
        except:
            pass

    def set_filter(self, file_path, filter_name):
        self.filters.apply(file_path, filter_name)
    
    def detect_card(self):
        return self.camera.detect_card()
