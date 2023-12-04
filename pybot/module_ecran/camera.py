import time
import cv2
import numpy as np
import pygame as pg
from ..interactions import UserCardsTracker
import os


def cam_track_cards_app(interface, window) -> int | None:
    """Run an application that opens the camera, and print the users name next to the matching cards."""
    cam = cv2.VideoCapture(0)
    card_tracker = UserCardsTracker()

    while window.get_camera_running():
        ret, frame = cam.read()
        W = window.getWidth()
        H = window.getHeight()

        if not ret:
            break
        window.surface.fill([0, 0, 0])

        frame, users = card_tracker.draw(frame)
        if (window.check_capture()):
            cv2.imwrite("pybot/photo.jpg", frame)
            time.sleep(1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.flip(frame, 1)
        frame = np.rot90(frame)
        frame = pg.surfarray.make_surface(frame)
        w = frame.get_width()
        h = frame.get_height()

        window.surface.blit(frame, (W / 2 - w / 2, H / 2 - h / 2))
        interface.draw()
        for event in pg.event.get():
            interface.check_event(event)
        pg.display.update()

    cam.release()
    cv2.destroyAllWindows()
    return None
