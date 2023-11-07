#**************************************************************#
#                                                              #
#              Python Robot - mdaadoun - 2023                  #
#                                                              #
#**************************************************************#

import pygame
import pygame_gui as pgui

import os, sys

img = {}
robot_face = "emoji_ok"

#**************************************************************#
#                  MAIN SETUP FUNCTIONS                        #
#**************************************************************#

def set_window():
    global window, WIDTH, HEIGHT
    # window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.init()
    window = pygame.display.set_mode((0, 0))
    WIDTH = window.get_width()
    HEIGHT = window.get_height()

def set_ui():
    global manager
    # pygame.font.Font( None, self.text_size )
    pygame.freetype.init()
    manager = pgui.UIManager((WIDTH, HEIGHT), os.getcwd() + '/assets/theme.json')

def load_images():
    img["emoji_ok"]  = pygame.image.load(os.getcwd() + "/assets/emoji_ok.png")
    img["emoji_nok"] = pygame.image.load(os.getcwd() + "/assets/emoji_nok.png")


#**************************************************************#
#                     DRAWING FUNCTIONS                        #
#**************************************************************#

def draw_screen():
    global update_drawing
    draw_face()
    draw_ui()
    update_drawing = False

def draw_ui():
    global b0_button

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

def draw_face():
    offset_x = img[robot_face].get_size()[0] / 2
    offset_y = img[robot_face].get_size()[1] / 2
    window.blit(img[robot_face], (WIDTH/2 - offset_x, HEIGHT/2 - offset_y))
    pygame.display.flip()
    print("face", robot_face)


#**************************************************************#
#                  EVENTS & INPUTS CONTROL                     #
#**************************************************************#

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

                
#**************************************************************#
#                         MAIN LOOP                            #
#**************************************************************#

def main_loop():
    global robot_running, update_drawing
    clock = pygame.time.Clock()
    robot_running = True
    update_drawing = True
    while robot_running:
        time_delta = clock.tick(30)/1000.0
        check_events()
        if update_drawing:
            window.fill((0,0,0))
            draw_screen()
            manager.update(time_delta)
            manager.draw_ui(window)
            pygame.display.update()
    pygame.quit()
    sys.exit()


#**************************************************************#
#                          START                               #
#**************************************************************#

def run():
    set_window()
    set_ui()
    load_images()
    main_loop()


if __name__ == "__main__":
    run()
