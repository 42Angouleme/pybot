from pybot import Robot

robot = Robot()

longueur = 800
hauteur = 600

robot.allumer_ecran()

robot.changer_titre("Exemple 2")

robot.ajouter_bouton("Quitter", robot.eteindre_ecran)
robot.ajouter_bouton("Afficher visage", robot.afficher_visage_content)

robot.lancer_boucle()
