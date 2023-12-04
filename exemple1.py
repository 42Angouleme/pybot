from pybot import Robot

robot = Robot()

longueur = 800
hauteur = 600

robot.allumer_ecran(longueur, hauteur)

robot.changer_titre("Exemple 1")

robot.lancer_boucle()
