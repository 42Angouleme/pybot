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

        self.emotion_dict : dict[str, str] = {
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
            "Soulagement" : "/images/emotions/soulagment.png",
            "Surprise" : "/images/emotions/surprise.png",
            "Tristesse" : "/images/emotions/tristesse.png",
        }

        self.attributs : AttributeDict = AttributeDict({"boutons": AttributeDict()})

    def start_window_module(self) :
        """
        """
        if (self.window is not None) :
            self.__error_message("Window module has already been started.", "en")
            return
        if (self.__webapp is None) :
            self.__warning_message("Webapp should be start before the window module.", "en")
        self.window = Fenetre()
        self.fenetre = self.window

    def demarrer_module_fenetre(self) :
        """
        """
        if (self.window is not None) :
            self.__error_message("Le module fenêtre est déjà démarrer.", "fr")
            return
        if (self.__webapp is None) :
            self.__warning_message("L'application web doit être lancée avant de créer la fenêtre.", "fr")
        self.start_window_module()
    
    def start_AI_module(self) :
        """
        """
        if (self.window is not None) :
            self.__error_message("AI module has already been started.", "en")
            return
        try :
            self.AI = ChatBot()
        except :
            self.__warning_message("Please add OPENAI_API_KEY and OPENAI_API_ORG_ID to the environment before startin the AI module", "en")
    
    def demarrer_module_IA(self) :
        """
        """
        if (self.window is not None) :
            self.__error_message("Le module IA est déjà démarrer.", "fr")
            return
        self.start_AI_module()
    
    def start_camera_module(self) :
        """
        """
        if (self.window is None) :
            self.__warning_message("Window module must be start before this module.", "en")
            return
        if (self.window is not None) :
            self.__error_message("Camera module has already been started.", "en")
        self.camera = Camera(self.fenetre._get_surface())

    def demarrer_module_camera(self) :
        """
        """
        if (self.window is None) :
            self.__warning_message("Le module fenetre doit être démarrer avant ce module.", "fr")
            return
        if (self.camera is not None) :
            self.__error_message("Le module camera est déjà démarrer.", "fr")
        self.start_camera_module()
    
    def start_user_module(self) :
        """
        """
        if (self.__webapp is None) :
            self.__warning_message("Webapp must be start before this module.", "en")
            return
        if (self.camera is None) :
            self.__warning_message("Camera module must be start before this module.", "en")
            return
        if (self.user is not None) :
            self.__error_message("User module has already been started.", "en")
        self.user = User_manager(self.__webapp, self.camera)

    def demarrer_module_utilisateur(self) :
        """
        """
        if (self.__webapp is None) :
            self.__warning_message("L'application web doit être lancée avant ce module.", "fr")
            return
        if (self.camera is None) :
            self.__warning_message("Le module camera doit être démarrer avant ce module.", "fr")
            return
        if (self.user is not None) :
            self.__error_message("Le module utilisateur est déjà démarrer.", "fr")
        self.start_user_module()

    ### Robot Module Methode ###
    
    def start_webapp(self):
        """
        """
        self.__webapp = create_app(root_dir=os.path.dirname(os.path.abspath(__file__)))
        pid = os.fork()
        if pid:
            self.__webapp.run()
            sys.exit()

    def demarrer_webapp(self):
        """
            Cette méthode lance de manière non bloquante le serveur web qui s'occupe de la partie base de données.
        """
        self.start_webapp()
    
    def sleep(self, secondes: int) :
        """
        """
        time.sleep(secondes)

    def dort(self, secondes: int) :
        """
            Le programme restera en attente le nombre de secondes passé en argument.
        """
        self.sleep(secondes)

    def is_active(self) -> bool :
        """
        """
        return self.__active
    
    def est_actif(self) -> bool :
        """
            Retourne vrai (True) ou faux (False) pour savoir si le robot est toujours actif. \n
            Peut être utilisé pour vérifier la sortie d'une boucle.
        """
        return self.is_active()
    
    def make_inactive(self) :
        """
        """
        self.__active = False

    def rendre_inactif(self) :
        """
            Rend le robot inactif
        """
        self.make_inactive()
    
    ### Robot Evenements ###

    def add_events(self, key: str, name: str) :
        """
        """
        new = (key.lower(), name)
        if new not in self.events:
            self.events.append(new)

    def ajouter_evenement(self, touche: str, nom: str) :
        """
            Ajoute à la liste des évènements, un évènement et la touche liée, un évènement peut avoir plusieurs touches. \n
            Voir documentation pour la liste des touches possibles.
        """
        self.add_events(touche, nom)

    def delete_events(self, name: str) :
        """
        """
        for e in self.events:
            if e[1] == name:
                self.events.remove(e)

    def supprimer_evenement(self, nom: str) :
        """
            Supprime l'évènement passé en paramètre de la liste des évènements.
        """
        self.delete_events(nom)
    
    def check_events(self) -> List[str] :
        """
        """
        return Input.check(self.events, self)

    def verifier_evenements(self) -> List[str] :
        """
            Vérifie chaque évènement et retourne un tableau avec les évènements détectés.
        """
        return self.check_events(self)

    def deactivate(self) :
        """
        """
        try:
            self.camera._stop()
            self.fenetre._stop()
            self.actif = False 
        except AttributeError:
            pass

    def desactiver(self) :
        """
            Sert à fermer correctement la fenêtre (et la bibliothèque graphique), le robot devient inactif. \n
            Combiné avec un évènement (par exemple appuyer sur une touche ou un bouton) cette méthode peut etre utilisée pour arrêter le programme.
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
