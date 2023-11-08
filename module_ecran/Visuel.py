#**************************************************************#
#                                                              #
#              Python Robot - mdaadoun - 2023                  #
#                                                              #
#**************************************************************#

import pygame as pg

class Visuel:
	def __init__(self, robot, window, debug=False):
		self.robot = robot
		self.window = window
		self.surface_visage = pg.Surface((10, 10))
	
	def afficher_visage(self):
		print("current visage: ", self.robot.get_visage())