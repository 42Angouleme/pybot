from .Interface import Interface
from cv2.typing import MatLike
from .Interface import Button
from ..types import Couleur
import pygame as pg
import os, sys


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'  # need to be declared before to import pygame

class Fenetre:
    def __init__(self, emotion_dict : dict[str, str], width: int = 800, height: int = 600) :
        self.__title = "Pybot"
        self.__is_fullscreen : bool = False
        # main surface
        self.__surface : pg.Surface = None
        # objects
        self.__interface : Interface = None
        # update flags
        self.__toggle_in_fullscreen : bool = False
        self.__toggle_out_fullscreen : bool  = False
        self.__change_title : bool = False
        # theming colors data
        self.__background_color : Couleur = (0, 0, 0)
        # clock and fps
        self.__color : pg.time.Clock = pg.time.Clock()
        self.__fps : float = 30
        self.__emotion_dict : dict[str, str] = emotion_dict
        pg.init()
        self.__surface = pg.display.set_mode((width, height))
    
    def open_window(self) :
        """
        Opens the window.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        pg.display.set_caption(self.__title)
        self.__interface = Interface(self.__surface)
        
    def ouvrir_fenetre(self):
        """
        Ouvre la fenêtre.

        Paramètres:
        ----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.open_window()
    
    def change_background_color(self, color: Couleur) :
        """
        Changes the background color of the window.

        Args:
        -----
            color (Couleur): A tuple representing the RGB values of the desired color.

        Returns:
        --------
            None
        """
        try:
            self.__change_background_color(color[0], color[1], color[2])
        except AttributeError:
            self.__error_message("the window hasn't been opened.", "en")
    
    def changer_couleur_fond(self, couleur: Couleur) :
        """
        Change la couleur de fond de la fenêtre.

        Paramètres:
        -----------
            couleur (Couleur): Un tuple représentant les valeurs RGB de la couleur souhaitée.

        Retour:
        -------
            Aucun
        """
        try :
            self.__change_background_color(couleur[0], couleur[1], couleur[2])
        except AttributeError :
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")

    def full_screen(self, change: bool) :
        """
        Toggles the fullscreen mode of the window.

        Args:
        -----
            change (bool): If True, changes the window to fullscreen mode. If False, changes the window to normal mode.
        
        Returns:
        --------
            None
        """
        if change == self.__is_fullscreen:
            return
        if change:
            self.__toggle_in_fullscreen = True
        else:
            self.__toggle_out_fullscreen = True
    
    def plein_ecran(self, changer: bool) :
        """
        Bascule le mode plein écran de la fenêtre.

        Paramètres:
        ----------
            changer (bool): Si True, passe la fenêtre en mode plein écran. Si False, passe la fenêtre en mode normal.
        
        Retour:
        -------
            Aucun
        """
        self.full_screen(changer)
    
    def change_title(self, title: str) :
        """
        Change the title of the window.

        Args:
        -----
            title (str): The new title for the window.

        Returns:
        --------
            None
        """
        try:
            self.__change_window_title(title)
        except AttributeError:
            self.__error_message("title must be defined after the window.", "en")
    
    def changer_titre(self, titre: str) :
        """
        Change le titre de la fenêtre.

        Paramètres:
        ----------
            titre (str): Le nouveau titre de la fenêtre.

        Retour:
        -------
            Aucun
        """
        try:
            self.__change_window_title(titre)
        except AttributeError:
            self.__error_message("le titre doit être défini après création de la fenêtre.", "fr")

    def refresh_display(self) :
        """
        Refreshes the window display.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        try:
            self.__check_flags()
            self.__color.tick(self.__fps)
            pg.display.update()
        except:
            pass

    def actualiser_affichage(self) :
        """
        Rafraîchit l'affichage de la fenêtre.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.refresh_display()

    def display_background(self) :
        """
        Displays the background of the window with the last colors saved by the method change_background_color.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        try:
            self.__draw_background()
        except AttributeError:
            self.__error_message("the window hasn't been opened.", "en")
            
    def afficher_fond(self):
        """
        Affiche l'arrière-plan de la fenêtre avec les dernières couleurs enregistrées par la méthode changer_couleur_fond.

        Paramètres:
        ----------
            Aucun

        Retour:
        -------
            Aucun
        """
        try:
            self.__draw_background()
        except AttributeError:
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")
    
    def draw_rectangle(self, width: int, height: int, position_x: int, position_y: int, color: Couleur) :
        """
        Draw a rectangle on the window.

        Args:
        -----
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            position_x (int): The x-coordinate of the top-left corner of the rectangle.
            position_y (int): The y-coordinate of the top-left corner of the rectangle.
            color (Couleur): The color of the rectangle.

        Returns:
        --------
            None
        """
        try:
            self.__draw_rect(width, height, position_x, position_y, color)
        except AttributeError:
            self.__error_message("the window hasn't been opened.", "en")
    
    def dessiner_rectangle(self, longueur: int, hauteur: int, position_x: int, position_y: int, couleur: Couleur) :
        """
        Dessine un rectangle dans la fenêtre.

        Paramètres:
        ----------
            longueur (int): La largeur du rectangle.
            hauteur (int): La hauteur du rectangle.
            position_x (int): La coordonnée x du coin supérieur gauche du rectangle.
            position_y (int): La coordonnée y du coin supérieur gauche du rectangle.
            couleur (Couleur): La couleur du rectangle.

        Retour:
        ------
            Aucun
        """
        try:
            self.__draw_rect(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")
    
    def display_text(self, text, position_x: int = 0, position_y: int = 0, size: int = 16, color: Couleur = (0, 0, 0)) :
        """
        Display text on the window.

        Args:
        -----
            text (str): The text to be displayed.
            position_x (int, optional): The x-coordinate of the text position. Defaults to 0.
            position_y (int, optional): The y-coordinate of the text position. Defaults to 0.
            size (int, optional): The font size of the text. Defaults to 16.
            color (Couleur, optional): The color of the text. Defaults to (0, 0, 0).
        
        Returns:
        --------
            None
        """
        try:
            self.__draw_text(text, position_x, position_y, size, color)
        except AttributeError:
            self.__error_message("the window hasn't been opened.", "en")
    
    def afficher_texte(self, texte, position_x: int = 0, position_y: int = 0, taille: int = 16, couleur: Couleur = (0, 0, 0)) :
        """
        Affiche du texte dans la fenêtre.

        Paramètres:
        -----------
            texte (str): Le texte à afficher.
            position_x (int, optionnel): La coordonnée x de la position du texte. Par défaut, 0.
            position_y (int, optionnel): La coordonnée y de la position du texte. Par défaut, 0.
            taille (int, optionnel): La taille de la police du texte. Par défaut, 16.
            couleur (Couleur, optionnel): La couleur du texte. Par défaut, (0, 0, 0).
        
        Retour:
        -------
            Aucun
        """
        try:
            self.__draw_text(texte, position_x, position_y, taille, couleur)
        except AttributeError:
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")
    
    def display_image(self, file_path: str, position_x: int, position_y: int) :
        """
        Display an image on the window at the specified position.

        Args:
        -----
            file_path (str): The path to the image file.
            position_x (int): The x-coordinate of the top-left corner of the image.
            position_y (int): The y-coordinate of the top-left corner of the image.

        Returns:
        --------
            None
        """
        try:
            img = pg.image.load(os.getcwd() + file_path)
            self.__surface.blit(img, (position_x, position_y))
        except:
            pass

    def afficher_image(self, chemin_fichier: str, position_x: int, position_y: int) :
        """
        Affiche une image dans la fenêtre à la position spécifiée.

        Paramètres:
        -----------
            chemin_fichier (str): Le chemin vers le fichier image.
            position_x (int): La coordonnée x du coin supérieur gauche de l'image.
            position_y (int): La coordonnée y du coin supérieur gauche de l'image.

        Retour:
        -------
            Aucun
        """
        self.display_image(chemin_fichier, position_x, position_y)

    def display_detected_card(self, detected_card: MatLike, position_x: int, position_y: int):
        """
        Displays the detected card on the window at the specified position.

        Args:
        -----
            detected_card (MatLike): The image of the detected card.
            position_x (int): The x-coordinate of the position where the card should be displayed.
            position_y (int): The y-coordinate of the position where the card should be displayed.

        Returns:
        --------
            None
        """
        self.__display_image(detected_card, position_x, position_y)
    
    def afficher_carte_detectee(self, carte_detectee: MatLike, position_x: int, position_y: int) :
        """
        Affiche la carte détectée dans la fenêtre à la position spécifiée.

        Paramètres:
        -----------
            carte_detectee (MatLike): L'image de la carte détectée.
            position_x (int): La coordonnée x de la position où la carte doit être affichée.
            position_y (int): La coordonnée y de la position où la carte doit être affichée.

        Retour:
        --------
            Aucun
        """
        self.display_detected_card(carte_detectee, position_x, position_y)
    
    def create_button(self, width: int, height: int, position_x: int, position_y: int, color: Couleur) -> Button:
        """
        Create a button with the specified width, height, position, and color.

        Args:
        -----
            width (int): The width of the button.
            height (int): The height of the button.
            position_x (int): The x-coordinate of the button's up-left corner.
            position_y (int): The y-coordinate of the button's up-left corner.
            color (Couleur): The color of the button.

        Returns:
        --------
            Button: The created button.
        """
        try:
            return self.__create_button(width, height, position_x, position_y, color)
        except AttributeError:
            self.__error_message("the window hasn't been opened.", "en")
    
    def creer_bouton(self, longueur: int, hauteur: int, position_x: int, position_y: int, couleur: Couleur) -> Button :
        """
        Crée un bouton avec la largeur, la hauteur, la position et la couleur spécifiées.

        Paramètres:
        -----------
            longueur (int): La largeur du bouton.
            hauteur (int): La hauteur du bouton.
            position_x (int): La coordonnée x du coin supérieur gauche du bouton.
            position_y (int): La coordonnée y du coin supérieur gauche du bouton.
            couleur (Couleur): La couleur du bouton.

        Retour:
        -------
            Button: Le bouton créé.
        """
        try:
            return self.__create_button(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")
        
    def create_text_area(self, width: int, height: int, position_x: int, position_y: int, color: Couleur) :
        """
        Create a text area with the specified width, height, position, and color.

        Args:
        -----
            width (int): The width of the text area.
            height (int): The height of the text area.
            position_x (int): The x-coordinate of the text area's up-left corner.
            position_y (int): The y-coordinate of the text area's up-left corner.
            color (Couleur): The color of the text area.

        Returns:
        --------
            The created text area.
        """
        try:
            return self.__interface.create_text_area(width, height, position_x, position_y, color)
        except AttributeError:
            self.__error_message("the window hasn't been opened.", "en")
    
    def creer_zone_texte(self, longueur: int, hauteur: int, position_x: int, position_y: int, couleur: Couleur) :
        """
        Crée une zone de texte avec la largeur, la hauteur, la position et la couleur spécifiées.

        Paramètres:
        -----------
            longueur (int): La largeur de la zone de texte.
            hauteur (int): La hauteur de la zone de texte.
            position_x (int): La coordonnée x du coin supérieur gauche de la zone de texte.
            position_y (int): La coordonnée y du coin supérieur gauche de la zone de texte.
            couleur (Couleur): La couleur de la zone de texte.

        Retour:
        -------
            La zone de texte créée.
        """
        try:
            return self.create_text_area(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")
    
    def get_emotion_image(self, emotion: str) -> str:
        """
        Returns the image associated with the given emotion.

        If the given emotion is not found in the emotion dictionary,
        the function returns the path to the neutral image.

        Args:
        -----
            emotion (str): The emotion for which to retrieve the image.

        Returns:
        --------
            str: The path to the image associated with the given emotion.
        """
        if not emotion in list(self.__emotion_dict.keys()):
            return  self.__emotion_dict["Neutre"]
        return self.__emotion_dict[emotion]

    def obtenir_image_emotion(self, emotion : str) -> str:
        """
        Renvoie l'image associée à l'émotion donnée.

        Si l'émotion donnée n'est pas trouvée dans le dictionnaire des émotions,
        la fonction renvoie le chemin de l'image neutre.

        Paramètres:
        -----------
            emotion (str): L'émotion pour laquelle récupérer l'image.

        Retour:
        -------
            str: Le chemin de l'image associée à l'émotion donnée.
        """
        return self.get_emotion_image(emotion)

    ### Private Methode ###
            
    def _stop(self) :
        pg.quit()
    
    def _get_surface(self) -> pg.Surface | None :
        return self.__surface

    def __change_background_color(self, R, G, B) :
            self.__background_color = (R, G, B)

    def __error_message(self, msg: str, lang: str = "fr") :
        if (lang.lower() == "fr") :
            print(f"\033[91mErreur: {msg}\033[00m", file=sys.stderr)
        elif (lang.lower() == "en") :
            print(f"\033[91mError: {msg}\033[00m", file=sys.stderr)
    
    def __getWidth(self) :
        return self.__surface.get_width()

    def __getHeight(self) :
        return self.__surface.get_height()

    def __draw_rect(self, w, h, x, y, c) :
        rect = pg.Rect(x, y, w, h)
        pg.draw.rect(self.__surface, c, rect)
    
    def __create_button(self, w, h, x, y, c) :
        return self.__interface.create_button(w, h, x, y, c)
    
    def __draw_background(self) :
        self.__surface.fill(self.__background_color)
        pg.display.update()
    
    def __change_window_title(self, title: str) :
            self.__title = title
            self.__change_title = True

    def __draw_text(self, txt, x, y, s, c) :
        font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", s)
        surf = font.render(txt, True, c)
        self.__surface.blit(surf, (x, y))
    
    def __display_image(self, img: MatLike, x, y) :
        try:
            if img is None:
                self.__draw_rect(200, 200, x, y, self.__background_color)
            else:
                self.__surface.blit(img, (x, y))
        except:
            pass
    
    def __check_flags(self) :
        if self.__toggle_in_fullscreen:
            pg.display.set_mode((self.__getWidth(), self.__getHeight()), pg.FULLSCREEN | pg.SCALED)
            self.__toggle_in_fullscreen = False
            self.__is_fullscreen = True
        elif self.__toggle_out_fullscreen:
            pg.display.set_mode((self.__getWidth(), self.__getHeight()))
            self.__toggle_out_fullscreen = False
            self.__is_fullscreen = False
        if self.__change_title:
            pg.display.set_caption(self.__title)

# class Fenetre:
#     def __init__(self, robot, debug=False):
#         self.debug = debug
#         self.__title = "Pybot"
#         self.__is_fullscreen = False
#         # main surface
#         self.__surface = None
#         # objects
#         self.robot = robot
#         self.__interface = None
#         # update flags
#         self.__toggle_in_fullscreen = False
#         self.__toggle_out_fullscreen = False
#         self.__change_title = False
#         # theming colors data
#         self.__background_color = (0, 0, 0)
#         # clock and fps
#         self.__color = pg.time.Clock()
#         self.__fps = 30
#         # filters
#         self.__filters = None

#     def run(self, width, height):
#         pg.init()
#         self.__surface = pg.display.set_mode((width, height))
#         pg.display.set_caption(self.__title)
#         self.__interface = Interface(self.__surface)
#         self.__filters = Filtres()
#         return self

#     def getWidth(self): 
#         return self.__surface.get_width()

#     def getHeight(self):
#         return self.__surface.get_height()

#     def change_background_color(self, R, G, B):
#         self.__background_color = (R, G, B)

#     def stop(self):
#         pg.quit()

#     def update_fullscreen(self, change):
#         if change == self.__is_fullscreen:
#             return
#         if change:
#             self.__toggle_in_fullscreen = True
#         else:
#             self.__toggle_out_fullscreen = True
    

#     def update_title(self, title):
#         self.__title = title
#         self.__change_title = True
    

#     def check_flags(self):
#         if self.__toggle_in_fullscreen:
#             pg.display.set_mode((self.getWidth(), self.getHeight()), pg.FULLSCREEN | pg.SCALED)
#             self.__toggle_in_fullscreen = False
#             self.__is_fullscreen = True
#         elif self.__toggle_out_fullscreen:
#             pg.display.set_mode((self.getWidth(), self.getHeight()))
#             self.__toggle_out_fullscreen = False
#             self.__is_fullscreen = False
#         if self.__change_title:
#             pg.display.set_caption(self.__title)

#     def render(self):
#         try:
#             self.check_flags()
#             self.__color.tick(self.__fps)
#             pg.display.update()
#         except:
#             pass
            
    # def __draw_rect(self, w, h, x, y, c):
    #     rect = pg.Rect(x, y, w, h)
    #     pg.draw.rect(self.__surface, c, rect)
    

#     def draw_background(self): TO ADD
#         self.__surface.fill(self.__background_color)
#         pg.display.update()
    

#     def draw_rect(self, w, h, x, y, c):
#         rect = pg.Rect(x, y, w, h)
#         pg.draw.rect(self.__surface, c, rect)
    

#     def draw_text(self, txt, x, y, s, c):
#         font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", s)
#         surf = font.render(txt, True, c)
#         self.__surface.blit(surf, (x, y))


#     def create_button(self, w, h, x, y, c):
#         return self.__interface.create_button(w, h, x, y, c)

#     def create_text_area(self, w, h, x, y, c):
#         return self.__interface.create_text_area(w, h, x, y, c)

#     def display_camera(self, x, y):
#         self.camera.display(x, y)
    
#     def capture_photo(self, file_name):
#         self.camera.capture(file_name)
    
#     def display_image_from_path(self, file_path, x, y):
#         try:
#             img = pg.image.load(os.getcwd() + file_path)
#             self.__surface.blit(img, (x, y))
#         except:
#             pass

#     def display_image(self, img: MatLike, x, y):
#         try:
#             if img is None:
#                 self.__draw_rect(200, 200, x, y, self.__background_color)
#             else:
#                 self.__surface.blit(img, (x, y))
#         except:
#             pass

#     def set_filter(self, file_path, filter_name):
#         self.__filters.apply(file_path, filter_name)