from pybot import Robot
robot = Robot()

long = 1200
haut = 1000

blanc = (255, 255, 255)
noir = (0, 0, 0)
rouge = (235, 64, 52)
rouge_sombre = (117, 23, 16)
bleu = (52, 164, 235)
bleu_sombre = (30, 93, 133)
vert = (105, 230, 83)
vert_sombre = (59, 135, 46)
jaune = (237, 212, 66)
jaune_sombre = (171, 128, 19)

bouton_camera = None
bouton_photo = None
afficher_camera = False

mettre_a_jour_affichage = True

def preparer_programme():
    global bouton_camera, bouton_photo
    robot.allumer_ecran(long, haut)
    robot.changer_titre("Bonjour camera!")
    robot.couleur_fond(noir)

    robot.ajouter_evenement("echap", "stop")
    bouton_camera = robot.creer_bouton(180, 60, 10, 10, bleu)
    bouton_camera.ajouter_texte("camera - allumer", 5, 20)
    bouton_photo = robot.creer_bouton(180, 60, 10, 80, rouge)
    bouton_photo.ajouter_texte("capture photo", 10, 10, 20)

def affichage_ecran():  
    global mettre_a_jour_affichage
    if mettre_a_jour_affichage:
        robot.afficher_fond()
        bouton_camera.afficher()
        if afficher_camera:
            bouton_photo.afficher()
        mettre_a_jour_affichage = False

def verifier_boutons():
    global mettre_a_jour_affichage, afficher_camera
    if bouton_camera.verifier_contact():
        afficher_camera = not afficher_camera
        if afficher_camera:
            bouton_camera.ajouter_texte("camera - eteindre")
        else:
            bouton_camera.ajouter_texte("camera - alumer")
        mettre_a_jour_affichage = True
    if bouton_photo.verifier_contact():
        robot.prendre_photo("photo")

def boucle_programme():
    while robot.est_actif():
        events = robot.verifier_evenements()
        if "stop" in events:
            robot.eteindre_ecran()
        affichage_ecran()
        if afficher_camera:
            robot.afficher_camera(200, 200)
            robot.detecter_carte()
        verifier_boutons()
        robot.dessiner_ecran()

if __name__ == "__main__":
    preparer_programme()
    boucle_programme()