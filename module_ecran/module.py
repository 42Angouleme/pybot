# **************************************************************#
#                                                              #
#              Python Robot - mdaadoun - 2023                  #
#                                                              #
# **************************************************************#

import pygame
import pygame_gui as pgui

import os
import sys

img = {}
robot_face = "emoji_ok"

# **************************************************************#
#                  MAIN SETUP FUNCTIONS                        #
# **************************************************************#


def init_app():
    pygame.freetype.init()
    pygame.display.init()
    set_window()
    set_ui()


def set_window():
    global window, WIDTH, HEIGHT

    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH = window.get_width()
    HEIGHT = window.get_height()


def set_ui():
    global manager, b0_button
    manager = pgui.UIManager(
        (WIDTH, HEIGHT), os.getcwd() + '/assets/theme.json')

    b0_button = pgui.elements.UIButton(
        relative_rect=pygame.Rect((350, 275), (150, 50)),
        text='Face',
        manager=manager
    )
    b1_button = pgui.elements.UIButton(
        relative_rect=pygame.Rect((10, 10), (150, 50)),
        text='BUTTON 1',
        manager=manager
    )
    b2_button = pgui.elements.UIButton(
        relative_rect=pygame.Rect((200, 10), (150, 50)),
        text='BUTTON 2',
        manager=manager
    )


def load_images():
    img["emoji_ok"] = pygame.image.load(os.getcwd() + "/assets/emoji_ok.png")
    img["emoji_nok"] = pygame.image.load(os.getcwd() + "/assets/emoji_nok.png")


# **************************************************************#
#                     DRAWING FUNCTIONS                        #
# **************************************************************#

def draw_screen(td):
    global update_drawing
    window.fill((0, 40, 0))
    draw_face()
    update_drawing = False
    manager.update(td)
    manager.draw_ui(window)
    pygame.display.flip()


def draw_face():
    offset_x = img[robot_face].get_size()[0] / 2
    offset_y = img[robot_face].get_size()[1] / 2
    window.blit(img[robot_face], (WIDTH/2 - offset_x, HEIGHT/2 - offset_y))
    # pygame.display.update()
    # pygame.display.flip()
    # print("face", robot_face)


# **************************************************************#
#                  EVENTS & INPUTS CONTROL                     #
# **************************************************************#

def switch_face():
    global robot_face, update_drawing
    if robot_face == "emoji_ok":
        robot_face = "emoji_nok"
    else:
        robot_face = "emoji_ok"
    update_drawing = True


def check_events():
    global robot_running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            robot_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                robot_running = False
            if event.key == pygame.K_SPACE:
                switch_face()
        if event.type == pygame.USEREVENT:
            if event.user_type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == b0_button:
                    switch_face()
        manager.process_events(event)


# **************************************************************#
#                         MAIN LOOP                            #
# **************************************************************#

def main_loop():
    global robot_running, update_drawing
    clock = pygame.time.Clock()
    robot_running = True
    update_drawing = True
    while robot_running:
        time_delta = clock.tick(30) / 1000.0
        check_events()
        if update_drawing:
            draw_screen(time_delta)
    pygame.quit()
    sys.exit()


# **************************************************************#
#                          START                               #
# **************************************************************#

def run():
    init_app()
    load_images()
    main_loop()


if __name__ == "__main__":
    run()
