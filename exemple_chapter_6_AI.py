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
text_area = None
text_area_bis = None

discussion_commencer = False

mettre_a_jour_affichage = True

def preparer_programme():
    global bouton_question, bouton_stop, text_area, text_area_bis
    robot.allumer_ecran(long, haut)
    robot.changer_titre("Bonjour Robot!")
    robot.couleur_fond(noir)
    robot.ajouter_evenement("echap", "stop")
    bouton_question = robot.creer_bouton(200, 60, 10, 10, bleu)
    bouton_question.ajouter_texte("Poser question", 5, 20)
    bouton_stop = robot.creer_bouton(200, 60, 10, 900, vert)
    bouton_stop.ajouter_texte("Quitter", 10, 10, 20)
    text_area = robot.creer_zone_texte(600, 100, 300, 250, blanc)
    text_area_bis = robot.creer_zone_texte(600, 100, 300, 400, blanc)
    text_area.modifier_couleur_ecriture(vert)
    robot.ajouter_evenement("C", "C")

def affichage_ecran():  
    global mettre_a_jour_affichage, discussion_commencer, text_area, text_area_bis
    if mettre_a_jour_affichage:
        robot.afficher_fond()
        bouton_question.afficher()
        bouton_stop.afficher()
        if (discussion_commencer) :
            text_area.afficher()
            text_area_bis.afficher()
        mettre_a_jour_affichage = False

def verifier_boutons(robot : Robot):
    global mettre_a_jour_affichage, discussion_commencer, text_area, text_area_bis
    if bouton_question.verifier_contact():
        discussion_commencer = not discussion_commencer
        if discussion_commencer :
            robot.demarrer_discussion()
            bouton_question.ajouter_texte("Arreter la discussion")
        else :
            bouton_question.ajouter_texte("Poser question")
            robot.arreter_discussion()
        mettre_a_jour_affichage = True
    if bouton_stop.verifier_contact():
        robot.desactiver()
    if discussion_commencer and text_area.verifier_contact() :
        user_entry = robot.ecrire(text_area)
        print("user_entry = ", user_entry)
        #robot.repondre_question(user_entry)
    if discussion_commencer and text_area_bis.verifier_contact() :
        user_entry = robot.ecrire(text_area_bis)
        print("user_entry = ", user_entry)
        text_area_bis.effacer_text()
        #robot.repondre_question(user_entry)

def boucle_programme():
    global discussion_commencer, mettre_a_jour_affichage
    while robot.est_actif():
        events = robot.verifier_evenements()
        if "stop" in events:
            robot.eteindre_ecran()
        elif "C" in events:
            print("Vous appuyez sur C")
        affichage_ecran()
        verifier_boutons(robot)
        robot.dessiner_ecran()

if __name__ == "__main__":
    preparer_programme()
    boucle_programme()

"""
To DO :
    Faire la documentation sur le site.
    Avoir plus de flexibilité sur la personalisation de la zone de texte

    Truc à dire dans la documentation sur le site :
    La fonction ecrire, bloque le fonctionnement du robot en général.
    Préciser que l'on arrete d'écrire si on tape sur entrée ou que l'on clique à nouveau sur la zone de texte
    Préciser que la fonction repondre_question bloque le robot le temps qu'il "réfléchisse", et qu'elle imprime la réponse dans le terminal.
    Préciser qu'il faut mettre une petite taille d'écriture

    S'occuper de pouvoir sortir de la zone de texte en cliquant à l'exterieur
"""