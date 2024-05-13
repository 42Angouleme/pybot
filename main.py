from main_initialisation import robot, initialiser_fenetre, initialiser_evenements, initialiser_modules, initialiser_boutons
from main_boucles import boucle_evenements, boucle_affichage_fenetre_titre, boucle_boutons_fenetre_titre

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
            boucle_boutons_fenetre_titre()
            boucle_affichage_fenetre_titre()

        # --- FENETRE CONNEXION ---
        if robot.attributs.page == 1:
            if one_time:
                robot.fenetre.afficher_fond()
                one_time = False

        # --- FENETRE CREATION ---
        if robot.attributs.page == 2:
            if one_time:
                robot.fenetre.afficher_fond()
                one_time = False