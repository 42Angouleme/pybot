from .UserCardsTracker import UserCardsTracker
from cv2.typing import MatLike
from .filtres import Filtres
from flask import Flask
import pygame as pg
import numpy as np
import cv2
import os

def verifier_systeme():
    if os.path.exists('/etc/os-release'):
        with open('/etc/os-release') as f:
            for ligne in f:
                if ligne.startswith('ID=ubuntu'):
                    return 'Ubuntu', 1
                elif ligne.startswith('ID=raspbian'):
                    return 'Raspberry Pi OS', 2
    return 'Système inconnu', 1

_ , systeme = verifier_systeme()

if systeme == 2 :
    from picamera2 import PiCamera2
    from libcamera import controls



class Camera :
    def __init__(self, surface : pg.Surface):
        self.__x : float = 0
        self.__y : float = 0
        self.__filters = Filtres()
        self.__frame : MatLike = None
        if systeme == 1 :
            self.__camera = cv2.VideoCapture(0)
        if systeme == 2 :
            self.__camera = PiCamera2()
            self.__camera.configure(self.__camera.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)}))
            self.__camera.set_control({"Afmode" : controls.AfModeEnum.Continuous})
            self.__camera.start()
        self.__surface : pg.Surface = surface
        self.__card_tracker: UserCardsTracker = None

    def display_camera(self, position_x: int = 0, position_y: int = 0) :
        """
        Display the camera in the window.

        Args:
        -----
            position_x (int): The x-coordinate of the top-left corner of the camera. Default is 0.
            position_y (int): The y-coordinate of the top-left corner of the camera. Default is 0.

        Returns:
        --------
            None
        """
        self.__x = position_x
        self.__y = position_y
        try:
            if systeme == 1 :
                ret, self.__frame = self.__camera.read()
            if systeme == 2 :
                self.__frame = self.__camera.capture_array()
            self.__frame = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2RGB)
            self.__frame = np.rot90(self.__frame)
            self.__frame = pg.surfarray.make_surface(self.__frame)
            self.__surface.blit(self.__frame, (self.__x, self.__y))
        except:
            pass

    def afficher_camera(self, position_x: int = 0, position_y: int = 0) :
        """
        Affiche la caméra dans la fenêtre.

        Paramètres:
        -----------
            position_x (int): La coordonnée x du coin supérieur gauche de la caméra. La valeur par défaut est 0.
            position_y (int): La coordonnée y du coin supérieur gauche de la caméra. La valeur par défaut est 0.

        Retour:
        -------
            Aucun
        """
        self.display_camera(position_x, position_y)
    
    def take_picture(self, file_name: str) :
        """
        Takes a picture using the camera and saves it as a JPEG file.
        It is saved in the "images" folder.

        Args:
        -----
            file_name (str): The name of the file to save the picture as.

        Returns:
        --------
            None
        """
        try:
            if systeme == 1 :
                ret, frame = self.__camera.read()
                if not ret:
                    return None
            if systeme == 2 :
                frame = self.__camera.capture_array()
            frame = cv2.flip(frame, 1)
            cv2.imwrite("images/" + file_name + ".jpg", frame)
        except:
            pass

    def prendre_photo(self, nom_fichier: str) :
        """
        Prend une photo en utilisant la caméra et l'enregistre en tant que fichier JPEG.
        Elle est enregistrée dans le dossier "images".

        Paramètres:
        -----------
            nom_fichier (str): Le nom du fichier pour enregistrer la photo.

        Retour:
        -------
            Aucun
        """
        self.take_picture(nom_fichier)
    
    def apply_filter(self, file_path: str, filter_name: str):
        """
        Apply a filter to the given photo.
        See documentation for the complete list of filters: https://42angouleme.github.io/ref/

        Args:
        -----
            file_path (str): The path to the file to apply the filter to.
            filter_name (str): The name of the filter to apply.

        Returns:
        --------
            None
        """
        self.__filters.apply(file_path, filter_name)
    
    def appliquer_filtre(self, chemin_fichier: str, nom_filtre: str) :
        """
        Applique un filtre a la photo donnée.
        Consultez la documentation pour la liste complète des filtres : https://42angouleme.github.io/ref/

        Paramètres:
        -----------
            chemin_fichier (str): Le chemin vers le fichier auquel appliquer le filtre.
            nom_filtre (str): Le nom du filtre à appliquer.

        Retour:
        -------
            Aucun
        """
        self.apply_filter(chemin_fichier, nom_filtre)
    
    ### Private Methode ###

    def _stop(self) :
        if systeme == 1 :
            self.__camera.release()
        if systeme == 2 :
            self.__camera.close()
        cv2.destroyAllWindows()
    
    def _is_open(self) -> bool :
        if systeme == 1 :
            return self.__camera.isOpened()
        if systeme == 2 :
            return True

    def _detect_user(self, min_threshold : float, stop_threshold : float):
        """
        Detect user and if user found, the card is detected and framed in the frame

        Params
            - min_threshold: Sufficient threshold to interpret frame as similar card
            - stop_threshold: Threshold to interpret frame as corresponding card
        Returns
            - matching_user: User that matches the most for detected card
        """
        # Handle first launch of camera with 0 frame
        if self.__frame is None:
            return [], []
        frame, user_detected = self.__card_tracker.get_detected_user(
                self.__frame,
                min_threshold,
                stop_threshold)
        if user_detected is not None:
            self.__surface.blit(frame, (self.__x, self.__y))
        return user_detected, frame

    def _detect_card(self, min_threshold: float, stop_threshold: float):
        """
        Detect user and if user found, the card is detected and framed in the frame

        Params
            - min_threshold: Sufficient threshold to interpret frame as similar card
            - stop_threshold: Threshold to interpret frame as corresponding card
        Returns
            - detected_card: card detected by algorithm and does not match any
                user's card
        """
        # Handle first launch of camera with 0 frame
        if self.__frame is None:
            return None
        frame, detected_card = self.__card_tracker.get_detected_card(
                self.__frame,
                min_threshold,
                stop_threshold)
        if detected_card is not None:
            self.__surface.blit(frame, (self.__x, self.__y))
        return detected_card

    def _updateUserCardsTracker(self, webapp: Flask):
        # Handle Unintialized webapp
        if not isinstance(webapp, Flask):
            raise ValueError
        self.__card_tracker = UserCardsTracker(webapp)
