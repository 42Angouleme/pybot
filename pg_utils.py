import pygame as pg

def drawText(surface, text, pos, color=(0, 0, 0), size=24, font=None, align="left"):
	font = pg.font.SysFont(font, size)
	img = font.render(text, True, color)
	if (align == "center"):
		placement = img.get_rect(center=pos)
		surface.blit(img, placement)
	else:
		surface.blit(img, pos)


class Button:
	"""
	La classe de nos boutons
	"""

	def __init__(self, dimension, text, colors):
		"""
		Méthode servant à créer nos boutons. Prends en paramètre :
		dimension (x, y, width, height), text (text (str), size (int), font (str), color (r, g, b)), colors (colorInactive (r, g, b), colorActive (r, g, b)), action (str)
		"""
		self._x = dimension[0]
		self._y = dimension[1]
		self._width = dimension[2]
		self._height = dimension[3]
		self._text = text
		self._colors = colors
		self._active = 0


	def draw(self, fen):
		"""
		Méthode servant à dessiner nos boutons
		"""
		self.mouse_on_button()
		pg.draw.rect(fen, self._colors[self._active], (self._x - self._width//2, self._y - self._height//2, self._width, self._height)) # On centre le bouton dans à la position qui nous est demandé
		self.draw_text(fen)


	def draw_text(self, fen):
		"""
		Méthode servant à afficher le texte dans le bouton.
		"""
		font1 = pg.font.SysFont(self._text[2], self._text[1])
		text1 = font1.render(self._text[0], 1, self._text[3])
		placement = text1.get_rect(center=(self._x, self._y)) # Sert à centrer le texte
		fen.blit(text1, placement)


	def mouse_on_button(self):
		"""
		Méthode permettant de définir si la sourie est sur le bouton ou non
		"""
		pos = pg.mouse.get_pos() # On récupère la position de la sourie
		mouse = pg.Rect(pos[0], pos[1], 1, 1) # On créer un rectangle à la position de la sourie
		if mouse.colliderect((self._x - self._width//2, self._y - self._height//2, self._width, self._height)):  # On se sert de la méthode colliderect pour savoir si la sourie est sur le bouton
			self._active = 1 # Permet de mettre la couleur claire au bouton
			return True
		else:
			self._active = 0 # Remet la couleur foncé au bouton
			return False


	def click(self, key2):
		"""
		Méthode servant à dire si le bouton est cliqué
		"""
		return key2[0] == 1 and self.mouse_on_button()


	def set_on_color_if(self, condition, colorTrue, colorFalse):
		if (condition):
			self._colors[0] = colorTrue
		else:
			self._colors[0] = colorFalse
