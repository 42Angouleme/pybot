from pybot import Robot
robot = Robot()

long = 1024
haut = 800

def ecrire_nom_evenement(event_name):
    print("L'évènement est:", event_name)

def preparer_robot():
    robot.allumer_ecran(long, haut)
    robot.changer_titre("Bonjour!")
    robot.ajouter_evenement("ESC", "stop")
    robot.ajouter_evenement("A", "banane")
    robot.ajouter_evenement("B", "banane")
    robot.ajouter_evenement("C", "carotte")

preparer_robot()

nom = "poireau"
while robot.est_actif():
    events = robot.verifier_evenements()    
    if "stop" in events:
        robot.eteindre_ecran()
    elif "carotte" in events:
        ecrire_nom_evenement("carotte")
        robot.ajouter_evenement("P", "poireau")
    elif nom in events:
        ecrire_nom_evenement(nom)
        if nom == "poireau":
            robot.supprimer_evenement("carotte")
            nom = "banane"
        if nom == "banane":
            robot.supprimer_evenement("stop")
            robot.ajouter_evenement("Q", "stop")
    robot.dessiner_ecran()
