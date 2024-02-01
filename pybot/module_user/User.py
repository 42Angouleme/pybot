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

    def logging(self, minimum_threshold: float = 0.75, search_stop_threshold: float = 0.85):
        """
        """
        if not self.__camera._is_open():
            return
        recognized_user = self.__connect_user(minimum_threshold, search_stop_threshold)

        if recognized_user and self.verifier_session():
            self.__warning_message("A user is already logged in.", "en")
        elif recognized_user:
            self.__user_logged_in = recognized_user
        

    def connecter(self, seuil_minimal: float = 0.75, seuil_arret_recherche: float = 0.85):
        """
            Affiche à l'écran un cadre autour de la carte et
            connecte l'utilisateur si reconnu.

            Paramètres:
                * seuil_minimal (défaut: 0.75) : score minimum pour
                    qu'une carte détectée soit considérée comme valide.
                * seuil_arret_recherche (défaut: 0.85) : score pour
                    qu'une carte détectée soit interprétée comme la bonne.
        """
        if not self.__camera._is_open():
            return
        recognized_user = self.__connect_user(seuil_minimal, seuil_arret_recherche)

        if recognized_user and self.verifier_session():
            self.__warning_message("Un utilisateur est déjà connecté.", "fr")
        elif recognized_user:
            self.__user_logged_in = recognized_user


    def detect_card(self, minimum_threshold: float = 0.75, search_stop_threshold: float = 0.85) -> MatLike:
        """
        """
        if not self.__camera._is_open():
            return None
        carte_reconnue, _ = self.__camera._detect_card(minimum_threshold,
                                                    search_stop_threshold)
        return carte_reconnue

    def detecter_carte(self, seuil_minimal: float = 0.75, seuil_arret_recherche: float = 0.85) -> MatLike:
        """
            Methode permettant de récupérer la carte détectée à l' écran.
            Carte qui n est pas une carte déjà enregistrée.

            Paramètres:
                * seuil_minimal (défaut: 0.75) : score minimum pour
                    qu'une carte détectée soit considérée comme valide.
                * seuil_arret_recherche (défaut: 0.85) : score pour
                    qu'une carte détectée soit interprétée comme la bonne.
        """
        return self.detect_card(seuil_minimal, seuil_arret_recherche)

    def deconnect(self) :
        """
        """
        self.__user_logged_in = None

    def deconnecter(self):
        """
            Déconnecte la personne actuellement connectée.
        """
        self.deconnect()

    def check_session(self) -> bool :
        """
        """
        return self.__user_logged_in is not None

    def verifier_session(self) -> bool :
        """
            Indique si un utilisateur est déjà connecté.

            Retourne:
                * True: Si une personne est connectée
                * False: Sinon
        """
        return self.check_session()

    def get_logged_in_user(self) -> User:
        """
            Méthode qui retourne un object contenant:
                - prenom de l'utilisateur
                - nom de l'utilisateur
        """
        utilisateur: User = User
        utilisateur.nom = self.__user_logged_in.last_name
        utilisateur.prenom = self.__user_logged_in.first_name
        utilisateur.carte = None
        return utilisateur

    def obtenir_utilisateur_connecte(self) -> User:
        """
            Méthode qui retourne un object contenant:
                - prenom de l'utilisateur
                - nom de l'utilisateur
        """
        return self.get_logged_in_user()

    def create_user(self, first_name: str, last_name: str, carte: MatLike):
        """
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

    def creer_utilisateur(self, prenom: str, nom: str, carte: MatLike):
        """
            Créer un utilisateur avec les données renseignées en paramètres

            Paramètres:
                - prenom: son prénom
                - nom: son nom de famille
                - carte: l'image de sa carte (générée avec Robot.detecter_carte())
        """
        if self.verifier_session():
            self.__warning_message("Un utilisateur est déjà connecté")
            return
        elif carte is None:
            self.__warning_message( "Création d'un utilisateur avec une carte invalide (=None)")
            return
        self.create_user(prenom, nom, carte)

    def delete_user(self):
        """
           Supprime l'utilisateur connecté.
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
    
    def supprimer_utilisateur(self):
        """
            Supprime l'utilisateur connecté.
        """
        if not self.verifier_session():
            self.__warning_message("Aucun utilisateur n'est connecté")
            return
        self.delete_user()
    
    ### Private Methode ###
            
    def __error_message(self, msg: str, lang: str = "fr"):
        if (lang.lower() == "fr") :
            print(f"\033[91mErreur: {msg}\033[00m", file=sys.stderr)
        elif (lang.lower() == "en") :
            print(f"\033[91mError: {msg}\033[00m", file=sys.stderr)
    
    def __warning_message(self, msg: str, lang: str = "fr"):
        if (lang.lower() == "fr") :
            print(f"\033[33mAttention: {msg}\033[00m", file=sys.stderr)
        elif (lang.lower() == "en") :
            print(f"\033[33mWarning: {msg}\033[00m", file=sys.stderr)
    
    def __connect_user(self, minimum_threshold: float = 0.75, search_stop_threshold: float = 0.85) -> UserResponse:
        recognized_user, _ = self.__camera._detect_user(minimum_threshold, search_stop_threshold)
        return recognized_user

    APP_BASE_URL, APP_ADRESS, APP_PORT = [""] * 3
    @staticmethod
    def load_env_file(path_file: str = '.env'):
        global APP_BASE_URL, APP_ADRESS, APP_PORT
        load_dotenv(dotenv_path=Path(path_file))
        APP_BASE_URL = os.getenv('WEBAPP_BASE_URI')
        APP_ADRESS = APP_BASE_URL.split(':')[1][2:]
        APP_PORT = APP_BASE_URL.split(':')[2]