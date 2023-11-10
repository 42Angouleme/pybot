# **************************************************************#
#                                                              #
#              Python Robot - mdaadoun - 2023                  #
#                                                              #
# **************************************************************#

import pygame as pg
import os
from .data import STATUS
from . import camera
import time

class Visuel:
	def __init__(self, robot, window, debug=False):
		self.debug = debug
		self.robot = robot
		self.window = window
		self.width = self.window.getWidth()
		self.height = self.window.getHeight()
		self.surface_visage = pg.Surface((10, 10))
		self.img = {}
		self.charger_images()
		self.carte = None
		self.connect_msg = ""

	def charger_images(self):
		img = self.robot.recevoir_images_visages()
		for i in img:
			self.img[i] = pg.image.load(os.getcwd() + "/assets/" + img[i])

	def charger_carte(self, filepath):
		print("charge carte ")
		self.carte = pg.image.load(os.getcwd() + filepath)

	def afficher(self):
		if self.window.getStatus() == STATUS['DISPLAY']:
			self.afficher_visage()
		if self.window.getStatus() == STATUS['CAMERA']:
			self.afficher_camera()
		if self.window.getStatus() == STATUS['MENU']:
			if self.robot.eleve_connecte() == "maybe":
				self.afficher_carte()
			elif self.robot.eleve_connecte() == "no":
				print("Connecte toi. (temp: CAMERA)")

		
	def afficher_carte(self):
		offset_x = self.carte.get_size()[0] / 2
		offset_y = self.carte.get_size()[1] / 2
		print(self.carte.get_size()[0], self.carte.get_size()[1])
		self.window.surface.blit(self.carte, (self.width/2 - offset_x, self.height/2 - offset_y))
		print(self.connect_msg)

	def afficher_visage(self):
		robot_face = self.robot.recevoir_visage()
		offset_x = self.img[robot_face].get_size()[0] / 2
		offset_y = self.img[robot_face].get_size()[1] / 2
		self.window.surface.blit(self.img[robot_face], (self.width/2 - offset_x, self.height/2 - offset_y))

	def afficher_camera(self):
		time.sleep(1)
		camera.cam_track_cards_app(self.robot, self.window)
		eleve = self.robot.obtenir_eleve()
		self.charger_carte(eleve["carte"])
		self.connect_msg = f"Bonjour {eleve['prenom']} {eleve['nom']}, est ce que c'est bien toi ?"
		self.window.setStatus(STATUS['MENU'])