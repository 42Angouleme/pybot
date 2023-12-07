from pybot import Robot
robot = Robot()

cacher_bouton = False
long = 1024
haut = 800

# def afficher_cacher_bouton():
    # une méthode détaillée :
    # if cacher_bouton == False:
    #     cacher_bouton = True
    # elif cacher_bouton == True:
    #     cacher_bouton = False

    # une méthode alternative :
    # cacher_bouton = not cacher_bouton
    # print("Les boutons sont cachés ?", cacher_bouton)  

def preparer_robot():
    robot.demarrer_webapp()
    robot.changer_titre("hello")
    robot.allumer_ecran(long, haut)

    robot.ajouter_evenement("ESC", "stop")
    robot.ajouter_evenement("Q", "stop")
    # robot.ajouter_evenement("A", "afficher_cacher_bouton")

    # robot.ajouter_bouton("quitter programme", robot.eteindre_ecran)
    # robot.ajouter_bouton("cacher bouton", afficher_cacher_bouton)

preparer_robot()

while robot.est_actif():
    events = robot.verifier_evenements()
    if "stop" in events:
        robot.eteindre_ecran()
    # elif "afficher_cacher_bouton" in events:
    #     afficher_cacher_bouton()
    robot.dessiner_ecran()
