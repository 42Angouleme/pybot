import cv2
import numpy as np
import pygame as pg
# from .UserCardsTracker import UserCardsTracker


class Camera:
    def __init__(self, surface):
        self.frame = None
        self.camera = cv2.VideoCapture(0)
        self.surface = surface
        # self.card_tracker = UserCardsTracker()
        self.x = 0
        self.y = 0

    def stop(self):
        self.camera.release()
        cv2.destroyAllWindows()

    def display(self, x, y):
        self.x = x
        self.y = y
        try:
            ret, self.frame = self.camera.read()
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = cv2.flip(self.frame, 1)
            self.frame = np.rot90(self.frame)
            self.frame = pg.surfarray.make_surface(self.frame)
            self.surface.blit(self.frame, (self.x, self.y))
        except:
            pass

    def capture(self, file_name):
        try:
            ret, frame = self.camera.read()
            if not ret:
                return None
            cv2.imwrite("images/" + file_name + ".jpg", frame)
        except:
            pass

    # def detect_card(self):
    #     frame, users = self.card_tracker.draw(self.frame)
    #     self.surface.blit(frame, (self.x, self.y))
    #     print(frame, users)
    #     return users
