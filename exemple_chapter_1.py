from pybot import Robot

robot = Robot()

robot.demarrer_module_fenetre()

robot.fenetre.changer_titre("bonjour,pybot!")
robot.fenetre.ouvrir_fenetre()
robot.fenetre.changer_titre("bonjour,pybot!")
robot.fenetre.actualiser_affichage()
robot.dort(1)
robot.fenetre.changer_titre("plein écran dans une seconde")
robot.fenetre.actualiser_affichage()
robot.dort(1)
robot.fenetre.plein_ecran(True)
robot.fenetre.actualiser_affichage()
robot.dort(1)
robot.fenetre.changer_titre("fin du programme dans une seconde")
robot.fenetre.plein_ecran(False)
robot.fenetre.actualiser_affichage()
robot.dort(1)