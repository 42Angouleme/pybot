from .module_ecran import module as ecran
from .module_ecran.Input import Input
from .module_ecran.filtres import Filtres
from .module_webapp import create_app
import os, sys
import time


class Robot:
    def __init__(self):
        self.debug = True
        self.ecran = None
        self.titre = "Pybot"
        self.actif = True
        self.events = []
        self.zone = "menu"

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
            Créer un écran avec une longueur et une hauteur de fenêtre passée en argument (en nombre de pixels).
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
            Retourne vrai (True) ou faux (False) pour savoir si le robot est toujours actif.
            Peut être utilisé pour vérifier la sortie d'une boucle.
        '''
        return self.actif
    
    def desactiver(self):
        '''
            Passe la variable self.actif du robot en mode False
        '''
        self.actif = False

    def eteindre_ecran(self):
        '''
            Sert à éteindre correctement l'écran (et la bibliothèque graphique), le robot est inactivé.
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
            Ajoute à la liste des évènements, un évènement et la touche liée, un évènement peut avoir plusieurs touches.
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
            ...
        """
        self.ecran.change_background_color(couleur[0], couleur[1], couleur[2])

    def afficher_fond(self):
        """
            ...
        """
        self.ecran.draw_background()

    def creer_bouton(self, longueur, hauteur, position_x, position_y, couleur):
        """
            ...
        """
        return self.ecran.create_button(longueur, hauteur, position_x, position_y, couleur)

    def dessiner_rectangle(self, longueur, hauteur, position_x, position_y, couleur):
        """
            ...
        """
        self.ecran.draw_rect(longueur, hauteur, position_x, position_y, couleur)
    
    def afficher_texte(self, texte, position_x=0, position_y=0, taille=16, couleur=(0, 0, 0)):
        """
            ...
        """
        self.ecran.draw_text(texte, position_x, position_y, taille, couleur)

    def zone_courante(self):
        """
            Retourne la zone courante.
        """
        return self.zone

    def changer_zone(self, nom):
        """
            Change la zone courante.
        """
        self.zone = nom

    ### CAMERA - CARTES ###
    ### IA ###
    ### AUDIO ###
    ### MICROPHONE ###

    ### AUTRES ###
    def message_erreur(self, msg):
        print(f"\033[91mErreur: {msg}\033[00m")