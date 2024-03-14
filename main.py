from main_boucle import boucle_boutons, boucle_fenetre, boucle_session, boucle_evenements
from main_initialiser import robot, initialiser_boutons, initialiser_evenements, initialiser_fenetre, initialiser_session


if __name__ == "__main__":
    initialiser_fenetre()
    initialiser_evenements()
    initialiser_boutons()
    initialiser_session()
    while robot.est_actif():
        boucle_evenements()
        boucle_boutons()
        boucle_fenetre()
        boucle_session()
        robot.fenetre.actualiser_affichage()
