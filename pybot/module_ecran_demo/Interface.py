import pygame as pg
import pygame_gui as pgui
import os
import time


class Interface:
    def __init__(self, robot, window, debug=False):
        self.debug = debug
        self.window = window
        self.manager_main = pgui.UIManager(
            (window.getWidth(), window.getHeight()), os.getcwd() + '/pybot/assets/theme.json')
        self.robot = robot
        self.button = {}
        self.textbox = {}
        self.buttons = {}
        self.total_width = 0
        self.button_line = 0

    def draw(self):
        self.manager_main.update(self.window.getDeltaTime())
        self.manager_main.draw_ui(self.window.surface)

    def add_button(self, titre, function):
        self.buttons[titre] = function
        button_width = len(titre) * 18
        if self.total_width + button_width > self.window.getWidth():
            self.button_line += 1
            self.total_width = 0
        self.button[titre] = pgui.elements.UIButton(
            relative_rect=pg.Rect(
                (self.total_width, 50 * self.button_line), (button_width, 50)),
            text=titre,
            manager=self.manager_main
        )
        self.total_width += button_width

    def delete_button(self, titre):
        self.manager_main.clear_and_reset()
        self.total_width = 0
        self.button_line = 0
        del self.buttons[titre]
        for b in self.buttons:
            self.add_button(b, self.buttons[b])

    def check_event(self, event):

        if event.type == pg.USEREVENT:
            if event.user_type == pgui.UI_BUTTON_PRESSED:
                try:
                    for b in self.buttons:
                        if event.ui_element == self.button[b]:
                            self.buttons[b]()
                except:
                    pass
        self.manager_main.process_events(event)
