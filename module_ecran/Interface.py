# **************************************************************#
#                                                              #
#              Python Robot - mdaadoun - 2023                  #
#                                                              #
# **************************************************************#

import pygame as pg
import pygame_gui as pgui
import os
from .data import STATUS

class Interface:
    def __init__(self, window, debug=False):
        self.debug = debug
        self.window = window
        self.manager_main = pgui.UIManager(
            (window.getWidth(), window.getHeight()), os.getcwd() + '/assets/theme.json')
        
        self.manager_display = pgui.UIManager(
            (window.getWidth(), window.getHeight()), os.getcwd() + '/assets/theme.json')
        
        self.button = {}
        self.load_buttons()

    def draw(self):
        self.manager_main.update(self.window.getDeltaTime())
        self.manager_main.draw_ui(self.window.surface)
        if self.window.getStatus() == STATUS['MENU']:
                print("menu drawing")
        elif self.window.getStatus() == STATUS['AUDIO']:
                print("audio drawing")
        elif self.window.getStatus() == STATUS['MICRO']:
                print("micro drawing")
        elif self.window.getStatus() == STATUS['CAMERA']:
                print("camera drawing")
        elif self.window.getStatus() == STATUS['DISPLAY']:
                print("display drawing")

    def load_buttons(self):
        self.button["face_button"] = pgui.elements.UIButton(
            relative_rect=pg.Rect(
                (self.window.getWidth() / 2 - 75, self.window.getHeight() - 60), (150, 50)),
            text='Face',
            manager=self.manager_display
        )
        self.button["speaker_button"] = pgui.elements.UIButton(
            relative_rect=pg.Rect((10, 10), (150, 50)),
            text='SPEAKER',
            manager=self.manager_main
        )
        self.button["microphone_button"] = pgui.elements.UIButton(
            relative_rect=pg.Rect((160, 10), (200, 50)),
            text='MICROPHONE',
            manager=self.manager_main
        )
        self.button["camera_button"] = pgui.elements.UIButton(
            relative_rect=pg.Rect((360, 10), (150, 50)),
            text='CAMERA',
            manager=self.manager_main
        )
        self.button["display_button"] = pgui.elements.UIButton(
            relative_rect=pg.Rect((510, 10), (150, 50)),
            text='DISPLAY',
            manager=self.manager_main
        )

    def check_event(self, event):
        if event.type == pg.USEREVENT:
            if event.user_type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button["face_button"]:
                    print("clicked_button_face, change face")
                if event.ui_element == self.button["speaker_button"]:
                    self.window.setStatus(STATUS['AUDIO'])
                if event.ui_element == self.button["microphone_button"]:
                    self.window.setStatus(STATUS['MICRO'])
                if event.ui_element == self.button["camera_button"]:
                    self.window.setStatus(STATUS['CAMERA'])
                if event.ui_element == self.button["display_button"]:
                    self.window.setStatus(STATUS['DISPLAY'])
        self.manager_main.process_events(event)
