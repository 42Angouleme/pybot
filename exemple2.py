from pybot import Robot
robot = Robot()

cacher_bouton = False
long = 1024
haut = 800

def ecrire_nom_event(event_name):
    robot.changer_titre(event_name)

def preparer_robot():
    robot.demarrer_webapp()
    robot.allumer_ecran(long, haut)
    robot.changer_titre("Bonjour!")
    robot.ajouter_evenement("ESC", "stop")
    robot.ajouter_evenement("Q", "stop")
    robot.ajouter_evenement("A", "banane")
    robot.ajouter_evenement("B", "banane")
    robot.ajouter_evenement("C", "poireau")

preparer_robot()

while robot.est_actif():
    events = robot.verifier_evenements()
    nom = "banane"
    if "stop" in events:
        robot.eteindre_ecran()
    if nom in events:
        ecrire_nom_event(nom)
    if "poireau" in events:
        ecrire_nom_event("poireau")
    robot.dessiner_ecran()
