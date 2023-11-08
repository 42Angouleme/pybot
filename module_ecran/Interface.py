#**************************************************************#
#                                                              #
#              Python Robot - mdaadoun - 2023                  #
#                                                              #
#**************************************************************#

import pygame as pg
import pygame_gui as pgui
import os

class Interface:
	def __init__(self, window, debug=False):
		self.window = window
		self.manager = pgui.UIManager((window.getWidth(), window.getHeight()), os.getcwd() + '/assets/theme.json')
		self.button = {}
		self.load_buttons()

	def draw(self):            
		self.manager.update(self.window.getDeltaTime())
		self.manager.draw_ui(self.window.surface)

	def load_buttons(self):
		self.button["face_button"] = pgui.elements.UIButton(
			relative_rect=pg.Rect((self.window.getWidth() / 2 - 75, self.window.getHeight() - 60), (150, 50)),
			text='Face',
			manager=self.manager
		)
		self.button["speaker_button"] = pgui.elements.UIButton(
			relative_rect=pg.Rect((10, 10), (150, 50)),
			text='SPEAKER',
			manager=self.manager
		)
		self.button["microphone_button"] = pgui.elements.UIButton(
			relative_rect=pg.Rect((160, 10), (200, 50)),
			text='MICROPHONE',
			manager=self.manager
		)
		self.button["camera_button"] = pgui.elements.UIButton(
			relative_rect=pg.Rect((360, 10), (150, 50)),
			text='CAMERA',
			manager=self.manager
		)
		self.button["display_button"] = pgui.elements.UIButton(
			relative_rect=pg.Rect((510, 10), (150, 50)),
			text='DISPLAY',
			manager=self.manager
		)

	def check_event(self, event):
		if event.type == pg.USEREVENT:
			if event.user_type == pgui.UI_BUTTON_PRESSED:
				if event.ui_element == self.button["face_button"]:
					print("clicked_button_face, change face")
				if event.ui_element == self.button["speaker_button"]:
					print("clicked_button_speaker")
				if event.ui_element == self.button["microphone_button"]:
					print("clicked_button_microphone")
				if event.ui_element == self.button["camera_button"]:
					print("clicked_button_camera")
				if event.ui_element == self.button["display_button"]:
					print("clicked_button_display")
		self.manager.process_events(event)