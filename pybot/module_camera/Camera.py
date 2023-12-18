import cv2
import numpy as np
import pygame as pg
# from .UserCardsTracker import UserCardsTracker


class Camera:
    def __init__(self, surface):
        self.cam = cv2.VideoCapture(0)
        self.surface = surface
        # self.track_card = False

    def stop(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def display(self, x, y):
        # card_tracker = UserCardsTracker()
        ret, frame = self.cam.read()
        # W = window.getWidth()
        # H = window.getHeight()
        # window.surface.fill([0, 0, 0])

        # frame, users = card_tracker.draw(frame)
        # if (window.check_capture()):
        #     cv2.imwrite("pybot/photo.jpg", frame)
        #     time.sleep(1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        frame = np.rot90(frame)
        frame = pg.surfarray.make_surface(frame)

        # w = frame.get_width()
        # h = frame.get_height()

        # self.surface.surface.blit(frame, (W / 2 - w / 2, H / 2 - h / 2))
        self.surface.blit(frame, (x, y))
        # interface.draw()
        # for event in pg.event.get():
        #     interface.check_event(event)
        pg.display.update()

    def capture(self, file_name):
        ret, frame = self.cam.read()
        if not ret:
            return None
        cv2.imwrite("images/" + file_name + ".jpg", frame)

    def detect_card(self):
        pass