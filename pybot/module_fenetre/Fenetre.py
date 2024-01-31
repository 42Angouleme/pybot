from .Interface import Interface
from cv2.typing import MatLike
from .Interface import Button
from ..types import Couleur
import pygame as pg
import os, sys


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'  # need to be declared before to import pygame

class Fenetre:
    def __init__(self):
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
    
    # run ??
    def open_window(self, width: int = 800, height: int = 600) :
        """
        """
        # Try to move pg.init and self_surface in __init__
        pg.init()
        self.__surface = pg.display.set_mode((width, height))
        pg.display.set_caption(self.__title)
        self.__interface = Interface(self.__surface)
        
    def ouvrir_fenetre(self, longueur: int = 800, hauteur: int = 600):
        """
            Créé une fenêtre avec une longueur et une hauteur passées en argument (en nombre de pixels). \n
            Si un argument n'est pas donné, la longueur par défaut sera 800 pixels et la hauteur par défaut sera 600 pixels.
        """
        self.open_window(longueur, hauteur)
    
    def __change_background_color(self, R, G, B) :
            self.__background_color = (R, G, B)

    def change_background_color(self, color : Couleur) :
        try :
            self.__change_background_color(color[0], color[1], color[2])
        except AttributeError :
            self.__error_message("the window hasn't been opened.", "en")
    
    def changer_couleur_fond(self, couleur: Couleur) :
        r"""
            Change la couleur du fond d'écran. \n
            La couleur passée en paramètre doit être au format: (R, G, B). \n
            R, G et B sont des nombres entre 0 et 255.
        """
        try :
            self.__change_background_color(couleur[0], couleur[1], couleur[2])
        except AttributeError :
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")

    def full_screen(self, change: bool):
        """
        """
        if change == self.__is_fullscreen:
            return
        if change:
            self.__toggle_in_fullscreen = True
        else:
            self.__toggle_out_fullscreen = True
    
    def plein_ecran(self, changer: bool):
        """
            Passer la fenêtre en plein écran (changer=True) ou en sortir (changer=False).
        """
        self.full_screen(changer)
    
    def change_window_title(self, title: str):
        """
        """
        try:
            self.__change_title(title)
        except AttributeError:
            self.__error_message("title must defined after the window.", "en")
    
    def changer_titre_fenetre(self, titre: str):
        """
        """
        try:
            self.__change_window_title(titre)
        except AttributeError:
            self.__error_message("le titre doit être défini après création de la fenêtre.", "fr")

    def refresh_display(self):
        try:
            self.__check_flags()
            self.__color.tick(self.__fps)
            pg.display.update()
        except:
            pass

    def actualiser_affichage(self):
        """
            Fonction nécessaire dans une boucle pour mettre à jour l'affichage de la fenêtre.
        """
        self.refresh_display()

    def display_background(self):
        r"""
        """
        try:
            self.__draw_background()
        except AttributeError:
            self.__error_message("the window hasn't been opened.", "en")
            
    def afficher_fond(self):
        r"""
            Affiche le fond d'écran avec la dernière couleur enregistrée par la fonction couleur_fond() \n
            (par défaut, la couleur est : noir).
        """
        try:
            self.__draw_background()
        except AttributeError:
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")
    
    def draw_rectangle(self, width: int, height: int, position_x: int, position_y: int, color: Couleur):
        r"""
            Dessine un rectangle dans la fenêtre. \n

            Les paramètres attendus sont : \n
                * la longueur et la hauteur du rectangle. \n
                * la position x et y du rectangle (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la couleur du rectangle.
        """
        try:
            self.__draw_rect(width, height, position_x, position_y, color)
        except AttributeError:
            self.__error_message("the window hasn't been opened.", "en")
    
    def dessiner_rectangle(self, longueur: int, hauteur: int, position_x: int, position_y: int, couleur: Couleur):
        r"""
        """
        try:
            self.__draw_rect(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")
    
    def display_text(self, text, position_x: int = 0, position_y: int = 0, size: int = 16, color: Couleur = (0, 0, 0)):
        r"""
        """

        try:
            self.__draw_text(text, position_x, position_y, size, color)
        except AttributeError:
            self.__error_message("the window hasn't been opened.", "en")
    
    def afficher_texte(self, texte, position_x: int = 0, position_y: int = 0, taille: int = 16, couleur: Couleur = (0, 0, 0)):
        r"""
            Affiche un texte dans la fenêtre. \n

            Les paramètres attendus sont : \n
                * le texte à afficher. \n
                * la position x et y du texte (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la taille du texte. \n
                * la couleur du texte.
        """
        try:
            self.__draw_text(texte, position_x, position_y, taille, couleur)
        except AttributeError:
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")
    
    def display_image(self, file_path: str, position_x: int, position_y: int):
        r"""
        """
        try:
            img = pg.image.load(os.getcwd() + file_path)
            self.__surface.blit(img, (position_x, position_y))
        except:
            pass

    def afficher_image(self, chemin_fichier: str, position_x: int, position_y: int):
        r"""
            Afficher une image. \n
            Les paramètres attendus sont : \n
                * Le chemin et nom du fichier. (ex: /images/photo.jpg) \n
                * Les coordonnées x et y où sera affichée l'image.
        """
        self.display_image(chemin_fichier, position_x, position_y)

    def display_detected_card(self, dectected_card: MatLike, position_x: int, position_y: int):   
        r"""
        """
        self.__display_image(dectected_card, position_x, position_y)

    def afficher_carte_detectee(self, carte_detectee: MatLike, position_x: int, position_y: int):
        r"""
            Afficher la carte détectée. \n
            Les paramètres attendus sont : \n
                * L'image de la carte detectée par Robot.detecter_carte() \n
                * Les coordonnées x et y où sera affichée l'image.
        """
        self.display_detected_card(carte_detectee, position_x, position_y)
    
    def create_bouton(self, width: int, height: int, position_x: int, position_y: int, color: Couleur) -> Button:
        """
        """
        try:
            return self.__create_button(width, height, position_x, position_y, color)
        except AttributeError:
            self.__error_message("the window hasn't been opened.", "en")
    
    def creer_bouton(self, longueur: int, hauteur: int, position_x: int, position_y: int, couleur: Couleur) -> Button:
        r"""
            Crée et retourne un bouton qui peut être affiché et vérifié plus tard. \n
            Les paramètres attendus sont : \n
                * la longueur et la hauteur du bouton. \n
                * la position x et y du bouton (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la couleur du bouton.
        """
        try:
            return self.__create_button(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")
        
    def create_text_area(self, width: int, height: int, position_x: int, position_y: int, color: Couleur):
        r"""
        """
        try:
            return self.__interface.create_text_area(width, height, position_x, position_y, color)
        except AttributeError:
            self.__error_message("the window hasn't been opened.", "en")
    
    def creer_zone_texte(self, longueur: int, hauteur: int, position_x: int, position_y: int, couleur: Couleur):
        r"""
            Créer et retourner une zone de texte qui peut être affichée et vérifiée plus tard. \n
            Cela est utile pour récupérer les entrées utilisateur \n
            Les paramètres attendus sont : \n
                * la longueur et la hauteur du bouton. \n
                * la position x et y du bouton (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la couleur du bouton.
        """
        try:
            return self.create_text_area(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.__error_message("la fenêtre n'a pas été ouverte.", "fr")

    ### Private Methode ###
            
    def _stop(self):
        pg.quit()
    
    def _get_surface(self) -> pg.Surface | None :
        return self.__surface

    def __error_message(self, msg: str, lang: str = "fr"):
        if (lang.lower() == "fr") :
            print(f"\033[91mErreur: {msg}\033[00m", file=sys.stderr)
        elif (lang.lower() == "en") :
            print(f"\033[91mError: {msg}\033[00m", file=sys.stderr)
    
    def __getWidth(self):
        return self.__surface.get_width()

    def __getHeight(self):
        return self.__surface.get_height()

    def __draw_rect(self, w, h, x, y, c):
        rect = pg.Rect(x, y, w, h)
        pg.draw.rect(self.__surface, c, rect)
    
    def __create_button(self, w, h, x, y, c):
        return self.__interface.create_button(w, h, x, y, c)
    
    def __draw_background(self):
        self.__surface.fill(self.__background_color)
        pg.display.update()
    
    def __change_window_title(self, title: str):
            self.__title = title
            self.__change_title = True

    def __draw_text(self, txt, x, y, s, c):
        font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", s)
        surf = font.render(txt, True, c)
        self.__surface.blit(surf, (x, y))
    
    def __display_image(self, img: MatLike, x, y):
        try:
            if img is None:
                self.__draw_rect(200, 200, x, y, self.__background_color)
            else:
                self.__surface.blit(img, (x, y))
        except:
            pass
    
    def __check_flags(self):
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