from pybot import Robot
robot = Robot()

robot.changer_titre("bonjour,pybot!") # Erreur
robot.allumer_ecran()
robot.changer_titre("bonjour,pybot!")
robot.dessiner_ecran()
robot.dort(1)
robot.changer_titre("plein écran dans une seconde")
robot.dessiner_ecran()
robot.dort(1)
robot.plein_ecran(True)
robot.dessiner_ecran()
robot.dort(1)
robot.changer_titre("fin du programme dans une seconde")
robot.plein_ecran(False)
robot.dessiner_ecran()
robot.dort(1)
