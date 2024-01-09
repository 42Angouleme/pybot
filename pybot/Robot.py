from .module_ecran import module as ecran
from .module_ecran.Input import Input
from .module_webapp import create_app
from .module_ia.IA import ChatBot
import os, sys
import time


class Robot:
    def __init__(self):
        self.debug = True
        self.ecran = None
        self.titre = "Pybot"
        self.actif = True
        self.events = []
        self.chatBot = None

    ### GENERAL - ECRAN ###

    def demarrer_webapp(self):
        '''
            Cette méthode lance de manière non bloquant le serveur web qui s'occupe de la partie base de donnée.
        '''
        pid = os.fork()
        if pid:
            webapp = create_app(root_dir=os.path.dirname(os.path.abspath(__file__)))
            webapp.run()
            sys.exit()

    def allumer_ecran(self, longueur=800, hauteur=600):
        '''
            Créer un écran avec une longueur et une hauteur de fenêtre passée en argument (en nombre de pixels). \n
            Si un argument n'est pas donné, la longueur par défaut sera 800 pixels et la hauteur par défaut sera 600 pixels.
        '''
        self.ecran = ecran.run(self, longueur, hauteur)

    def changer_titre(self, titre):
        '''
            Changer le titre de la fenêtre.
        '''
        try:
            self.ecran.update_title(titre)
        except AttributeError:
            self.message_erreur("Le titre doit être défini aprés création de l'écran.")

    def dessiner_ecran(self):
        '''
            Fonction nécessaire dans une boucle pour mettre à jour l'affichage de l'écran.
        '''
        self.ecran.render()

    def plein_ecran(self, changer):
        '''
            Passer l'ecran en plein ecran (changer=True) ou en sortir (changer=False).
        '''
        self.ecran.update_fullscreen(changer)

    def dort(self, secondes):
        '''
            Le programme restera en attente le nombre de seconde passé en argument.
        '''
        time.sleep(secondes)
    
    def est_actif(self):
        '''
            Retourne vrai (True) ou faux (False) pour savoir si le robot est toujours actif. \n
            Peut être utilisé pour vérifier la sortie d'une boucle.
        '''
        return self.actif
    
    def desactiver(self):
        '''
            Passe la variable self.actif du robot avec la valeur False.
        '''
        self.actif = False

    def eteindre_ecran(self):
        '''
            Sert à éteindre correctement l'écran (et la bibliothèque graphique), le robot est inactivé. \n
            Combiné avec un évènement (par exemple appuyer sur une touche ou un bouton) il peut etre utilisé pour arrêter le programme.
        '''
        try:
            self.ecran.stop()
            self.actif = False
        except AttributeError:
                self.message_erreur("L'écran n'a pas été allumé.")

    ### GENERAL - EVENEMENTS ###

    def ajouter_evenement(self, touche, nom):
        """
            Ajoute à la liste des évènements, un évènement et la touche liée, un évènement peut avoir plusieurs touches. \n
            Voir documentation pour la liste des touches possibles.
        """
        new = (touche.lower(), nom)
        if new not in self.events:
            self.events.append(new)

    def supprimer_evenement(self, nom):
        """
            Supprimer l'évènement donnée en paramètre de la liste des évènements.
        """
        for e in self.events:
            if e[1] == nom:
                self.events.remove(e)

    def verifier_evenements(self):
        """
            Vérifie chaque évènements et retourne un tableau avec les évènements détectés.
        """
        return Input.check(self.events, self)


    ### INTERFACE - BOUTONS ###

    def couleur_fond(self, couleur):
        """
            Change la couleur du fond d'écran. \n
            La couleur passée en paramètre doit être au format: (R, G, B). \n
            R, G et B sont des nombres entre 0 et 255.
        """
        try:
            self.ecran.change_background_color(couleur[0], couleur[1], couleur[2])
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")

    def afficher_fond(self):
        """
            Affiche le fond d'écran avec la couleur enregistrée en dernier avec la fonction couleur_fond() \n
            (par défaut, la couleur est noir).
        """
        try:
            self.ecran.draw_background()
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")


    def creer_bouton(self, longueur, hauteur, position_x, position_y, couleur):
        """
            Créer et retourner un bouton qui peut être affiché et vérifié plus tard. \n
            Les paramètres attendus sont : \n
                * la longueur et la hauteur du bouton. \n
                * la position x et y du bouton (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la couleur du bouton.
        """
        try:
            return self.ecran.create_button(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")


    def dessiner_rectangle(self, longueur, hauteur, position_x, position_y, couleur):
        """
            Dessine un rectangle dans la fenêtre. \n
        
            Les paramètres attendus sont : \n
                * la longueur et la hauteur du rectangle. \n
                * la position x et y du rectangle (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la couleur du rectangle.
        """
        try:
            self.ecran.draw_rect(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")

    
    def afficher_texte(self, texte, position_x=0, position_y=0, taille=16, couleur=(0, 0, 0)):
        """
            Affiche un texte dans la fenêtre. \n

            Les paramètres attendus sont : \n
                * le texte à afficher. \n
                * la position x et y du texte (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la taille du texte. \n
                * la couleur du texte.
        """

        try:

            self.ecran.draw_text(texte, position_x, position_y, taille, couleur)
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")

    ### CAMERA - PHOTOS ###
    
    def afficher_camera(self, x=0, y=0):
        """
            ...
        """
        self.ecran.display_camera(x, y)

    def prendre_photo(self, nom_fichier):
        """
            ...
        """
        self.ecran.capture_photo(nom_fichier)
        
    def afficher_image(self, chemin_fichier, position_x, position_y):
        """
            ...
        """
        self.ecran.display_image(chemin_fichier, position_x, position_y)

    def appliquer_filtre(self, chemin_fichier, nom_filtre):
        """
            ...
        """
        self.ecran.set_filter(chemin_fichier, nom_filtre)

    ### RECONNAISANCE CARTES - SESSION UTILISATEUR ###
        
    def detecter_carte(self):
        """
            ...
        """
        return self.ecran.detect_card()
    
    def creer_session(self, nom_eleve):
        """
            ...
        """
        print("creer une session pour", nom_eleve)

    def fermer_session(self):
        """
            ...
        """
        print("fermer une session")

    def verifier_session(self):
        """
            ...
        """
        print("vérifier session")

    ### IA ###

    def demarrer_discussion(self) :
        """
            Commence une discussion avec le robot
        """
        self.chatBot = ChatBot()
    
    def arrêter_discussion(self) :
        """
            Arrete la discussion avec le robot
        """
        self.chatBot = None

    def repondre_question(self, question):
        """
            Permet de poser une question au robot.
            Imprime la réponse du robot
        """
        if (self.chatBot == None) :
            self.message_erreur("Aucune conversation n'a été commencé avec le robot")
        reponse = self.chatBot.get_ai_answer(question)
        print(reponse)
        # En finalité la fonction renverra la réponse du robot.
        # return "Réponse"
    
    def charger_historique(self, historique_de_conversation=None):
        """
            Commence la discussion avec le robot.
            L'historique de la conversation passer en parametre doit etre recuperer / cree avant d'appeler cette fonction pour pour le passer en parametre a la fonction.
            Sinon le robot n'aura pas de mémoire.
        """
        if (self.chatBot == None) :
            self.message_erreur("Aucune conversation n'a été commencé avec le robot")
        self.chatBot.load_history(historique_de_conversation)
           
    def supprimer_historique(self) :
        """
            Arrete la discussion actuel avec le robot
            Après l'appelle de cette fonction le robot ne se souvient plus de la discussion
        """
        if (self.chatBot == None) :
            self.message_erreur("Aucune conversation n'a été commencé avec le robot")
        self.chatBot.unload_history()

    def recuperer_historique_de_conversation(self):
        """
            Permet de recuperer la discussion actuel de l'utilisateur avec le robot
        """
        if (self.chatBot == None) :
            self.message_erreur("Aucune conversation n'a été commencé avec le robot")
        memory = self.chatBot.getCurrentConversationHistory()
        return memory
    
    def choisir_emotion(texte, liste_emotions):
        """
            ...
        """
        print("avec", texte, "choisir emotion dans", liste_emotions)
    
    def entrainer(self, texte):
        """
            ...
        """
        print("entrainer avec", texte)


    ### AUDIO ###

    def parler(self, texte):
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
    def message_erreur(self, msg):
        print(f"\033[91mErreur: {msg}\033[00m")
