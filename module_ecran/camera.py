import time
import cv2
import numpy as np
import pygame as pg
from interactions import UserCardsTracker
import os


def cam_track_cards_app(robot, window) -> int | None:
    """Run an application that opens the camera, and print the users name next to the matching cards."""
    cam = cv2.VideoCapture(0)
    card_tracker = UserCardsTracker(robot.recevoir_webapp())
    pg.font.init()
    font = pg.freetype.Font(os.getcwd() + "/assets/chicago.ttf", size=20)

    running = True
    while running:
        ret, frame = cam.read()
        W = window.surface.get_width()
        H = window.surface.get_height()

        if not ret:
            break
        window.surface.fill([0,0,0])
        font.render_to(window.surface, (W / 2 - 30, H - 40), 'Appuyer sur Q pour quitter.', fgcolor=(197, 203, 216), size=20)

        frame, users = card_tracker.draw(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame,1)
        frame = np.rot90(frame)
        frame = pg.surfarray.make_surface(frame)
        w = frame.get_width()
        h = frame.get_height()

        window.surface.blit(frame, (W / 2 - w / 2, H / 2 - h / 2))
        pg.display.update()
        if len(users):
            robot.configurer_eleve(users[0].id, users[0].first_name, users[0].last_name, users[0].picture_path.split('?')[0])
            robot.change_eleve_connecte("maybe")
            time.sleep(2)
            running = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                   running = False

    cam.release()
    cv2.destroyAllWindows()
    return None
