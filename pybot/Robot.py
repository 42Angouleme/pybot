from .module_ecran import module as ecran
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

    def eteindre_ecran(self):
        '''
            Sert à éteindre correctement l'écran (et la bibliothèque graphique), le robot est inactivé.
            Combiné avec un évènement (par exemple appuyer sur une touche ou un bouton) il peut etre utilisé pour arrêter le programme.
        '''
        self.ecran.stop()
        self.actif = False

    def dessiner_ecran(self):
        self.ecran.render()

    def changer_titre(self, titre):
        '''
            Changer le titre de la fenêtre.
        '''
        try:
            self.ecran.update_title(titre)
        except AttributeError:
            self.message_erreur("Le titre doit être défini aprés création de l'écran.")

    def plein_ecran(self, changer):
        '''
            Passer l'ecran en plein ecran (changer=True) ou en sortir (changer=False).
        '''
        self.ecran.update_fullscreen(changer)

    def est_actif(self):
        '''
            Retourne vrai (True) ou faux (False) pour savoir si le robot est toujours actif.
            Peut être utilisé pour vérifier la sortie d'une boucle.
        '''
        return self.actif
    
    def dort(self, secondes):
        '''
            Le programme restera en attente le nombre de seconde passé en argument.
        '''
        time.sleep(secondes)
    
    ### INTERFACE - LAYOUT ###

    ### CAMERA - CARTES ###
    ### IA ###
    ### AUDIO ###
    ### MICROPHONE ###

    ### AUTRES ###
    def message_erreur(self, msg):
        print(f"\033[91mErreur: {msg}\033[00m")