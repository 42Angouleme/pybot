from pybot import Robot

robot = Robot()

robot.changer_titre("bonjour,pybot!") #  Erreur
robot.creer_fenetre()
robot.changer_titre("bonjour,pybot!")
robot.actualiser_affichage()
robot.dort(1)
robot.changer_titre("plein écran dans une seconde")
robot.actualiser_affichage()
robot.dort(1)
robot.plein_ecran(True)
robot.actualiser_affichage()
robot.dort(1)
robot.changer_titre("fin du programme dans une seconde")
robot.plein_ecran(False)
robot.actualiser_affichage()
robot.dort(1)
