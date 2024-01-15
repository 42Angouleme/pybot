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
        self.isWriting = False

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
    
    def afficher_camera(self, position_x=0, position_y=0):
        """
            Affiche la caméra aux coordonées x et y.
        """
        self.ecran.display_camera(position_x, position_y=0)

    def prendre_photo(self, nom_fichier):
        """
            Capture une image de la caméra au nom du fichier passé en paramètre et l'enregistre dans le dossier images.
        """
        self.ecran.capture_photo(nom_fichier)
        
    def afficher_image(self, chemin_fichier, position_x, position_y):
        """
            Afficher une image. \n
            Les paramètres attendus sont : \n
                * Le chemin et nom du fichier. (ex: /images/photo.jpg) \n
                * Les coordonnées x et y ou seront affiché l'image.
        """
        self.ecran.display_image(chemin_fichier, position_x, position_y)

    def appliquer_filtre(self, chemin_fichier, nom_filtre):
        """
            Applique un filtre sur une image. \n
            Les paramètres attendus sont : \n
                * Le chemin et nom du fichier. (ex: /images/photo.jpg) \n
                * Le nom du filtre. (ex: cartoon, alien, tourner...) \n
        (voir documentation pour la liste complète des filtres: https://42angouleme.github.io/ref/)
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
    
    def arreter_discussion(self) :
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
        print("Humain : " + question + "\nRobot : " + reponse)
        return reponse
        # En finalité la fonction n'imprimera plus la reponse
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

    def creer_historique(self) :
        """
            Renvoi un nouvel historique de conversation
        """
        if (self.chatBot == None) :
            self.message_erreur("Aucune conversation n'a été commencé avec le robot")
        return self.chatBot.create_conversation_history()
    
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
    
    ### ENTREE UTILISATEUR ###

    def creer_zone_texte(self, longueur, hauteur, position_x, position_y, couleur):
        """
            Créer et retourner une zone de texte qui peut être affiché et vérifié plus tard. \n
            Cela est utile pour récuperer les entrées utilisateur \n
            Les paramètres attendus sont : \n
                * la longueur et la hauteur du bouton. \n
                * la position x et y du bouton (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la couleur du bouton.
        """
        try:
            return self.ecran.create_text_area(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")
    
    def get_user_entry(self, texte, text_area) :
        """
        """
        letter = Input.get_user_entry(self, text_area)
        if (letter != None) :
            if letter == "\b" :
                texte = texte[:-1]
            else :
                texte += letter
        return texte
    
    def ecrire(self, text_area) :
        """
            Permet à l'utilisateur d'ecrire dans la zone de texte associé
            Renvoie le texte ecrit par l'utilisateur
        """
        new_text = ""
        self.isWriting = True
        text = text_area.renvoi_texte()
        print("User start writing")
        while self.isWriting :
            if not text_area.is_pressed() :
                self.isWriting = False
            new_text = self.get_user_entry(text, text_area)
            if (not self.actif) :
                return ""
            if (new_text != text) :
                if ("\r" in new_text) :
                    self.isWriting = False
                    text_area.pressed = False
                    break
                text_area.add_text(new_text, 10, 10, text)
                text_area.afficher()
                self.dessiner_ecran() # Vraiment utile ??
                text = new_text
        print("User end writing")
        return text

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
