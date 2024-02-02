from ..module_webapp.models.user import UserResponse
from ..module_camera.Camera import Camera
from cv2.typing import MatLike
from dotenv import load_dotenv
from pathlib import Path
from ..types import User
from flask import Flask
import pygame as pg
import requests
import os, sys

class User_manager:
    def __init__(self, webapp : Flask, camera : Camera) :
        """
        """
        self.__webapp : Flask = webapp
        self.__camera: Camera = camera
        self.__user_logged_in : UserResponse | None = None
        self.__load_env_file(".env_to_rename")

    def logging(self, minimum_threshold: float = 0.75, search_stop_threshold: float = 0.85) :
        """
        Logs in a user if a recognized user is found.
        Draw a square around the recognized user's card.
        
        Args:
        -----
            minimum_threshold (float): The minimum confidence threshold for user recognition. Defaults to 0.75.
            search_stop_threshold (float): The confidence threshold at which the search for a user stops. Defaults to 0.85.
        
        Returns:
        --------
            None
        """
        if not self.__camera._is_open():
            return
        recognized_user = self.__connect_user(minimum_threshold, search_stop_threshold)

        if recognized_user and self.check_session():
            self.__warning_message("A user is already logged in.", "en")
        elif recognized_user:
            self.__user_logged_in = recognized_user
        

    def connecter(self, seuil_minimal: float = 0.75, seuil_arret_recherche: float = 0.85) :
        """
        Connecte un utilisateur si un utilisateur reconnu est trouvé.
        Dessine un carré autour de la carte de l'utilisateur reconnu.
        
        Paramètres:
        -----------
            seuil_minimal (float): Le seuil de confiance minimum pour la reconnaissance de l'utilisateur. Par défaut à 0.75.
            seuil_arret_recherche (float): Le seuil de confiance à partir duquel la recherche d'un utilisateur s'arrête. Par défaut à 0.85.
        
        Retour:
        -------
            Aucun
        """
        if not self.__camera._is_open():
            return
        recognized_user = self.__connect_user(seuil_minimal, seuil_arret_recherche)

        if recognized_user and self.check_session():
            self.__warning_message("Un utilisateur est déjà connecté.", "fr")
        elif recognized_user:
            self.__user_logged_in = recognized_user


    def detect_card(self, minimum_threshold: float = 0.75, search_stop_threshold: float = 0.85) -> MatLike :
        """
        Detects a card using the camera.

        Args:
        -----
            minimum_threshold (float): The minimum threshold for card detection. Defaults to 0.75.
            search_stop_threshold (float): The threshold at which the search for a card should stop. Defaults to 0.85.

        Returns:
        --------
            MatLike: The detected card image, or None if the camera is not open.
        """
        if not self.__camera._is_open():
            return None
        carte_reconnue, _ = self.__camera._detect_card(minimum_threshold,
                                                    search_stop_threshold)
        return carte_reconnue

    def detecter_carte(self, seuil_minimal: float = 0.75, seuil_arret_recherche: float = 0.85) -> MatLike :
        """
        Détecte une carte en utilisant la caméra.

        Paramètres:
        -----------
            seuil_minimal (float): Le seuil minimum pour la détection de la carte. Par défaut, 0.75.
            seuil_arret_recherche (float): Le seuil à partir duquel la recherche de la carte doit s'arrêter. Par défaut, 0.85.

        Retour:
        -------
            MatLike: L'image de la carte détectée, ou None si la caméra n'est pas ouverte.
        """
        return self.detect_card(seuil_minimal, seuil_arret_recherche)

    def disconnect(self) :
        """
        Disconnects the user from the current session.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        self.__user_logged_in = None

    def deconnecter(self) :
        """
        Déconnecte l'utilisateur de la session en cours.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.disconnect()

    def check_session(self) -> bool :
        """
        Check if a user session is active.

        Args:
        -----
            None

        Returns:
        --------
            bool: True if a user session is active, False otherwise.
        """
        return self.__user_logged_in is not None

    def verifier_session(self) -> bool :
        """
        Vérifie si une session utilisateur est active.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            bool: True si une session utilisateur est active, False sinon.
        """
        return self.check_session()

    def get_logged_in_user(self) -> User :
        """
        Get the logged-in user.

        Args:
        -----
            None

        Returns:
        --------
            User: The logged-in user object.
        """
        user: User = User
        user.nom = self.__user_logged_in.last_name
        user.prenom = self.__user_logged_in.first_name
        user.carte = None
        return user

    def obtenir_utilisateur_connecte(self) -> User :
        """
        Récupère l'utilisateur connecté.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            User: L'utilisateur connecté sous forme d'un objet.
        """
        return self.get_logged_in_user()

    def create_user(self, first_name: str, last_name: str, carte: MatLike) :
        """
        Create a new user with the given first name, last name, and card image.

        Args:
        -----
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            carte (MatLike): The card image linked to the user.

        Returns:
        --------
            None
        """
        if self.verifier_session():
            self.__warning_message("A user is already logged in.", "en")
            return
        elif carte is None:
            self.__warning_message("Creation of an user with an invalid card (=None)")
            return
        pg.image.save(carte, ".tmp_card.png")
        with open(".tmp_card.png", "rb") as img:
            files = {
                "picture": ("picture.png", img, "image/png"),
            }
            new_user = {
                "first_name": first_name,
                "last_name": last_name,
            }
            os.unlink(".tmp_card.png")
            try:
                response = requests.post(
                    f"{APP_BASE_URL}/api/users", data=new_user, files=files
                )
                if response.status_code != 201:
                    self.__error_message("[HTTP ERROR]" + str(response.content), "en")
                else:
                    print("Success")
                    # Update les cartes des sessions chargées lors
                    #   de la construction de CardsTracker
                    self.__camera._updateUserCardsTracker(self.__webapp)
            except Exception as e:
                self.__error_message("[HTTP EXCEPTION]" + str(e), "en")

    def creer_utilisateur(self, prenom: str, nom: str, carte: MatLike) :
        """
        Crée un nouvel utilisateur avec le prénom, le nom et l'image de la carte donnés.

        Paramètres:
        -----------
            prenom (str): Le prénom de l'utilisateur.
            nom (str): Le nom de famille de l'utilisateur.
            carte (MatLike): L'image de la carte liée à l'utilisateur.

        Retour:
        -------
            Aucun
        """
        if self.verifier_session():
            self.__warning_message("Un utilisateur est déjà connecté")
            return
        elif carte is None:
            self.__warning_message("Création d'un utilisateur avec une carte invalide (=None)")
            return
        self.create_user(prenom, nom, carte)

    def delete_user(self):
            """
            Deletes the current user.

            Args:
            -----
                None

            Returns:
            --------
                None
            """
            if not self.verifier_session():
                self.__warning_message("No user is logged in")
                return
            try:
                id = self.__user_logged_in.id
                response = requests.delete(f"{APP_BASE_URL}/api/users/{id}")
                if response.status_code != 200:
                    self.__error_message("[HTTP ERROR]" + str(response.content), "en")
                else:
                    self.deconnecter()
                    # Update les cartes des sessions chargées lors
                    #   de la construction de CardsTracker
                    self.__camera._updateUserCardsTracker(self.__webapp)
            except Exception as e:
                self.__error_message("[HTTP EXCEPTION]" + str(e), "en")
    
    def supprimer_utilisateur(self) :
        """
        Supprime l'utilisateur actuel.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        if not self.verifier_session():
            self.__warning_message("Aucun utilisateur n'est connecté")
            return
        self.delete_user()
    
    ### Private Methode ###
            
    def __error_message(self, msg: str, lang: str = "fr") :
        if (lang.lower() == "fr") :
            print(f"\033[91mErreur: {msg}\033[00m", file=sys.stderr)
        elif (lang.lower() == "en") :
            print(f"\033[91mError: {msg}\033[00m", file=sys.stderr)
    
    def __warning_message(self, msg: str, lang: str = "fr"):
        if (lang.lower() == "fr") :
            print(f"\033[33mAttention: {msg}\033[00m", file=sys.stderr)
        elif (lang.lower() == "en") :
            print(f"\033[33mWarning: {msg}\033[00m", file=sys.stderr)
    
    def __connect_user(self, minimum_threshold: float = 0.75, search_stop_threshold: float = 0.85) -> UserResponse :
        recognized_user, _ = self.__camera._detect_user(minimum_threshold, search_stop_threshold)
        return recognized_user

    APP_BASE_URL, APP_ADRESS, APP_PORT = [""] * 3
    @staticmethod
    def __load_env_file(path_file: str = '.env') :
        global APP_BASE_URL, APP_ADRESS, APP_PORT
        load_dotenv(dotenv_path=Path(path_file))
        APP_BASE_URL = os.getenv('WEBAPP_BASE_URI')
        APP_ADRESS = APP_BASE_URL.split(':')[1][2:]
        APP_PORT = APP_BASE_URL.split(':')[2]