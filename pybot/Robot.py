from .module_fenetre.Fenetre import Fenetre
from .module_user.User import User_manager
from .module_camera.Camera import Camera
from .module_fenetre.Input import Input
from .module_webapp import create_app
from .module_ia.IA import ChatBot
from flask import Flask
import os, sys
import time

# Typing
from typing import List
from .AttributeDict import AttributeDict


class Robot:
    def __init__(self):

        # English Module #
        self.AI : ChatBot = None
        self.camera : Camera = None
        self.window : Fenetre = None
        self.user : User_manager = None

        # Module Francais#
        self.IA : ChatBot = self.AI
        self.fenetre : Fenetre = self.window
        self.utilisateur : User_manager = self.user

        # Robot Attributs #
        self.events = []
        self.__active : bool = True
        self.__webapp : Flask = None
        self._isWriting : bool = False

        self.__emotion_dict : dict[str, str] = {
            "Neutre" : "/images/emotions/neutre.png",
            "Amuser" : "/images/emotions/amuser.png",
            "Celebration" : "/images/emotions/celebration.png",
            "Colere" : "/images/emotions/colere.png",
            "Contrariete" : "/images/emotions/contrariete.png",
            "Degout" : "/images/emotions/degout.png",
            "Fatigue" : "/images/emotions/fatigue.png",
            "Incomprehension" : "/images/emotions/incomprehension.png",
            "Inquietude" : "/images/emotions/inquietude.png",
            "Joie" : "/images/emotions/joie.png",
            "Peur" : "/images/emotions/peur.png",
            "Reflexion" : "/images/emotions/reflexion.png",
            "Soulagement" : "/images/emotions/soulagement.png",
            "Surprise" : "/images/emotions/surprise.png",
            "Tristesse" : "/images/emotions/tristesse.png",
        }

        self.attributs : AttributeDict = AttributeDict({"boutons": AttributeDict(), "zones_de_texte": AttributeDict()})

    def start_window_module(self) :
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
        if (self.window is not None) :
            self.__error_message("Window module has already been started.", "en")
            return
        if (self.__webapp is None) :
            self.__warning_message("Webapp should be start before the window module.", "en")
        self.window = Fenetre(self.__emotion_dict)
        self.fenetre = self.window

    def demarrer_module_fenetre(self) :
        """
        Démarre le module fenêtre avec la longueur et la largeur spécifiées.

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
        if (self.window is not None) :
            self.__error_message("Le module fenêtre est déjà démarré.", "fr")
            return
        if (self.__webapp is None) :
            self.__warning_message("L'application web doit être lancée avant de créer la fenêtre.", "fr")
        self.start_window_module()
    
    def start_AI_module(self) :
        """
        Starts the AI module.

        This method initializes the AI module if it has not already been started.
        
        Note that the environment variables OPENAI_API_KEY and OPENAI_API_ORG_ID must be set before starting the AI module.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        if (self.AI is not None) :
            self.__error_message("AI module has already been started.", "en")
            return
        try :
            self.AI = ChatBot(list(self.__emotion_dict.keys()))
            self.IA = self.AI
        except :
            self.__warning_message("Please add OPENAI_API_KEY and OPENAI_API_ORG_ID to the environment before starting the AI module", "en")
    
    def demarrer_module_IA(self) :
        """
        Démarre le module IA.

        Cette méthode initialise le module IA si ce n'est pas déjà fait.
        
        Notez que les variables d'environnement OPENAI_API_KEY et OPENAI_API_ORG_ID doivent être définies avant de démarrer le module IA.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        if (self.AI is not None) :
            self.__error_message("Le module IA est déjà démarré.", "fr")
            return
        self.start_AI_module()
    
    def start_camera_module(self):
        """
        Starts the camera module.

        This method initializes the camera module if it has not already been started.
        Note that the window module must be started before this module.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        if (self.window is None or self.fenetre._get_surface() is None) :
            self.__warning_message("Window module must be started and the window must be opened before this module.", "en")
            return
        if (self.camera is not None) :
            self.__error_message("Camera module has already been started.", "en")
        self.camera = Camera(self.fenetre._get_surface())

    def demarrer_module_camera(self) :
        """
        Démarre le module caméra.

        Cette méthode initialise le module caméra s'il n'a pas déjà été démarré.
        Notez que le module fenêtre doit être démarré avant ce module.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        if (self.window is None) :
            self.__warning_message("Le module fenêtre doit être démarré et la fenêtre ouverte avant ce module.", "fr")
            return
        if (self.camera is not None) :
            self.__error_message("Le module caméra est déjà démarré.", "fr")
        self.start_camera_module()
    
    def start_user_module(self):
        """
        Starts the user module.

        Note that the webapp and the camerea module must be started before this module.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        if (self.__webapp is None):
            self.__warning_message("Webapp must be started before this module.", "en")
            return
        if (self.camera is None):
            self.__warning_message("Camera module must be started before this module.", "en")
            return
        if (self.user is not None) :
            self.__error_message("User module has already been started.", "en")
        self.camera._updateUserCardsTracker(self.__webapp)
        self.user = User_manager(self.__webapp, self.camera)
        self.utilisateur = self.user

    def demarrer_module_utilisateur(self) :
        """
        Démarre le module utilisateur.

        Notez que l'application web et le module caméra doivent être démarrés avant ce module.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        if (self.__webapp is None) :
            self.__warning_message("L'application web doit être lancée avant ce module.", "fr")
            return
        if (self.camera is None) :
            self.__warning_message("Le module caméra doit être démarré avant ce module.", "fr")
            return
        if (self.user is not None) :
            self.__error_message("Le module utilisateur est déjà démarré.", "fr")
        self.start_user_module()

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
        self.__webapp = create_app(root_dir=os.path.dirname(os.path.abspath(__file__)))
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
    
    def sleep(self, secondes: int) :
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

    def dort(self, secondes: int) :
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

    def is_active(self) -> bool :
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
    
    def est_actif(self) -> bool :
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
        if new not in self.events:
            self.events.append(new)

    def ajouter_evenement(self, touche: str, nom: str) :
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
        for e in self.events:
            if e[1] == name:
                self.events.remove(e)

    def supprimer_evenement(self, nom: str) :
        """
        Supprime les évènements ayant le nom donné de la liste des évènements.

        Paramètres:
            nom (str): Le nom des évènements à supprimer.

        Retour:
        -------
            Aucun
        """
        self.delete_event(nom)
    
    def check_events(self) -> List[str] :
        """
        Check all the events and return a list of detected events.

        Args:
        -----
            None

        Returns:
        --------
            A list of strings representing the events.
        """
        return Input.check(self.events, self)

    def verifier_evenements(self) -> List[str] :
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
            if (self.camera is not None) :
                self.camera._stop()
            self.window._stop()
            self.__active = False

        except AttributeError:
            pass

    def desactiver(self) :
        """
        Désactive le robot en arrêtant la caméra et la fenêtre et définit l'attribut actif à False.
        Un robot qui a été désactivé ne pourra pas effectuer d'action.

        Paramètres:
        ------------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.deactivate()

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
