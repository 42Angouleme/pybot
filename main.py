from v2_main_chapter5_boucle import boucle_boutons, boucle_fenetre, boucle_session, boucle_evenements
from v2_main_chapter5_initialiation import robot, initialisation_boutons, initialisation_evenements, initialisation_fenetre, initialisation_session


if __name__ == "__main__":
    initialisation_boutons()
    initialisation_evenements()
    initialisation_fenetre()
    initialisation_session()
    while robot.est_actif():
        boucle_evenements()
        boucle_fenetre()
        boucle_session()
        boucle_boutons()
        robot.actualiser_affichage()