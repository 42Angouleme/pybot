# **************************************************************#
#                                                              #
#              Python Robot - mdaadoun - 2023                  #
#                                                              #
# **************************************************************#

import pygame as pg
import os

class Visuel:
	def __init__(self, robot, window, debug=False):
		self.debug = debug
		self.robot = robot
		self.window = window
		self.surface_visage = pg.Surface((10, 10))
		self.img = {}
		self.charger_images()

	def charger_images(self):
		img = self.robot.recevoir_images_visages()
		for i in img:
			self.img[i] = pg.image.load(os.getcwd() + "/assets/" + img[i])


	def afficher(self):
		self.afficher_visage()
		
		
	def afficher_visage(self):
		robot_face = self.robot.recevoir_visage()
		offset_x = self.img[robot_face].get_size()[0] / 2
		offset_y = self.img[robot_face].get_size()[1] / 2
		WIDTH = self.window.getWidth()
		HEIGHT = self.window.getHeight()
		self.window.surface.blit(self.img[robot_face], (WIDTH/2 - offset_x, HEIGHT/2 - offset_y))
