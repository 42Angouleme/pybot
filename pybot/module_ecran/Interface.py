import pygame as pg
import os

class Interface:
    def __init__(self, surface, debug=False):
        self.debug = debug
        self.surface = surface
        pg.freetype.init()

    def create_button(self, w, h, x, y, c):
        data = {
            "width":w,
            "height":h,
            "x":x,
            "y":y,
            "color":c,  
        }
        return Button(data, self.surface)

    def create_text_area(self, w, h, x, y, c):
        data = {
            "width":w,
            "height":h,
            "x":x,
            "y":y,
            "color":c,  
        }
        return TextArea(data, self.surface)

class Button:
    def __init__(self, data, surface):
        self.surface = surface
        self.position = (data['x'], data['y'])
        self.rect = pg.Rect(data['x'], data['y'], data["width"], data["height"])
        self.color = data["color"]
        self.text = None
        self.text_size = 16
        self.text_color = (0, 0, 0)
        self.text_position = self.position
        self.pressed = False
        
    def ajouter_texte(self, texte, position_x=0, position_y=0, taille=16, couleur=(0, 0, 0)):
        """
            Ajoute le texte dans le bouton, a la position x et y dans le bouton. \n
            Il est aussi possible de fournir une taille et une couleur au texte.
        """
        self.text = texte
        self.text_size = taille
        self.text_color = couleur
        self.text_position = (self.text_position[0] + position_x, self.text_position[1] + position_y)

    def verifier_contact(self):
        """
            Retourne vrai si le bouton a été cliqué.
        """
        try:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                if pg.mouse.get_pressed()[0] and not self.pressed:
                    self.pressed = True
                    return True
            if pg.mouse.get_pressed() == (0,0,0):
                self.pressed = False
        except:
            pass
        return False

    def afficher(self):
        """
            Affiche le bouton dans la fenêtre principale.
        """
        pg.draw.rect(self.surface, self.color, self.rect)
        if self.text:
            font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", self.text_size)
            surf = font.render(self.text, True, self.text_color)
            self.surface.blit(surf, self.text_position)
        pg.display.update()

class TextArea(Button) :
    def __init__(self, data, surface):
        super().__init__(data, surface)
        self.old_text = ""
    
    def afficher(self):
        """
            Affiche la zone de texte dans la fenêtre principale.
        """
        pg.draw.rect(self.surface, self.color, self.rect)
        if self.text:
            font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", self.text_size)
            surf = font.render(self.old_text, True, self.color)
            surf = font.render(self.text, True, self.text_color)
            self.surface.blit(surf, self.text_position)
        pg.display.update()
        
    def add_text(self, texte,position_x=0, position_y=0, taille=16, couleur=(0, 0, 0), old_text = ""):
        """
            Permet l'affiche d'un texte dans la zone de texte
        """
        self.text = texte
        self.text_size = taille
        self.old_text = old_text
        self.text_color = couleur
        self.text_position = (self.position[0] + position_x, self.position[1] + position_y)
