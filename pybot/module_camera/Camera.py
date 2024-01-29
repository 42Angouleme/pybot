import cv2
import numpy as np
import pygame as pg
from .UserCardsTracker import UserCardsTracker
from flask import Flask


class Camera:
    def __init__(self, surface):
        self.frame = None
        self.camera = cv2.VideoCapture(0)
        self.surface = surface
        self.card_tracker: UserCardsTracker = None
        self.x = 0
        self.y = 0

    def updateUserCardsTracker(self, webapp: Flask):
        # Handle Unintialized webapp
        if not isinstance(webapp, Flask):
            raise ValueError
        self.card_tracker = UserCardsTracker(webapp)

    def stop(self):
        self.camera.release()
        cv2.destroyAllWindows()

    def display(self, x, y):
        self.x = x
        self.y = y
        try:
            ret, self.frame = self.camera.read()
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = np.rot90(self.frame)
            self.frame = pg.surfarray.make_surface(self.frame)
            self.surface.blit(self.frame, (self.x, self.y))
        except:
            pass
    
    # def afficher_camera(self, position_x: int = 0, position_y: int = 0):
    #     """
    #         Affiche la caméra aux coordonées x et y.
    #     """
    #     self.x = position_x
    #     self.y = position_y
    #     try:
    #         ret, self.frame = self.camera.read() # ret is unused ?
    #         self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
    #         self.frame = np.rot90(self.frame)
    #         self.frame = pg.surfarray.make_surface(self.frame)
    #         self.surface.blit(self.frame, (self.x, self.y))
    #     except:
    #         pass

    def capture(self, file_name):
        try:
            ret, frame = self.camera.read()
            if not ret:
                return None
            frame = cv2.flip(frame, 1)
            cv2.imwrite("images/" + file_name + ".jpg", frame)
        except:
            pass

    def detect_card(self, min_threshold: float, stop_threshold: float):
        """
        Detect user and if user found, the card is detected and framed in the frame

        Params
            - min_threshold: Sufficient threshold to interpret frame as similar card
            - stop_threshold: Threshold to interpret frame as corresponding card
        Returns
            - detected_card: card detected by algorithm and does not match any
                user's card
        """
        # Handle first launch of camera with 0 frame
        if self.frame is None:
            return []
        frame, detected_card = self.card_tracker.get_detected_card(
                self.frame,
                min_threshold,
                stop_threshold)
        if detected_card is not None:
            self.surface.blit(frame, (self.x, self.y))
        return detected_card, frame

    def detect_user(self, min_threshold, stop_threshold):
        """
        Detect user and if user found, the card is detected and framed in the frame

        Params
            - min_threshold: Sufficient threshold to interpret frame as similar card
            - stop_threshold: Threshold to interpret frame as corresponding card
        Returns
            - matching_user: User that matches the most for detected card
        """
        # Handle first launch of camera with 0 frame
        if self.frame is None:
            return []
        frame, user_detected = self.card_tracker.get_detected_user(
                self.frame,
                min_threshold,
                stop_threshold)
        if user_detected is not None:
            self.surface.blit(frame, (self.x, self.y))
        return user_detected, frame
