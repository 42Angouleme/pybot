import pygame as pg
import os
import numpy as np
import cv2
from . import camera


class Visuel:
    def __init__(self, robot, window, debug=False):
        self.debug = debug
        self.robot = robot
        self.window = window
        self.width = self.window.getWidth()
        self.height = self.window.getHeight()
        self.img = {}
        self.charger_images()
        self.carte = None
        self.connect_msg = ""
        self.photo = None
        self.display_photo = False
        self.display_carte = False
        self.display_visage = False

    def charger_images(self):
        img = self.robot.recevoir_images_visages()
        for i in img:
            self.img[i] = pg.image.load(
                os.getcwd() + "/pybot/assets/" + img[i])

    def charger_carte(self, filepath):
        self.carte = pg.image.load(os.getcwd() + filepath)

    def charger_photo(self):
        self.photo = pg.image.load(os.getcwd() + "/pybot/photo.jpg")
        self.display_photo = True

    def afficher_photo(self):
        offset_x = self.photo.get_size()[0] / 2
        offset_y = self.photo.get_size()[1] / 2
        self.window.surface.blit(
            self.photo, (self.width/2 - offset_x, self.height/2 - offset_y))

    def afficher(self):
        if self.display_carte:
            self.afficher_carte()
        if self.display_photo:
            self.afficher_photo()
        if self.display_visage:
            self.afficher_visage()

    def afficher_carte(self):
        offset_x = self.carte.get_size()[0] / 2
        offset_y = self.carte.get_size()[1] / 2
        print(self.carte.get_size()[0], self.carte.get_size()[1])
        self.window.surface.blit(
            self.carte, (self.width/2 - offset_x, self.height/2 - offset_y))

    def afficher_visage(self):
        robot_face = self.robot.recevoir_visage()
        print(robot_face)
        offset_x = self.img[robot_face].get_size()[0] / 2
        offset_y = self.img[robot_face].get_size()[1] / 2
        self.window.surface.blit(
            self.img[robot_face], (self.width/2 - offset_x, self.height/2 - offset_y))

    def afficher_camera(self, ui):
        camera.cam_track_cards_app(ui, self.window)

    def set_visage(self, set):
        self.display_visage = set

    def appliquer_filtre(self, filter):
        image_path = os.getcwd() + "/pybot/photo.jpg"
        image = cv2.imread(image_path)
        if image is None:
            print(f"Il faut prendre une image avant de pouvoir appliquer un filtre.")
            return
        filtered_image = filter(image)
        cv2.imwrite(image_path, filtered_image)
