from pybot import Robot
robot = Robot()

long = 840
haut = 300

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

paroles_index = 0
paroles_robot = [
    "Salut ! Je m'appelle Pybot le robot. Je suis ici pour t'aider,", 
    "jouer avec toi et répondre à toutes tes questions.",
    "Je peux raconter des histoires passionnantes, jouer à des jeux amusants,",
    "et même t'aider avec tes devoirs.",
    "J'ai aussi une super fonction de danse pour les moments joyeux.",
    "Alors, prêt pour des moments incroyables en ma compagnie ?"
]

bouton_menu = None
bouton_quitter = None
bouton_discussion = None
bouton_plus = None

mettre_a_jour_affichage = True

zone = "menu"

def preparer_programme():
    global bouton_menu, bouton_quitter, bouton_discussion, bouton_plus
    robot.allumer_ecran(long, haut)
    robot.changer_titre("Bonjour boutons!")
    robot.couleur_fond(rouge)

    robot.ajouter_evenement("echap", "stop")
    bouton_menu = robot.creer_bouton(120, 50, 10, 10, bleu)
    bouton_menu.ajouter_texte("Menu", couleur=jaune)
    bouton_quitter = robot.creer_bouton(120, 50, 10, 110, vert)
    bouton_quitter.ajouter_texte("Quitter", 10, 10, 24)
    bouton_discussion = robot.creer_bouton(120, 50, 10, 220, jaune)
    bouton_discussion.ajouter_texte("Discussion", 5, 30, 20, rouge)
    bouton_plus = robot.creer_bouton(180, 40, 200, 200, rouge)
    bouton_plus.ajouter_texte("suite du texte", 10, 10, 20, noir)

def verifier_boutons():
    global mettre_a_jour_affichage, paroles_index, zone
    if bouton_menu.verifier_contact():
        zone = "menu"
        mettre_a_jour_affichage = True
    if bouton_quitter.verifier_contact():
        robot.eteindre_ecran()
    if bouton_discussion.verifier_contact():
        zone = "discussion"
        mettre_a_jour_affichage = True
    if bouton_plus.verifier_contact():
        paroles_index = paroles_index + 1
        if paroles_index == len(paroles_robot):
            paroles_index = 0
        mettre_a_jour_affichage = True

def affichage_ecran():
    global mettre_a_jour_affichage
    if mettre_a_jour_affichage:
        if zone == "menu":
            robot.couleur_fond(rouge_sombre)
        else:
            robot.couleur_fond(bleu_sombre)
        robot.afficher_fond()
        bouton_menu.afficher()
        bouton_quitter.afficher()
        if zone == "menu":
            bouton_discussion.afficher()
        if zone == "discussion":
            robot.dessiner_rectangle(700, 100, 150, 50, blanc)
            robot.afficher_texte(paroles_robot[paroles_index], 150, 80, 20)
            bouton_plus.afficher()
        mettre_a_jour_affichage = False

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