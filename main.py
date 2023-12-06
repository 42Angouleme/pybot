from pybot import Robot
robot = Robot()

cacher_bouton = False
long = 1024
haut = 800

def stop():
      robot.eteindre_ecran()

def afficher_cacher_bouton():
    # if cacher_bouton == False:
    #     cacher_bouton = True
    # elif cacher_bouton == True:
    #     cacher_bouton = False
    cacher_bouton = not cacher_bouton
    print(cacher_bouton)
      

def preparer_robot():
    robot.demarrer_webapp()
    robot.changer_titre("hello")
    robot.allumer_ecran(long, haut)

    robot.ajouter_evenement("ESC", stop)
    robot.ajouter_evenement("Q", robot.eteindre_ecran)

    robot.ajouter_evenement("A", afficher_cacher_bouton)

    robot.ajouter_bouton("quitter programme", robot.eteindre_ecran)
    robot.ajouter_bouton("cacher bouton", afficher_cacher_bouton)

preparer_robot()

while robot.est_actif():
    if robot.verifier_evenement("stop"):
        robot.eteindre_ecran()
    robot.mettre_a_jour_ecran()


