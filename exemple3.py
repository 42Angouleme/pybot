from pybot import Robot
robot = Robot()

long = 1024
haut = 800

rouge = (235, 64, 52)
rouge_sombre = (117, 23, 16)
bleu = (52, 164, 235)
bleu_sombre = (30, 93, 133)
vert = (105, 230, 83)
vert_sombre = (59, 135, 46)
jaune = (237, 212, 66)
jaune_sombre = (171, 128, 19)

bouton_bleu = None
bouton_vert = None
bouton_jaune = None

cacher_bouton = True
mettre_a_jour_affichage = True

def afficher_cacher_bouton():
    global mettre_a_jour_affichage, cacher_bouton
    # une méthode détaillée :
    if cacher_bouton == False:
        cacher_bouton = True
    elif cacher_bouton == True:
        cacher_bouton = False

    # une méthode alternative pour faire passer True à False :
    # cacher_bouton = not cacher_bouton
    mettre_a_jour_affichage = True

def preparer_robot():
    global bouton_bleu, bouton_vert, bouton_jaune
    robot.allumer_ecran(long, haut)
    robot.changer_titre("Bonjour boutons!")
    robot.couleur_fond(rouge)

    robot.ajouter_evenement("echap", "stop")
    robot.ajouter_evenement("espace", "afficher_cacher_bouton")
    bouton_bleu = robot.creer_bouton(100, 40, 100, 100, bleu)
    bouton_vert = robot.creer_bouton(300, 20, 10, 10, vert)
    bouton_vert.configurer_bouton("Afficher boutons")
    bouton_jaune = robot.creer_bouton(500, 30, 200, 220, jaune)
    bouton_jaune.configurer_bouton("Eteindre robot", taille_texte=20, couleur_texte=rouge)

preparer_robot()

while robot.est_actif():
    events = robot.verifier_evenements()
    if "stop" in events:
        robot.eteindre_ecran()
    elif "afficher_cacher_bouton" in events:
        afficher_cacher_bouton()

    if mettre_a_jour_affichage:
        robot.afficher_fond()

        if not cacher_bouton:
            bouton_bleu.afficher_bouton()
            bouton_jaune.afficher_bouton()
        bouton_vert.afficher_bouton()
        mettre_a_jour_affichage = False

    if not cacher_bouton:
        if bouton_jaune.verifier_contact():
            robot.desactiver()
        if bouton_bleu.verifier_contact():
            robot.eteindre_ecran()
    if bouton_vert.verifier_contact():
        if cacher_bouton:
            bouton_vert.configurer_bouton("Cacher bouton")
        else:
            bouton_vert.configurer_bouton("Afficher bouton")
        afficher_cacher_bouton()

    robot.dessiner_ecran()
