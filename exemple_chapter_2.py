from pybot import Robot
robot = Robot()

long = 1024
haut = 800

def ecrire_nom_evenement(event_name):
    print("L'évènement est:", event_name)

def preparer_robot():
    robot.allumer_ecran(long, haut)
    robot.changer_titre("Bonjour!")
    robot.ajouter_evenement("echap", "stop")
    robot.ajouter_evenement("B", "banane")
    robot.ajouter_evenement("C", "carotte")
    print("Vous pouvez maintenant utiliser ECHAP et C")

preparer_robot()

nom = "poireau"
while robot.est_actif():
    events = robot.verifier_evenements()    
    if "stop" in events:
        robot.eteindre_ecran()
    elif "carotte" in events:
        print("Vous pouvez maintenant utiliser P")
        ecrire_nom_evenement("carotte")
        robot.supprimer_evenement("carotte")
        robot.ajouter_evenement("P", "poireau")
    elif nom in events:
        ecrire_nom_evenement(nom)
        if nom == "poireau":
            print("Vous pouvez maintenant utiliser B")
            robot.supprimer_evenement("poireau")
            nom = "banane"
        elif nom == "banane":
            print("ECHAP ne permet plus de quitter, il faut maintenant utiliser Q")
            robot.supprimer_evenement("stop")
            robot.supprimer_evenement("banane")
            robot.ajouter_evenement("Q", "stop")
    robot.dessiner_ecran()
