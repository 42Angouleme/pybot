from ..types import Couleur
from pybot import Robot
import pygame as pg
import os

class Interface:
    def __init__(self, surface) :
        self.__surface : pg.Surface = surface
        pg.freetype.init()

    def create_button(self, w: int, h:int , x: int , y:int , c: int) :
        data = {
            "width":w,
            "height":h,
            "x":x,
            "y":y,
            "color":c,  
        }
        return Button(data, self.__surface)

    def create_text_area(self, w: int, h:int , x: int , y:int , c: int) :
        data = {
            "width":w,
            "height":h,
            "x":x,
            "y":y,
            "color":c,  
        }
        return TextArea(data, self.__surface)

class Button:
    def __init__(self, data, surface : pg.Surface) :
        self.__surface : pg.surface = surface
        self.__position : tuple[int, int] = (data['x'], data['y'])
        self.__rect : pg.Rect = pg.Rect(data['x'], data['y'], data["width"], data["height"])
        self.__color : Couleur = data["color"]
        self.__text : str = None
        self.__text_size : int = 16
        self.__text_color : Couleur = (0, 0, 0)
        self.__text_position : tuple[int, int ] = self.__position
        self.__pressed : bool = False
    
    def add_text(self, text: str, position_x: int = 0, position_y: int = 0, size: int = 16, color : Couleur = (0, 0, 0)) :
        """
        """
        self.__text = text
        self.__text_size = size
        self.__text_color = color
        self.__text_position = (self.__text_position[0] + position_x, self.__text_position[1] + position_y)

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
            if self.__rect.collidepoint(pg.mouse.get_pos()):
                if pg.mouse.get_pressed()[0] and not self.__pressed:
                    self.__pressed = True
                    return True
            if pg.mouse.get_pressed() == (0,0,0):
                self.__pressed = False
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
        pg.draw.rect(self.__surface, self.__color, self.__rect)
        if self.__text:
            font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", self.__text_size)
            surf = font.render(self.__text, True, self.__text_color)
            self.__surface.blit(surf, self.__text_position)
        pg.display.update()

    def afficher(self):
        """
            Affiche le bouton dans la fenêtre principale.
        """
        self.display()

class TextArea(Button) :
    def __init__(self, data, surface : pg.Surface):
        super().__init__(data, surface)
        self.__old_text : str = ""
        self.__text : str = ""

    def display(self):
        """
            Affiche la zone de texte dans la fenêtre principale.
        """
        pg.draw.rect(self.__surface, self.__color, self.__rect)
        if self.__text != "":
            font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", self.__text_size)
            surf = font.render(self.__old_text, True, self.__color)
            surf = font.render(self.__text, True, self.__text_color)
            self.__surface.blit(surf, self.__text_position)
        pg.display.update()
    
    def afficher(self):
        """
            Affiche la zone de texte dans la fenêtre principale.
        """
        self.display()

    def write(self, robot : Robot) :
        """
        """
        new_text = ""
        robot._isWriting = True
        text = self.get_text()
        #print("User start writing")
        while robot._isWriting:
            if not self.__pressed:
                robot._isWriting = False
            new_text = robot._get_user_entry(text, self)
            if (not robot.actif):
                return ""
            if (new_text != text):
                if ("\r" in new_text):
                    robot._isWriting = False
                    self.__pressed = False
                    break
                self.__add_text(new_text, 10, 10, text)
                self.afficher()
                #robot.actualiser_affichage()  # Vraiment utile ??
                #robot.fenetre.refresh_display()
                text = new_text
        #print("User end writing")
        return text

    def ecrire(self, robot):
        """
            Permet à l'utilisateur d'écrire dans la zone de texte associé.
            Renvoit le texte écrit par l'utilisateur.
        """
        self.write(robot)
    
    def get_text(self) :
        """
        """
        return self.__text

    def obtenir_texte(self) :
        """
            Renvoie le texte contenu dans la zone de texte.
        """
        return self.get_text()

    def erase_text(self) :
        """
        """
        self.__old_text = self.__text
        self.__text = ""
        self.afficher()
        return self.__old_text
    
    def effacer_texte(self) :
        """
            Permet d'effacer le contenu de la zone de texte.
            Renvoi le texte contenu
        """
        return self.erase_text()
    
    def modify_font_size(self, size : int = 16) :
        """
        """
        self.__text_size = size

    def modifier_taille_police(self, taille :int = 16) :
        """
            Permet de changer la taille de la police.
            Utilisée sans paramètre, cela réinitialise la taille.
        """
        self.modify_font_size(taille)
    
    def modify_font_color(self, color : Couleur = (0,0,0)) :
        """
        """
        self.__text_color = color
    
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
        if not self.__rect.collidepoint(position) :
            self.__pressed = False
            return True
        return False
    
    def __add_text(self, texte : str ,position_x: int = 0, position_y: int = 0, old_text: str = ""):
        """
            Add text to display in the text area
        """
        self.__text = texte
        self.__old_text = old_text
        self.__text_position = (self.__position[0] + position_x, self.__position[1] + position_y)
