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
mettre_a_jour_affichage = True

def preparer_programme():
    global bouton_camera
    robot.allumer_ecran(long, haut)
    robot.changer_titre("Bonjour camera!")
    robot.couleur_fond(noir)

    robot.ajouter_evenement("echap", "stop")
    bouton_camera = robot.creer_bouton(120, 50, 10, 10, bleu)

def affichage_ecran():  
    global mettre_a_jour_affichage
    if mettre_a_jour_affichage:
        robot.afficher_fond()
        bouton_camera.afficher()
        mettre_a_jour_affichage = False

def verifier_boutons():
    global mettre_a_jour_affichage, afficher_camera
    if bouton_camera.verifier_contact():
        afficher_camera = not afficher_camera
        if afficher_camera:
            print("afficher camera")
        else:
            print("eteindre camera")
        mettre_a_jour_affichage = True

def boucle_programme():
    while robot.est_actif():
        events = robot.verifier_evenements()
        if "stop" in events:
            robot.eteindre_ecran()
        affichage_ecran()
        verifier_boutons()
        robot.dessiner_ecran()

if __name__ == "__main__":
    preparer_programme()
    boucle_programme()