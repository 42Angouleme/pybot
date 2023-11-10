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

	def charger_images(self):
		img = self.robot.recevoir_images_visages()
		for i in img:
			self.img[i] = pg.image.load(os.getcwd() + "/assets/" + img[i])


	def afficher(self):
		if self.window.getStatus() == STATUS['DISPLAY']:
			self.afficher_visage()
		if self.window.getStatus() == STATUS['CAMERA']:
			self.afficher_camera()
		
	def afficher_visage(self):
		robot_face = self.robot.recevoir_visage()
		offset_x = self.img[robot_face].get_size()[0] / 2
		offset_y = self.img[robot_face].get_size()[1] / 2
		self.window.surface.blit(self.img[robot_face], (self.width/2 - offset_x, self.height/2 - offset_y))


	# def auth():
	# 	from interactions import UserCardsTracker
	# 	import time
	# 	time.sleep(2)
	# 	cam_track_cards_app(app)

	def afficher_camera(self):
		time.sleep(1)
		camera.cam_track_cards_app(self.robot.recevoir_webapp())
		self.window.setStatus(STATUS['MENU'])
		# threading.Thread(target=auth).start()
		# ret, frame = camera.read()
		# self.window.surface.fill([0,0,0])

		# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		# frame = np.rot90(frame)
		# frame = pg.surfarray.make_surface(frame)
		# self.window.surface.blit(frame, (0,0))
		# width = self.width / 2
		# offset_x = width / 2
		# height = self.height / 2
		# offset_y = height / 2
		# pg.draw.rect(self.window.surface, (100, 255, 255), (width - offset_x , height - offset_y, width, height))