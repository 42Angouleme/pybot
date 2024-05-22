from .module_haut_parleur.HautParleur import HautParleur
from .module_microphone.Microphone import Microphone
from .module_fenetre.Fenetre import Fenetre
from .module_user.User import User_manager
from .module_camera.Camera import Camera
from .module_fenetre.Input import Input
from .module_webapp import create_app
from .module_ia.IA import ChatBot
from dotenv import load_dotenv, find_dotenv
from flask import Flask
import os
import sys
import time

# Typing
from typing import List
from .AttributeDict import AttributeDict
from . import ensure


class Robot:
    # English Module #
    AI: ChatBot | None = None
    camera: Camera | None = None
    microphone: Microphone | None = None
    window: Fenetre | None = None
    user: User_manager | None = None
    speaker: HautParleur | None = None

    # Module Francais #
    IA: ChatBot | None = None
    fenetre: Fenetre | None = None
    utilisateur: User_manager | None = None
    haut_parleur: HautParleur | None = None

    # Robot Attributs #
    __events: list[tuple[str, str]] = []
    __active: bool = True
    __webapp: Flask | None = None
    _isWriting: bool = False

    __emotion_dict: dict[str, str] = {
        "Neutre": "/images/emotions/neutre.png",
        "Amuser": "/images/emotions/amuser.png",
        "Celebration": "/images/emotions/celebration.png",
        "Colere": "/images/emotions/colere.png",
        "Contrariete": "/images/emotions/contrariete.png",
        "Degout": "/images/emotions/degout.png",
        "Fatigue": "/images/emotions/fatigue.png",
        "Incomprehension": "/images/emotions/incomprehension.png",
        "Inquietude": "/images/emotions/inquietude.png",
        "Joie": "/images/emotions/joie.png",
        "Peur": "/images/emotions/peur.png",
        "Reflexion": "/images/emotions/reflexion.png",
        "Soulagement": "/images/emotions/soulagement.png",
        "Surprise": "/images/emotions/surprise.png",
        "Tristesse": "/images/emotions/tristesse.png",
    }

    attributs: AttributeDict = AttributeDict(
        {"boutons": AttributeDict(), "zones_de_texte": AttributeDict()})

    def __init__(self):
        self.IA: ChatBot = self.AI
        self.fenetre: Fenetre = self.window
        self.utilisateur: User_manager = self.user
        self.haut_parleur: HautParleur = self.speaker

        env_file = find_dotenv(".env")
        load_dotenv(env_file)

    @ensure.no_window('en')
    def init_window_module(self):
        """
        Start the window module with the specified width and length.

        This method initializes the window module if it has not already been started.

        Note that the webapp if you use it, must be started before the window module.

        Args:
        -----
            width (int): The width of the window.
            length (int): The length of the window.

        Returns:
        --------
            None
        """
        self.window = Fenetre(self.__emotion_dict)
        self.fenetre = self.window

    @ensure.no_window('fr')
    @ensure.warn_webapp('fr')
    def initialiser_module_fenetre(self):
        """
        Initialise le module fenêtre avec la longueur et la largeur spécifiées.

        Cette méthode initialise le module fenêtre si ce n'est pas déjà fait.

        Notez que l'application web si vous l'utilisez, doit être démarré avant le module fenêtre.

        Paramètres:
        -----------
            longueur (int): La longueur de la fenêtre.
            largeur (int): La largeur de la fenêtre.

        Retour:
        -------
            Aucun
        """
        self.init_window_module()

    @ensure.no_AI("en")
    def init_AI_module(self):
        """
        Initialize the AI module.

        This method initializes the AI module if it has not already been started.

        Note that the environment variables OPENAI_API_KEY and OPENAI_API_ORG_ID must be set before starting the AI module.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        try:
            self.AI = ChatBot(list(self.__emotion_dict.keys()))
            self.IA = self.AI
        except:
            ensure.warn(
                "Please add OPENAI_API_KEY and OPENAI_API_ORG_ID to the environment before starting the AI module", "en")

    @ensure.no_AI('fr')
    def initialiser_module_IA(self):
        """
        Initialise le module IA.

        Cette méthode initialise le module IA si ce n'est pas déjà fait.

        Notez que les variables d'environnement OPENAI_API_KEY et OPENAI_API_ORG_ID doivent être définies avant de démarrer le module IA.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.init_AI_module()

    @ensure.window('en')
    @ensure.no_camera('en')
    def init_camera_module(self):
        """
        Initialize the camera module.

        This method initializes the camera module if it has not already been started.
        Note that the window module must be started before this module.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        self.camera = Camera(self.fenetre._get_surface())

    @ensure.window('fr')
    @ensure.no_camera('fr')
    def initialiser_module_camera(self):
        """
        Initialise le module caméra.

        Cette méthode initialise le module caméra s'il n'a pas déjà été démarré.
        Notez que le module fenêtre doit être démarré avant ce module.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.init_camera_module()

    @ensure.webapp('en')
    @ensure.camera('en')
    @ensure.no_user('en')
    def init_user_module(self):
        """
        Initialize the user module.

        This method initializes the user module if it has not already been started.
        Note that the webapp and the camera module must be started before this module.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        self.camera._updateUserCardsTracker(self.__webapp)
        self.user = User_manager(self.__webapp, self.camera)
        self.utilisateur = self.user

    @ensure.webapp('fr')
    @ensure.camera('fr')
    @ensure.no_user('fr')
    def initialiser_module_utilisateur(self):
        """
        Initialise le module utilisateur.

        Cette méthode initialise le module utilisateur s'il n'a pas déjà été démarré.
        Notez que l'application web et le module caméra doivent être démarrés avant ce module.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.init_user_module()

    def init_microphone_module(self):
        """
        Initialize the microphone module.

        This method initializes the microphone module if it has not already been started.

        Parameters:
        -----------
            None

        Returns:
        --------
            None
        """
        self.microphone = Microphone()

    def initialiser_module_microphone(self):
        """
        Initialise le module microphone.

        Cette méthode initialise le module microphone s'il n'a pas déjà été démarré.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.init_microphone_module()

    def init_speaker_module(self):
        """
        Initialize the speaker module.

        This method initializes the speaker module if it has not already been started.

        Parameters:
        -----------
            None

        Returns:
        --------
            None
        """
        self.speaker = HautParleur()
        self.haut_parleur = self.speaker

    def initialiser_module_haut_parleur(self):
        """
        Initialise le module haut_parleur.

        Cette méthode initialise le module haut_parleur s'il n'a pas déjà été démarré.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.init_speaker_module()

    ### Robot Module Methode ###

    def start_webapp(self):
        """
        Starts the web application.

        This method starts the web application in a non-blocking way.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        self.__webapp = create_app(
            root_dir=os.path.dirname(os.path.abspath(__file__)))
        pid = os.fork()
        if pid:
            self.__webapp.run()
            sys.exit()

    def demarrer_webapp(self):
        """
        Démarre l'application web.

        Cette méthode démarre l'application web de manière non bloquante.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.start_webapp()

    def sleep(self, secondes: int):
        """
        Pause the execution of the robot for the specified number of seconds.

        Args:
        -----
            secondes (int): The number of seconds to sleep.

        Returns:
        --------
            None
        """
        time.sleep(secondes)

    def dort(self, secondes: int):
        """
        Met en pause l'exécution du robot pendant le nombre de secondes spécifié.

        Paramètres:
        ------------
            secondes (int): Le nombre de secondes à attendre.

        Retour:
        -------
            Aucun
        """
        self.sleep(secondes)

    def is_active(self) -> bool:
        """
        Check if the robot is active.

        Args:
        -----
            None

        Returns:
        --------
            bool: True if the robot is active, False otherwise.
        """
        return self.__active

    def est_actif(self) -> bool:
        """
        Vérifie si le robot est actif.

        Paramètres:
        ------------
            Aucun

        Retour:
        -------
            bool: True si le robot est actif, False sinon.
        """
        return self.is_active()

    ### Robot Evenements ###

    def add_event(self, key: str, name: str):
        """
        Add events to the robot events list.
        See documentation for the list of possible keys.s

        Args:
        -----
            key (str): The key of the event.
            name (str): The name of the event.

        Returns:
        --------
            None
        """
        new = (key.lower(), name)
        if new not in self.__events:
            self.__events.append(new)

    def ajouter_evenement(self, touche: str, nom: str):
        """
        Ajoute des évènements à la liste des évènements du robot.
        Voir la documentation pour la liste des touches possibles.

        Paramètres:
        ------------
            touche (str): La touche de l'évènement.
            nom (str): Le nom de l'évènement.

        Retour:
        -------
            Aucun
        """
        self.add_event(touche, nom)

    def delete_event(self, name: str):
        """
        Delete events with the given name from the list of events.

        Args:
        -----
            name (str): The name of the events to be deleted.

        Returns:
        --------
            None
        """
        for e in self.__events:
            if e[1] == name:
                self.__events.remove(e)

    def supprimer_evenement(self, nom: str):
        """
        Supprime les évènements ayant le nom donné de la liste des évènements.

        Paramètres:
        -----------
            nom (str): Le nom des évènements à supprimer.

        Retour:
        -------
            Aucun
        """
        self.delete_event(nom)

    def check_events(self) -> List[str]:
        """
        Check all the events and return a list of detected events.

        Args:
        -----
            None

        Returns:
        --------
            A list of strings representing the events.
        """
        return Input.check(self, self.__events)

    def verifier_evenements(self) -> List[str]:
        """
        Vérifie tous les évènements et renvoie une liste d'évènements détectés.

        Paramètres:
        ------------
            Aucun

        Retour:
        -------
            Une liste de chaînes de caractères représentant les évènements.
        """
        return self.check_events()

    def deactivate(self):
        """
        Deactivates the robot by stopping the camera and the window and set the active attribute to False.
        A robot that has been deactivated will not be able to perform any action.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        try:
            if (self.camera is not None):
                self.camera._stop()
            self.window._stop()
            self.__active = False

        except AttributeError:
            pass

    def desactiver(self):
        """
        Désactive le robot en arrêtant la caméra et la fenêtre et définit l'attribut actif à False.
        Un robot qui a été désactivé ne pourra plus effectuer d'action.

        Paramètres:
        ------------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.deactivate()

    ### Private Method ###

    def _get_user_entry(self, texte, text_area):
        """
            Allow to get the user_entry, use in texte_area and in fuction ecrire
        """
        letter = Input.get_user_entry(self, text_area)
        if (letter is not None):
            if letter == "\b":
                texte = texte[:-1]
            else:
                texte += letter
        return texte
