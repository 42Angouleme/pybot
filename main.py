from main_initialisation import robot, initialiser_fenetre, initialiser_evenements, initialiser_modules, initialiser_boutons
from main_boucles import boucle_evenements, boucle_affichage_fenetre_titre, boucle_affichage_fenetre_connexion, boucle_affichage_fenetre_creation, boucle_affichage_fenetre_session
from main_boucles import boucle_boutons_fenetre_creation, boucle_boutons_fenetre_titre, boucle_boutons_fenetre_connexion, boucle_connexion, boucle_boutons_fenetre_session

one_time = True

if __name__ == "__main__":
    initialiser_fenetre()
    initialiser_evenements()
    initialiser_modules()
    initialiser_boutons()
    while robot.est_actif():
        boucle_evenements()

        # --- FENETRE TITRE ---
        if robot.attributs.page == 0:
            boucle_affichage_fenetre_titre()
            boucle_boutons_fenetre_titre()

        # --- FENETRE CONNEXION ---
        if robot.attributs.page == 1:
            boucle_affichage_fenetre_connexion()
            boucle_boutons_fenetre_connexion()
            boucle_connexion()

        # --- FENETRE CREATION ---
        if robot.attributs.page == 2:
            boucle_affichage_fenetre_creation()
            boucle_boutons_fenetre_creation()
        
        # --- FENETRE SESSION ---
        if robot.attributs.page == 3:
            boucle_affichage_fenetre_session()
            boucle_boutons_fenetre_session()