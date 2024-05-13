from main_initialisation import robot, initialiser_fenetre, initialiser_evenements, initialiser_modules


if __name__ == "__main__":
    initialiser_fenetre()
    initialiser_evenements()
    while robot.est_actif():
        robot.fenetre.actualiser_affichage()