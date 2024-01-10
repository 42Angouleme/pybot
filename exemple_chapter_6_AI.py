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

bouton_question = None
bouton_stop = None

discussion_commencer = False

mettre_a_jour_affichage = True

texte = ""

def preparer_programme():
    global bouton_question, bouton_stop
    robot.allumer_ecran(long, haut)
    robot.changer_titre("Bonjour Robot!")
    robot.couleur_fond(noir)
    robot.ajouter_evenement("echap", "stop")
    bouton_question = robot.creer_bouton(200, 60, 10, 10, bleu)
    bouton_question.ajouter_texte("Poser question", 5, 20)
    bouton_stop = robot.creer_bouton(200, 60, 10, 900, vert)
    bouton_stop.ajouter_texte("Quitter", 10, 10, 20)
    robot.ajouter_evenement("C", "carotte")

def affichage_ecran():  
    global mettre_a_jour_affichage, texte
    if mettre_a_jour_affichage:
        robot.afficher_fond()
        bouton_question.afficher()
        bouton_stop.afficher()
        robot.afficher_texte(texte, 150, 80, 10, blanc)
        mettre_a_jour_affichage = False

def verifier_boutons(robot : Robot):
    global mettre_a_jour_affichage, discussion_commencer, texte
    if bouton_question.verifier_contact():
        discussion_commencer = not discussion_commencer
        if discussion_commencer :
            robot.demarrer_discussion()
            bouton_question.ajouter_texte("Arreter la discussion")
        else :
            texte = ""
            bouton_question.ajouter_texte("Poser question")
            robot.arreter_discussion()
        mettre_a_jour_affichage = True
    if bouton_stop.verifier_contact():
        robot.desactiver()

def boucle_programme():
    global discussion_commencer, mettre_a_jour_affichage, texte
    while robot.est_actif():
        events = robot.verifier_evenements()
        if "stop" in events:
            robot.eteindre_ecran()
        elif "carotte" in events:
            print("Vous appuyer sur C")
        affichage_ecran()
        verifier_boutons(robot)
        if discussion_commencer :
            new_texte = robot.recuperer_entree_utilisateur(texte)
            if (new_texte != texte) :
                texte = new_texte
                if ("\r" in texte) :
                    robot.repondre_question(texte)
                    texte = ""
                mettre_a_jour_affichage = True
        robot.dessiner_ecran()

if __name__ == "__main__":
    preparer_programme()
    boucle_programme()