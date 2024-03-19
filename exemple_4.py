from pybot import Robot, Couleur

# ---- Dans main_initialisation.py -------
robot = Robot()

long = 1200
haut = 1000

robot.demarrer_module_fenetre()

robot.attributs.afficher_camera = False
robot.attributs.afficher_photo = False
robot.attributs.mettre_a_jour_affichage = True

def initialisation_fenetre():
    robot.fenetre.ouvrir_fenetre(long, haut)
    robot.demarrer_module_camera()
    robot.fenetre.changer_titre("Bonjour camera!")
    robot.fenetre.changer_couleur_fond(Couleur.NOIR)

def initialisation_evenements():
    robot.ajouter_evenement("echap", "stop")

def initialisation_boutons():
    boutons = robot.attributs.boutons
    boutons.camera = robot.fenetre.creer_bouton(180, 60, 10, 10, Couleur.BLEU)
    boutons.camera.ajouter_texte("camera - allumer", 5, 20)
    boutons.capture = robot.fenetre.creer_bouton(180, 60, 10, 80, Couleur.ROUGE)
    boutons.capture.ajouter_texte("capture photo", 10, 10, 20)
    boutons.photo = robot.fenetre.creer_bouton(180, 60, 10, 150, Couleur.JAUNE)
    boutons.photo.ajouter_texte("afficher photo", 10, 10, 16)
    boutons.filter_1 = robot.fenetre.creer_bouton(200, 60, 15, 220, Couleur.ORANGE)
    boutons.filter_1.ajouter_texte("filtre: ocean", 10, 10, 16)
    boutons.filter_2 = robot.fenetre.creer_bouton(200, 60, 15, 290, Couleur.ORANGE)
    boutons.filter_2.ajouter_texte("filtre: cartoon", 10, 10, 16)
    boutons.filter_3 = robot.fenetre.creer_bouton(200, 60, 15, 360, Couleur.ORANGE)
    boutons.filter_3.ajouter_texte("filtre: alien", 10, 10, 16)
    boutons.filter_4 = robot.fenetre.creer_bouton(200, 60, 15, 430, Couleur.ORANGE)
    boutons.filter_4.ajouter_texte("filtre: rose", 10, 10, 16)
    boutons.filter_5 = robot.fenetre.creer_bouton(200, 60, 15, 500, Couleur.ORANGE)
    boutons.filter_5.ajouter_texte("filtre: flou", 10, 10, 16)
    boutons.filter_6 = robot.fenetre.creer_bouton(200, 60, 15, 570, Couleur.ORANGE)
    boutons.filter_6.ajouter_texte("filtre: noir et blanc", 10, 10, 16)
    boutons.filter_7 = robot.fenetre.creer_bouton(200, 60, 15, 640, Couleur.ORANGE)
    boutons.filter_7.ajouter_texte("filtre: tourner", 10, 10, 16)
    boutons.filter_8 = robot.fenetre.creer_bouton(200, 60, 15, 710, Couleur.ORANGE)
    boutons.filter_8.ajouter_texte("filtre: vernis", 10, 10, 16)
    boutons.stop = robot.fenetre.creer_bouton(180, 60, 10, 900, Couleur.VERT_SAPIN)
    boutons.stop.ajouter_texte("quitter", 10, 10, 20)
# ----------------------------------------


# -------- Dans main_boucle.py -----------
def boucle_fenetre():
    boutons = robot.attributs.boutons
    if robot.attributs.afficher_camera:
        robot.camera.afficher_camera(300, 10)
    if robot.attributs.afficher_photo:
        robot.fenetre.afficher_image("/images/photo.jpg", 300, 500)
        robot.fenetre.afficher_image("/images/fier.png", 1000, 500)
    if robot.attributs.mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()
        boutons.camera.afficher()
        boutons.photo.afficher()
        boutons.filter_1.afficher()
        boutons.filter_2.afficher()
        boutons.filter_3.afficher()
        boutons.filter_4.afficher()
        boutons.filter_5.afficher()
        boutons.filter_6.afficher()
        boutons.filter_7.afficher()
        boutons.filter_8.afficher()
        boutons.stop.afficher()
        if robot.attributs.afficher_camera:
            boutons.capture.afficher()
        robot.attributs.mettre_a_jour_affichage = False

def boucle_evenements():
    events = robot.verifier_evenements()
    if "stop" in events:
        robot.desactiver()

def boucle_boutons():
    boutons = robot.attributs.boutons
    afficher_camera = robot.attributs.afficher_camera
    afficher_photo = robot.attributs.afficher_photo
    if boutons.camera.est_actif():
        afficher_camera = not afficher_camera
        robot.attributs.afficher_camera = afficher_camera
        if afficher_camera:
            boutons.camera.ajouter_texte("camera - eteindre")
        else:
            boutons.camera.ajouter_texte("camera - alumer")
        robot.attributs.mettre_a_jour_affichage = True
    if afficher_camera:
        if boutons.capture.est_actif():
            robot.camera.prendre_photo("photo")
    if boutons.photo.est_actif():
        afficher_photo = not afficher_photo
        robot.attributs.afficher_photo = afficher_photo
        if robot.attributs.afficher_photo:
            boutons.photo.ajouter_texte("cacher photo")
        else:
            boutons.photo.ajouter_texte("afficher photo")
        robot.attributs.mettre_a_jour_affichage = True
    if boutons.stop.est_actif():
        robot.desactiver()
    if boutons.filter_1.est_actif():
        robot.camera.appliquer_filtre("/images/photo.jpg", "ocean")
        robot.attributs.mettre_a_jour_affichage = True
    if boutons.filter_2.est_actif():
        robot.camera.appliquer_filtre("/images/photo.jpg", "cartoon")
        robot.attributs.mettre_a_jour_affichage = True
    if boutons.filter_3.est_actif():
        robot.camera.appliquer_filtre("/images/photo.jpg", "alien")
        robot.attributs.mettre_a_jour_affichage = True
    if boutons.filter_4.est_actif():
        robot.camera.appliquer_filtre("/images/photo.jpg", "rose")
        robot.attributs.mettre_a_jour_affichage = True
    if boutons.filter_5.est_actif():
        robot.camera.appliquer_filtre("/images/photo.jpg", "flou")
        robot.attributs.mettre_a_jour_affichage = True
    if boutons.filter_6.est_actif():
        robot.camera.appliquer_filtre("/images/photo.jpg", "noir_et_blanc")
        robot.attributs.mettre_a_jour_affichage = True
    if boutons.filter_7.est_actif():
        robot.camera.appliquer_filtre("/images/photo.jpg", "tourner")
        robot.attributs.mettre_a_jour_affichage = True
    if boutons.filter_8.est_actif():
        robot.camera.appliquer_filtre("/images/photo.jpg", "vernis")
        robot.attributs.mettre_a_jour_affichage = True
# ----------------------------------------


if __name__ == "__main__":
    initialisation_fenetre()
    initialisation_evenements()
    initialisation_boutons()
    while robot.est_actif():
        boucle_evenements()
        boucle_boutons()
        boucle_fenetre()
        robot.fenetre.actualiser_affichage()