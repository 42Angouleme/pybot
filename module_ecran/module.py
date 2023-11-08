# **************************************************************#
#                                                              #
#              Python Robot - mdaadoun - 2023                  #
#                                                              #
# **************************************************************#

import pygame as pg
import pygame_gui as pgui

import os
import sys
from .Ecran import Ecran

img = {}
robot_face = "emoji_ok"


# **************************************************************#
#                  MAIN SETUP FUNCTIONS                        #
# **************************************************************#

# def set_window():
#     global window, WIDTH, HEIGHT
#     # window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
#     pg.display.init()
#     window = pg.display.set_mode((0, 0))
#     WIDTH = window.get_width()
#     HEIGHT = window.get_height()

# def set_ui():
#     global manager
#     # pg.font.Font( None, self.text_size )
#     pg.freetype.init()
#     manager = pgui.UIManager((WIDTH, HEIGHT), os.getcwd() + '/assets/theme.json')

def load_images():
    img["emoji_ok"] = pg.image.load(os.getcwd() + "/assets/emoji_ok.png")
    img["emoji_nok"] = pg.image.load(os.getcwd() + "/assets/emoji_nok.png")


# **************************************************************#
#                     DRAWING FUNCTIONS                        #
# **************************************************************#

# def draw_screen():
#     global update_drawing
#     draw_face()
#     # draw_ui()
#     update_drawing = False

# def draw_ui():
#     global b0_button

#     b0_button = pgui.elements.UIButton(
#         relative_rect=pg.Rect((350, 275), (150, 50)),
#         text='Face',
#         manager=manager
#     )
#     b1_button = pgui.elements.UIButton(
#         relative_rect=pg.Rect((10, 10), (150, 50)),
#         text='BUTTON 1',
#         manager=manager
#     )
#     b2_button = pgui.elements.UIButton(
#         relative_rect=pg.Rect((200, 10), (150, 50)),
#         text='BUTTON 2',
#         manager=manager
#     )

def draw_face():
    offset_x = img[robot_face].get_size()[0] / 2
    offset_y = img[robot_face].get_size()[1] / 2
    window.blit(img[robot_face], (WIDTH/2 - offset_x, HEIGHT/2 - offset_y))
    pg.display.flip()
    print("face", robot_face)


# **************************************************************#
#                  EVENTS & INPUTS CONTROL                     #
# **************************************************************#

def switch_face():
    global robot_face, update_drawing
    if robot_face == "emoji_ok":
        robot_face = "emoji_nok"
    else:
        robot_face = "emoji_ok"
    print("switch", robot_face)
    update_drawing = True


def check_events():
    global robot_running

    for event in pg.event.get():
        if event.type == pg.QUIT:
            robot_running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                robot_running = False
            if event.key == pg.K_SPACE:
                switch_face()
        if event.type == pg.USEREVENT:
            if event.user_type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == b0_button:
                    switch_face()
        manager.process_events(event)


# **************************************************************#
#                         MAIN LOOP                            #
# **************************************************************#

# def main_loop():
#     global robot_running, update_drawing
#     clock = pg.time.Clock()
#     robot_running = True
#     update_drawing = True
#     while robot_running:
#         time_delta = clock.tick(30)/1000.0
#         check_events()
#         if update_drawing:
#             window.fill((0,0,0))
#             draw_screen()
#             manager.update(time_delta)
#             manager.draw_ui(window)
#             pg.display.update()
#     pg.quit()
#     sys.exit()


# **************************************************************#
#                          START                               #
# **************************************************************#

def run(robot):
    win = Ecran(robot, True)
    win.run()
    # set_window()
    # set_ui()
    # load_images()
    # main_loop()
