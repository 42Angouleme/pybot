from pybot import Robot


# ---- Dans main_initialisation.py -------
robot = Robot()

long = 1024
haut = 800

robot.demarrer_module_fenetre(long, haut)

robot.fenetre.ouvrir_fenetre()
robot.fenetre.changer_titre("Bonjour!")

def initialisation_evenements():
    print("Creation des eveneemnts sur les touches <ECHAP> ou <C>")
    robot.ajouter_evenement("echap", "stop")
    robot.ajouter_evenement("C", "carotte")
# ----------------------------------------

# -------- Dans main_boucle.py -----------
def boucle_evenements():
    evenements = robot.verifier_evenements()
    if "stop" in evenements:
        robot.desactiver()
    elif "carotte" in evenements:
        print("Suppression de l' évenement de la touche <C>")
        robot.supprimer_evenement("carotte")
        print("Création de l' évenement de la touche <P>")
        robot.ajouter_evenement("P", "poireau")
    elif "poireau" in evenements:
        print("Suppression des évenements de la touche <P> et <Echap>")
        robot.supprimer_evenement("poireau")
        robot.supprimer_evenement("stop")
        print("Pour quitter tu dois maintenant utiliser: <Q>")
        robot.ajouter_evenement("Q", "stop")
# ----------------------------------------


if __name__ == '__main__':
    initialisation_evenements()
    while robot.est_actif():
        boucle_evenements()
        robot.fenetre.actualiser_affichage()
