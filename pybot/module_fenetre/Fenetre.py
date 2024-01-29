from cv2.typing import MatLike
from .Interface import Interface
from .filtres import Filtres
import pygame as pg
import os, sys

# from ..types import Couleur HERE a retirer pour le passage en module

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'  # need to be declared before to import pygame

class Fenetre:
    def __init__(self, robot, debug=False):
        self.debug = debug
        self.title = "Pybot"
        self.is_fullscreen = False
        # main surface
        self.surface = None
        # objects
        self.robot = robot
        self.interface = None
        # update flags
        self.toggle_in_fullscreen = False
        self.toggle_out_fullscreen = False
        self.change_title = False
        # theming colors data
        self.background_color = (0, 0, 0)
        # clock and fps
        self.clock = pg.time.Clock()
        self.fps = 30
        # filters
        self.filters = None

    def run(self, width, height):
        pg.init()
        self.surface = pg.display.set_mode((width, height))
        pg.display.set_caption(self.title)
        self.interface = Interface(self.surface)
        self.filters = Filtres()
        return self

    def getWidth(self):
        return self.surface.get_width()

    def getHeight(self):
        return self.surface.get_height()

    def change_background_color(self, R, G, B):
        self.background_color = (R, G, B)
    
    # def couleur_fond(self, couleur: Couleur):
    #     r"""
    #         Change la couleur du fond d'écran. \n
    #         La couleur passée en paramètre doit être au format: (R, G, B). \n
    #         R, G et B sont des nombres entre 0 et 255.
    #     """
    #     try:
    #         self.background_color = (couleur[0], couleur[1], couleur[2])
    #     except AttributeError:
    #         self.message_erreur("la fenêtre n'a pas été ouverte.")

    def stop(self):
        pg.quit()

    def update_fullscreen(self, change):
        if change == self.is_fullscreen:
            return
        if change:
            self.toggle_in_fullscreen = True
        else:
            self.toggle_out_fullscreen = True
    
    # def plein_ecran(self, changer: bool):
    #     '''
    #         Passer la fenêtre en plein écran (changer=True) ou en sortir (changer=False).
    #     '''
    #     if changer == self.is_fullscreen:
    #         return
    #     if changer:
    #         self.toggle_in_fullscreen = True
    #     else:
    #         self.toggle_out_fullscreen = True

    def update_title(self, title):
        self.title = title
        self.change_title = True
    
    # def changer_titre(self, titre: str):
    #     '''
    #         Changer le titre de la fenêtre.
    #     '''
    #     try:
    #         self.title = title
    #         self.change_title = True
    #     except AttributeError:
    #         self.message_erreur("Le titre doit être défini après création de la fenêtre.")

    def check_flags(self):
        if self.toggle_in_fullscreen:
            pg.display.set_mode((self.getWidth(), self.getHeight()), pg.FULLSCREEN | pg.SCALED)
            self.toggle_in_fullscreen = False
            self.is_fullscreen = True
        elif self.toggle_out_fullscreen:
            pg.display.set_mode((self.getWidth(), self.getHeight()))
            self.toggle_out_fullscreen = False
            self.is_fullscreen = False
        if self.change_title:
            pg.display.set_caption(self.title)

    def render(self):
        try:
            self.check_flags()
            self.clock.tick(self.fps)
            pg.display.update()
        except:
            pass
    
    # def actualiser_affichage(self): Est ce que l'on change la fonction render ?? (elle est appeler à d'autre endroit dans le code)
    #     '''
    #         Fonction nécessaire dans une boucle pour mettre à jour l'affichage de la fenêtre.
    #     '''
    #     self.render()

    def draw_background(self):
        self.surface.fill(self.background_color)
        pg.display.update()
    
    # def afficher_fond(self):
    #     r"""
    #         Affiche le fond d'écran avec la dernière couleur enregistrée par la fonction couleur_fond() \n
    #         (par défaut, la couleur est : noir).
    #     """
    #     try:
    #         self.surface.fill(self.background_color)
    #         pg.display.update()
    #     except AttributeError:
    #         self.message_erreur("la fenêtre n'a pas été ouverte.")

    def draw_rect(self, w, h, x, y, c):
        rect = pg.Rect(x, y, w, h)
        pg.draw.rect(self.surface, c, rect)
    
    # def dessiner_rectangle(self, longueur: int, hauteur: int, position_x: int, position_y: int, couleur: Couleur):
    #   Est ce que l'on change la fonction draw_rect ?? (elle est appeler à d'autre endroit dans le code)
    #     r"""
    #         Dessine un rectangle dans la fenêtre. \n

    #         Les paramètres attendus sont : \n
    #             * la longueur et la hauteur du rectangle. \n
    #             * la position x et y du rectangle (son coin en haut à gauche) par rapport à la fenêtre. \n
    #             * la couleur du rectangle.
    #     """
    #     try:
    #         self.fenetre.draw_rect(longueur, hauteur, position_x, position_y, couleur)
    #     except AttributeError:
    #         self.message_erreur("la fenêtre n'a pas été ouverte.")

    def draw_text(self, txt, x, y, s, c):
        font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", s)
        surf = font.render(txt, True, c)
        self.surface.blit(surf, (x, y))

    # def afficher_texte(self, texte, position_x: int = 0, position_y: int = 0, taille: int = 16, couleur: Couleur = (0, 0, 0)):
    #     r"""
    #         Affiche un texte dans la fenêtre. \n

    #         Les paramètres attendus sont : \n
    #             * le texte à afficher. \n
    #             * la position x et y du texte (son coin en haut à gauche) par rapport à la fenêtre. \n
    #             * la taille du texte. \n
    #             * la couleur du texte.
    #     """

    #     try:
    #         font = pg.font.Font(os.getcwd() + "/pybot/assets/chicago.ttf", taille)
    #         surf = font.render(texte, True, couleur)
    #         self.surface.blit(surf, (position_x, position_y))
    #     except AttributeError:
    #         self.message_erreur("la fenêtre n'a pas été ouverte.")

    def create_button(self, w, h, x, y, c):
        return self.interface.create_button(w, h, x, y, c)

    def create_text_area(self, w, h, x, y, c):
        return self.interface.create_text_area(w, h, x, y, c)

    def display_camera(self, x, y):
        self.camera.display(x, y)
    
    def capture_photo(self, file_name):
        self.camera.capture(file_name)
    
    def display_image_from_path(self, file_path, x, y):
        try:
            img = pg.image.load(os.getcwd() + file_path)
            self.surface.blit(img, (x, y))
        except:
            pass
    
    # def afficher_image(self, chemin_fichier: str, position_x: int, position_y: int):
    #     r"""
    #         Afficher une image. \n
    #         Les paramètres attendus sont : \n
    #             * Le chemin et nom du fichier. (ex: /images/photo.jpg) \n
    #             * Les coordonnées x et y où sera affichée l'image.
    #     """
    #     try:
    #         img = pg.image.load(os.getcwd() + chemin_fichier)
    #         self.surface.blit(img, (position_x, position_y))
    #     except:
    #         pass

    def display_image(self, img: MatLike, x, y):
        try:
            if img is None:
                self.draw_rect(200, 200, x, y, self.background_color)
            else:
                self.surface.blit(img, (x, y))
        except:
            pass

    def set_filter(self, file_path, filter_name):
        self.filters.apply(file_path, filter_name)
    
    # def message_erreur(self, msg: str): HERE
    #     print(f"\033[91mErreur: {msg}\033[00m", file=sys.stderr)

