from main_boucle import boucle_boutons, boucle_fenetre, boucle_session, boucle_evenements
from main_initialisation import robot, initialisation_boutons, initialisation_evenements, initialisation_fenetre, initialisation_session


if __name__ == "__main__":
    initialisation_fenetre()
    initialisation_evenements()
    initialisation_boutons()
    initialisation_session()
    while robot.est_actif():
        boucle_evenements()
        boucle_boutons()
        boucle_fenetre()
        boucle_session()
        robot.actualiser_affichage()
