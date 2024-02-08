# from pybot import Robot

# robot = Robot()

# robot.demarrer_module_fenetre()

# robot.fenetre.changer_titre("bonjour,pybot!")
# robot.fenetre.ouvrir_fenetre()
# robot.fenetre.changer_titre("bonjour,pybot!")
# robot.fenetre.actualiser_affichage()
# robot.dort(1)
# robot.fenetre.changer_titre("plein écran dans une seconde")
# robot.fenetre.actualiser_affichage()
# robot.dort(1)
# robot.fenetre.plein_ecran(True)
# robot.fenetre.actualiser_affichage()
# robot.dort(1)
# robot.fenetre.changer_titre("fin du programme dans une seconde")
# robot.fenetre.plein_ecran(False)
# robot.fenetre.actualiser_affichage()
# robot.dort(1)

from pybot import Robot, Couleur

robot = Robot()
robot.demarrer_module_fenetre()

robot.fenetre.ouvrir_fenetre(1200, 900)

boutons = robot.attributs.boutons
boutons.quitter = robot.fenetre.creer_bouton(100, 100, 100, 100, Couleur.BLANC)
boutons.quitter.ajouter_texte("Quitter", 10, 10, 20, Couleur.NOIR)

while robot.est_actif():
    boutons = robot.attributs.boutons
    if boutons.quitter.est_actif():
        robot.desactiver()
        break # Sort de la boucle
    boutons.quitter.afficher()
    robot.fenetre.actualiser_affichage()