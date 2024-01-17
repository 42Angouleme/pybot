from .module_camera.Camera import Camera
from .module_fenetre import module as fenetre
from .module_fenetre.Input import Input
from .module_webapp import create_app
from .module_ia.IA import ChatBot
import pygame as pg
import io, os, sys
from pathlib import Path
import time
import requests
from dotenv import load_dotenv
# Typing
from typing import List, Dict
from cv2 import MatLike
from module_fenetre.Interface import Button

Couleur = (int, int, int)

class Robot:
    def __init__(self):
        self.load_env_file('.env_to_rename')
        self.webapp = None
        self.debug = True
        self.fenetre = None
        self.titre = "Pybot"
        self.actif = True
        self.events = []
        # camera
        self.camera = None
        # Utilisateur connecté
        self.utilisateur_connecte = None
        self.chatBot = None
        self.isWriting = False

    ### GENERAL - FENETRE ###

    def demarrer_webapp(self):
        '''
            Cette méthode lance de manière non bloquante le serveur web qui s'occupe de la partie base de données.
        '''
        self.webapp = create_app(root_dir=os.path.dirname(os.path.abspath(__file__)))
        pid = os.fork()
        if pid:
            self.webapp.run()
            sys.exit()

    def creer_fenetre(self, longueur: int = 800, hauteur: int = 600):
        '''
            Créé une fenêtre avec une longueur et une hauteur passées en argument (en nombre de pixels). \n
            Si un argument n'est pas donné, la longueur par défaut sera 800 pixels et la hauteur par défaut sera 600 pixels.
        '''
        self.fenetre = fenetre.run(self, longueur, hauteur)
        self.camera = Camera(self.fenetre.surface)
        try:
            self.camera.updateUserCardsTracker(self.webapp)
        except ValueError:
            self.message_erreur("L'application web doit être lancée avant de créer la fenêtre.")

    def changer_titre(self, titre: str):
        '''
            Changer le titre de la fenêtre.
        '''
        try:
            self.fenetre.update_title(titre)
        except AttributeError:
            self.message_erreur("Le titre doit être défini après création de la fenêtre.")

    def actualiser_affichage(self):
        '''
            Fonction nécessaire dans une boucle pour mettre à jour l'affichage de la fenêtre.
        '''
        self.fenetre.render()

    def plein_ecran(self, changer: bool):
        '''
            Passer la fenêtre en plein écran (changer=True) ou en sortir (changer=False).
        '''
        self.fenetre.update_fullscreen(changer)

    def dort(self, secondes: int):
        '''
            Le programme restera en attente le nombre de secondes passé en argument.
        '''
        time.sleep(secondes)

    def est_actif(self) -> bool:
        '''
            Retourne vrai (True) ou faux (False) pour savoir si le robot est toujours actif. \n
            Peut être utilisé pour vérifier la sortie d'une boucle.
        '''
        return self.actif

    def desactiver(self):
        '''
            Passe la variable self.actif du robot à la valeur False.
        '''
        self.actif = False

    def fermer_fenetre(self):
        '''
            Sert à fermer correctement la fenêtre (et la bibliothèque graphique), le robot devient inactif. \n
            Combiné avec un évènement (par exemple appuyer sur une touche ou un bouton) cette méthode peut etre utilisée pour arrêter le programme.
        '''
        try:
            self.camera.stop()
            self.fenetre.stop()
            self.actif = False
        except AttributeError:
            self.message_erreur("la fenêtre n'a pas été ouverte.")

    ### GENERAL - EVENEMENTS ###

    def ajouter_evenement(self, touche: str, nom: str):
        """
            Ajoute à la liste des évènements, un évènement et la touche liée, un évènement peut avoir plusieurs touches. \n
            Voir documentation pour la liste des touches possibles.
        """
        new = (touche.lower(), nom)
        if new not in self.events:
            self.events.append(new)

    def supprimer_evenement(self, nom: str):
        """
            Supprime l'évènement passé en paramètre de la liste des évènements.
        """
        for e in self.events:
            if e[1] == nom:
                self.events.remove(e)

    def verifier_evenements(self) -> List[str]:
        """
            Vérifie chaque évènement et retourne un tableau avec les évènements détectés.
        """
        return Input.check(self.events, self)

    ### INTERFACE - BOUTONS ###

    def couleur_fond(self, couleur: Couleur):
        r"""
            Change la couleur du fond d'écran. \n
            La couleur passée en paramètre doit être au format: (R, G, B). \n
            R, G et B sont des nombres entre 0 et 255.
        """
        try:
            self.fenetre.change_background_color(couleur[0], couleur[1], couleur[2])
        except AttributeError:
            self.message_erreur("la fenêtre n'a pas été ouverte.")

    def afficher_fond(self):
        r"""
            Affiche le fond d'écran avec la dernière couleur enregistrée par la fonction couleur_fond() \n
            (par défaut, la couleur est : noir).
        """
        try:
            self.fenetre.draw_background()
        except AttributeError:
            self.message_erreur("la fenêtre n'a pas été ouverte.")

    def creer_bouton(self, longueur: int, hauteur: int, position_x: int, position_y: int, couleur: Couleur) -> Button:
        """
            Crée et retourne un bouton qui peut être affiché et vérifié plus tard. \n
            Les paramètres attendus sont : \n
                * la longueur et la hauteur du bouton. \n
                * la position x et y du bouton (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la couleur du bouton.
        """
        try:
            return self.fenetre.create_button(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.message_erreur("la fenêtre n'a pas été ouverte.")

    def dessiner_rectangle(self, longueur: int, hauteur: int, position_x: int, position_y: int, couleur: Couleur):
        r"""
            Dessine un rectangle dans la fenêtre. \n

            Les paramètres attendus sont : \n
                * la longueur et la hauteur du rectangle. \n
                * la position x et y du rectangle (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la couleur du rectangle.
        """
        try:
            self.fenetre.draw_rect(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.message_erreur("la fenêtre n'a pas été ouverte.")

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

            self.fenetre.draw_text(texte, position_x, position_y, taille, couleur)
        except AttributeError:
            self.message_erreur("la fenêtre n'a pas été ouverte.")

    ### CAMERA - PHOTOS ###

    def afficher_camera(self, position_x: int = 0, position_y: int = 0):
        """
            Affiche la caméra aux coordonées x et y.
        """
        self.camera.display(position_x, position_y)

    def prendre_photo(self, nom_fichier: str):
        """
            Capture une image de la caméra au nom du fichier passé en paramètre et l'enregistre dans le dossier images.
        """
        self.camera.capture(nom_fichier)

    def afficher_image(self, chemin_fichier: str, position_x: int, position_y: int):
        r"""
            Afficher une image. \n
            Les paramètres attendus sont : \n
                * Le chemin et nom du fichier. (ex: /images/photo.jpg) \n
                * Les coordonnées x et y où sera affichée l'image.
        """
        self.fenetre.display_image_from_path(chemin_fichier, position_x, position_y)

    def appliquer_filtre(self, chemin_fichier: str, nom_filtre: str):
        r"""
            Applique un filtre sur une image. \n
            Les paramètres attendus sont : \n
                * Le chemin et nom du fichier. (ex: /images/photo.jpg) \n
                * Le nom du filtre. (ex: cartoon, alien, tourner...) \n
        (voir documentation pour la liste complète des filtres: https://42angouleme.github.io/ref/)
        """
        self.fenetre.set_filter(chemin_fichier, nom_filtre)

    ### RECONNAISANCE CARTES - SESSION UTILISATEUR ###

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
        if self.webapp is None:
            self.message_avertissement(
                "La fonction Robot.connecter() a été appelée"
                "sans Robot.demarrer_webapp()")
            return
        elif not self.camera.camera.isOpened():
            return
        utilisateur_reconnu, _ = self.camera.detect_user(seuil_minimal,
                                                         seuil_arret_recherche)
        if utilisateur_reconnu and self.verifier_session():
            self.message_avertissement("Un utilisateur est déjà connecté.")
        elif utilisateur_reconnu:
            self.utilisateur_connecte = utilisateur_reconnu

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
        if self.webapp is None:
            self.message_avertissement(
                "La fonction Robot.detecter_carte() a été appelée"
                "sans Robot.demarrer_webapp()")
            return None
        elif not self.camera.camera.isOpened():
            return None
        carte_reconnue, _ = self.camera.detect_card(seuil_minimal,
                                                    seuil_arret_recherche)
        return carte_reconnue

    def afficher_carte_detectee(self, carte_detectee: MatLike, position_x: int, position_y: int):
        r"""
            Afficher la carte détectée. \n
            Les paramètres attendus sont : \n
                * L'image de la carte detectée par Robot.detecter_carte() \n
                * Les coordonnées x et y où sera affichée l'image.
        """
        self.fenetre.display_image_from_path(carte_detectee, position_x, position_y)

    def deconnecter(self):
        """
            Déconnecte la personne actuellement connectée.
        """
        self.utilisateur_connecte = None

    def verifier_session(self) -> bool:
        """
            Indique si un utilisateur est déjà connecté.

            Retourne:
                * True: Si une personne est connectée
                * False: Sinon
        """
        return self.utilisateur_connecte is not None

    def recuperer_utilisateur_connecte(self) -> Dict:
        """
            Méthode qui retourne un object contenant:
                - prenom de l'utilisateur
                - nom de l'utilisateur
        """
        user = dict()
        user['prenom'] = self.utilisateur_connecte.first_name
        user['nom'] = self.utilisateur_connecte.last_name
        # user['carte'] = self.utilisateur_connecte.picture
        return user

    def creer_utilisateur(self, prenom: str, nom: str, carte: MatLike):
        """
            Créer un utilisateur avec les données renseignées en paramètres

        Paramètres:
            - prenom: son prénom
            - nom: son nom de famille
            - carte: l'image de sa carte (générée avec Robot.detecter_carte())
        """
        if self.verifier_session():
            self.message_avertissement("Un utilisateur est déjà connecté")
            return
        elif carte is None:
            self.message_avertissement(
                "Création d'un utilisateur avec une carte invalide (=None)"
            )
            return
        pg.image.save(carte, ".tmp_card.png")
        with open(".tmp_card.png", "rb") as img:
            files = {
                "picture": ("picture.png", img, "image/png"),
            }
            new_user = {
                "first_name": prenom,
                "last_name": nom,
            }
            os.unlink(".tmp_card.png")
            try:
                response = requests.post(
                    f"{APP_BASE_URL}/api/users", data=new_user, files=files
                )
                if response.status_code != 201:
                    self.message_erreur("[HTTP ERROR]" + str(response.content))
                else:
                    print("Success")
                    # Update les cartes des sessions chargées lors
                    #   de la construction de CardsTracker
                    self.camera.updateUserCardsTracker(self.webapp)
            except Exception as e:
                self.message_erreur("[HTTP EXCEPTION]" + str(e))

    def supprimer_utilisateur(self):
        """
           Supprime l'utilisateur connecté.
        """
        if not self.verifier_session():
            self.message_avertissement("Aucun utilisateur n'est connecté")
            return
        try:
            id = self.utilisateur_connecte.id
            response = requests.delete(f"{APP_BASE_URL}/api/users/{id}")
            if response.status_code != 200:
                self.message_erreur("[HTTP ERROR]" + str(response.content))
            else:
                self.deconnecter()
                # Update les cartes des sessions chargées lors
                #   de la construction de CardsTracker
                self.camera.updateUserCardsTracker(self.webapp)
        except Exception as e:
            self.message_erreur("[HTTP EXCEPTION]" + str(e))

    ### IA ###

    def demarrer_discussion(self):
        """
            Commence une discussion avec le robot
        """
        self.chatBot = ChatBot()

    def arreter_discussion(self):
        """
            Arrête la discussion avec le robot
        """
        self.chatBot = None

    def repondre_question(self, question: str) -> str:
        """
            Permet de poser une question au robot.
            Imprime la réponse du robot dans le terminal et la renvoit.
        """
        if (self.chatBot is None):
            self.message_erreur("Aucune conversation n'a été commencé avec le robot")
        reponse = self.chatBot.get_ai_answer(question)
        print("Humain : " + question + "\nRobot : " + reponse)
        return reponse
        # En finalité la fonction n'imprimera plus la reponse
        # return "Réponse"

    def creer_historique(self):
        """
            Renvoit un nouvel historique de conversation
        """
        if (self.chatBot is None):
            self.message_erreur("Aucune conversation n'a été commencé avec le robot")
        return self.chatBot.create_conversation_history()

    def charger_historique(self, historique_de_conversation=None):
        """
            Commence la discussion avec le robot.
            L'historique de la conversation passé en paramètre doit être récuperé / crée avant d'appeler cette fonction pour pour le passer en paramètre à la fonction.
            Sinon le robot n'aura pas de mémoire.
        """
        if (self.chatBot is None):
            self.message_erreur("Aucune conversation n'a été commencée avec le robot")
        self.chatBot.load_history(historique_de_conversation)

    def supprimer_historique(self):
        """
            Arrête la discussion actuelle avec le robot.
            Après l'appel de cette fonction, le robot ne se souvient plus de la discussion.
        """
        if (self.chatBot is None):
            self.message_erreur("Aucune conversation n'a été commencée avec le robot")
        self.chatBot.unload_history()

    def recuperer_historique_de_conversation(self):
        """
            Permet de récupérer la discussion actuelle de l'utilisateur.
        """
        if (self.chatBot is None):
            self.message_erreur("Aucune conversation n'a été commencé avec le robot")
        memory = self.chatBot.getCurrentConversationHistory()
        return memory

    def choisir_emotion(texte, liste_emotions: List[str] = []):
        """
            ...
        """
        print("avec", texte, "choisir emotion dans", liste_emotions)

    def entrainer(self, texte: str):
        """
            ...
        """
        print("entraîner avec", texte)

    ### ENTREE UTILISATEUR ###

    def creer_zone_texte(self, longueur: int, hauteur: int, position_x: int, position_y: int, couleur: Couleur):
        """
            Créer et retourner une zone de texte qui peut être affichée et vérifiée plus tard. \n
            Cela est utile pour récupérer les entrées utilisateur \n
            Les paramètres attendus sont : \n
                * la longueur et la hauteur du bouton. \n
                * la position x et y du bouton (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la couleur du bouton.
        """
        try:
            return self.fenetre.create_text_area(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.message_erreur("la fenêtre n'a pas été ouverte.")

    def get_user_entry(self, texte, text_area):
        """
            Ne pas utiliser
            Allow to get the user_entry, use in texte_area and in fuction ecrire
        """
        letter = Input.get_user_entry(self, text_area)
        if (letter is not None):
            if letter == "\b":
                texte = texte[:-1]
            else:
                texte += letter
        return texte

    def ecrire(self, text_area):
        """
            Permet à l'utilisateur d'écrire dans la zone de texte associé.
            Renvoit le texte écrit par l'utilisateur.
        """
        new_text = ""
        self.isWriting = True
        text = text_area.recuperer_texte()
        print("User start writing")
        while self.isWriting:
            if not text_area.is_pressed():
                self.isWriting = False
            new_text = self.get_user_entry(text, text_area)
            if (not self.actif):
                return ""
            if (new_text != text):
                if ("\r" in new_text):
                    self.isWriting = False
                    text_area.pressed = False
                    break
                text_area.add_text(new_text, 10, 10, text)
                text_area.afficher()
                self.actualiser_affichage()  # Vraiment utile ??
                text = new_text
        print("User end writing")
        return text

    ### AUDIO ###

    def parler(self, texte: str):
        """
            ...
        """
        print("texte conversion audio", texte)

    ### MICROPHONE ###

    def enregister_audio(self):
        """
            ...
        """
        print("enregistrer audio")

    ### AUTRES ###
    def message_erreur(self, msg: str):
        print(f"\033[91mErreur: {msg}\033[00m", file=sys.stderr)

    def message_avertissement(self, msg: str):
        print(f"\033[33mAttention: {msg}\033[00m", file=sys.stderr)

    APP_BASE_URL, APP_ADRESS, APP_PORT = [""] * 3
    @staticmethod
    def load_env_file(path_file: str = '.env'):
        global APP_BASE_URL, APP_ADRESS, APP_PORT
        load_dotenv(dotenv_path=Path(path_file))
        APP_BASE_URL = os.getenv('WEBAPP_BASE_URI')
        APP_ADRESS = APP_BASE_URL.split(':')[1][2:]
        APP_PORT = APP_BASE_URL.split(':')[2]
