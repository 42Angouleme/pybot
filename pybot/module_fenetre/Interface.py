from ..types import Couleur
from pybot import Robot
import pygame as pg
import os

class Interface:
    def __init__(self, surface) :
        self._surface : pg.Surface = surface
        pg.freetype.init()

    def create_button(self, w: int, h:int , x: int , y:int , c: int) :
        data = {
            "width":w,
            "height":h,
            "x":x,
            "y":y,
            "color":c,  
        }
        return Button(data, self._surface)

    def create_text_area(self, w: int, h:int , x: int , y:int , c: int) :
        data = {
            "width":w,
            "height":h,
            "x":x,
            "y":y,
            "color":c,  
        }
        return TextArea(data, self._surface)

class Button:
    def __init__(self, data, surface : pg.Surface) :
        self._surface : pg.Surface = surface
        self._position : tuple[int, int] = (data['x'], data['y'])
        self._rect : pg.Rect = pg.Rect(data['x'], data['y'], data["width"], data["height"])
        self._color : Couleur = data["color"]
        self._text : str = None
        self._text_size : int = 16
        self._text_color : Couleur = (0, 0, 0)
        self._text_position : tuple[int, int ] = self._position
        self._pressed : bool = False
    
    def add_text(self, text: str, position_x: int = 0, position_y: int = 0, size: int = 16, color : Couleur = (0, 0, 0)) :
        """
        """
        self._text = text
        self._text_size = size
        self._text_color = color
        self._text_position = (self._text_position[0] + position_x, self._text_position[1] + position_y)

    def ajouter_texte(self, texte : str, position_x: int = 0, position_y:int = 0, taille:int = 16, couleur : Couleur = (0, 0, 0)) :
        """
            Ajoute le texte dans le bouton, a la position x et y dans le bouton. \n
            Il est aussi possible de fournir une taille et une couleur au texte.
        """
        self.add_text(texte, position_x, position_y, taille, couleur)

    def is_active(self) :
        """
            Retourne vrai si le bouton a été cliqué.
        """
        try:
            if self._rect.collidepoint(pg.mouse.get_pos()):
                if pg.mouse.get_pressed()[0] and not self._pressed:
                    self._pressed = True
                    return True
            if pg.mouse.get_pressed() == (0,0,0):
                self._pressed = False
        except:
            pass
        return False

    def est_actif(self) :
        """
            Retourne vrai si le bouton a été cliqué.
        """
        return self.is_active()

    def display(self) :
        """
        """
        pg.draw.rect(self._surface, self._color, self._rect)
        if self._text:
            font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", self._text_size)
            surf = font.render(self._text, True, self._text_color)
            self._surface.blit(surf, self._text_position)
        pg.display.update()

    def afficher(self):
        """
            Affiche le bouton dans la fenêtre principale.
        """
        self.display()

class TextArea(Button) :
    def __init__(self, data, surface : pg.Surface):
        super().__init__(data, surface)
        self._old_text : str = ""
        self._text : str = ""

    def display(self):
        """
            Affiche la zone de texte dans la fenêtre principale.
        """
        pg.draw.rect(self._surface, self._color, self._rect)
        if self._text != "":
            font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", self._text_size)
            surf = font.render(self._old_text, True, self._color)
            surf = font.render(self._text, True, self._text_color)
            self._surface.blit(surf, self._text_position)
        pg.display.update()
    
    def afficher(self):
        """
            Affiche la zone de texte dans la fenêtre principale.
        """
        self.display()

    def write(self, robot : Robot) -> str:
        """
        """
        new_text = ""
        robot._isWriting = True
        text = self.get_text()
        print("User start writing")
        while robot._isWriting:
            if not self._pressed:
                robot._isWriting = False
            new_text = robot._get_user_entry(text, self)
            if (not robot.is_active()):
                return ""
            if (new_text != text):
                if ("\r" in new_text):
                    robot._isWriting = False
                    self._pressed = False
                    break
                self.__add_text(new_text, 10, 10, text)
                self.afficher()
                robot.fenetre.refresh_display()
                text = new_text
        print("User end writing")
        return text

    def ecrire(self, robot : Robot) -> str:
        """
            Permet à l'utilisateur d'écrire dans la zone de texte associé.
            Renvoit le texte écrit par l'utilisateur.
        """
        return self.write(robot)
    
    def get_text(self) -> str:
        """
        """
        return self._text

    def obtenir_texte(self) -> str:
        """
            Renvoie le texte contenu dans la zone de texte.
        """
        return self.get_text()

    def erase_text(self) -> str:
        """
        """
        self._old_text = self._text
        self._text = ""
        self.afficher()
        return self._old_text
    
    def effacer_texte(self) -> str:
        """
            Permet d'effacer le contenu de la zone de texte.
            Renvoi le texte contenu
        """
        return self.erase_text()
    
    def modify_font_size(self, size : int = 16) :
        """
        """
        self._text_size = size

    def modifier_taille_police(self, taille :int = 16) :
        """
            Permet de changer la taille de la police.
            Utilisée sans paramètre, cela réinitialise la taille.
        """
        self.modify_font_size(taille)
    
    def modify_font_color(self, color : Couleur = (0,0,0)) :
        """
        """
        self._text_color = color
    
    def modifier_couleur_police(self, couleur : Couleur = (0,0,0)) :
        """
            Permet de modifier la couleur de la police.
            Utilisée sans paramètre, cela réinitialise la couleur.
        """
        self.modify_font_color(couleur)

    ### Private Methode ###

    def _check_is_outside(self, position):
        """
            Check if the mouse click is outside of the texte area.
        """
        if not self._rect.collidepoint(position) :
            self._pressed = False
            return True
        return False
    
    def __add_text(self, texte : str ,position_x: int = 0, position_y: int = 0, old_text: str = ""):
        """
            Add text to display in the text area
        """
        self._text = texte
        self._old_text = old_text
        self._text_position = (self._position[0] + position_x, self._position[1] + position_y)
