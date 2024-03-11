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
    
    def add_text(self, text: str, position_x: int = 0, position_y: int = 0, size: int = 16, color: Couleur = (0, 0, 0)):
        """
        Add text to the button.

        Args:
        ----
            text (str): The text to be added.
            position_x (int, optional): The x-coordinate of the text in the button. Defaults to 0.
            position_y (int, optional): The y-coordinate of the text in the button. Defaults to 0.
            size (int, optional): The size of the text. Defaults to 16.
            color (Couleur, optional): The color of the text. Defaults to (0, 0, 0).
        
        Returns:
        -------
            None
        """
        self._text = text
        self._text_size = size
        self._text_color = color
        self._text_position = (self._text_position[0] + position_x, self._text_position[1] + position_y)

    def ajouter_texte(self, texte : str, position_x: int = 0, position_y:int = 0, taille:int = 16, couleur : Couleur = (0, 0, 0)) :
        """
        Ajoute du texte au bouton.

        Args:
        -----
            texte (str): Le texte à ajouter.
            position_x (int, optionnel): La coordonnée x du texte dans le bouton. Par défaut, 0.
            position_y (int, optionnel): La coordonnée y du texte dans le bouton. Par défaut, 0.
            taille (int, optionnel): La taille du texte. Par défaut, 16.
            couleur (Couleur, optionnel): La couleur du texte. Par défaut, (0, 0, 0).
        
        Retour:
        --------
            Aucun
        """
        self.add_text(texte, position_x, position_y, taille, couleur)

    def is_active(self) :
        """
        Check if the button is click.

        Args:
        -----
            None

        Returns:
        --------
            bool: True if the button is click, False otherwise.
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
        Vérifie si le bouton est cliqué.

        Paramètres:
        ----------
            None

        Retour:
        -------
            bool: True si le bouton est cliqué, False sinon.
        """
        return self.is_active()

    def display(self) :
        """
        Display the button in the window.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        pg.draw.rect(self._surface, self._color, self._rect)
        if self._text:
            font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", self._text_size)
            surf = font.render(self._text, True, self._text_color)
            self._surface.blit(surf, self._text_position)
        pg.display.update()

    def afficher(self):
        """
        Affiche le bouton dans la fenêtre.

        Parametre:
        ----------
            None

        Retour:
        --------
            None
        """
        self.display()

class TextArea(Button) :
    def __init__(self, data, surface : pg.Surface):
        super().__init__(data, surface)
        self._old_text : str = ""
        self._text : str = ""

    def display(self):
        """
        Display the text area on the window.

        Args:
        -----
            None

        Returns:
        --------
            None
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
        Affiche la zone de texte dans la fenêtre.

        Parametre:
        ----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.display()

    def write(self, robot : Robot) -> str:
        """
        Writes the user's input into the texte area and returns the final text.

        Args:
        -----
            robot (Robot): The robot.

        Returns:
        --------
            str: The final text after the user has finished writing.
        """
        new_text = ""
        robot._isWriting = True
        text = self.get_text()
        #print("User start writing")
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
        #print("User end writing")
        return text

    def ecrire(self, robot : Robot) -> str:
        """
        Écrit l'entrée de l'utilisateur dans la zone de texte et renvoie le texte final.

        Paramètres:
        -----------
            robot (Robot): Le robot.

        Retour:
        -------
            str: Le texte final après que l'utilisateur ait fini d'écrire.
        """
        return self.write(robot)
    
    def get_text(self) -> str:
        """
        Get the text from the text area.

        Args:
        -----
            None

        Returns:
        --------
            str: The text from the text area.
        """
        return self._text

    def obtenir_texte(self) -> str:
        """
        Renvoie le texte contenu dans la zone de texte.

        Paramètre:
        ----------
            Aucun
        
        Retour:
        -------
            str: Le texte contenu dans la zone de texte.
        """
        return self.get_text()

    def erase_text(self) -> str:
        """
        Erases the current text and returns the old text.

        Args:
        -----
            None

        Returns:
        --------
            str: The text that was erased.
        """
        self._old_text = self._text
        self._text = ""
        self.afficher()
        return self._old_text
    
    def effacer_texte(self) -> str:
        """
        Efface le texte actuel et renvoie l'ancien texte.

        Paramètres:
        ----------
            Aucun

        Retour:
        -------
            str: Le texte qui a été effacé.
        """
        return self.erase_text()
    
    def modify_font_size(self, size: int = 16):
        """
        Modifies the font size of the text area.

        Args:
        -----
            size (int): The new font size to be set. Default is 16.

        Returns:
        --------
            None
        """
        self._text_size = size

    def modifier_taille_police(self, taille: int = 16) :
        """
        Modifie la taille de la police de la zone de text.

        Paramètres:
        -----------
            taille (int): La nouvelle taille de police à définir.

        Retour:
        -------
            None
        """
        self.modify_font_size(taille)
    
    def modify_font_color(self, color : Couleur = (0,0,0)) :
        """
        Modifies the font color of the text area.

        Parameters:
        -----------
            color (Couleur): The RGB color value to set as the font color. Defaults to (0, 0, 0) (black).
        
        Returns:
        --------
            None
        """
        self._text_color = color
    
    def modifier_couleur_police(self, couleur : Couleur = (0,0,0)) :
        """
        Modifie la couleur de police de la zone de texte.

        Paramètres:
        ----------
            couleur (Couleur): La valeur RGB de la couleur à définir comme couleur de police. Par défaut, (0, 0, 0) (noir).

        Retour:
        -------
            None
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
