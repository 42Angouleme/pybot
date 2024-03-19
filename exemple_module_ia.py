from pybot.module_fenetre.Interface import Button, TextArea
from pybot import Robot, Couleur


# --- GENERAL ---
robot = Robot()
robot.demarrer_webapp()
mettre_a_jour_affichage = True
largeur_fenetre = 1200
hauteur_fenetre = 500
discussion_commencer = False

robot.initialiser_module_fenetre()
robot.initialiser_module_IA()


# --- FENETRE ---
# - Preparation -
robot.fenetre.ouvrir_fenetre(largeur_fenetre, hauteur_fenetre)
robot.fenetre.change_background_color(Couleur.NOIR)
robot.fenetre.changer_titre("Bonjour Robot!")


# - Boucle -
def boucle_fenetre():
    global mettre_a_jour_affichage
    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()
        bouton_question.afficher()
        bouton_stop.afficher()
        if discussion_commencer:
            text_area.afficher()
        mettre_a_jour_affichage = False


# --- EVENEMENTS ---
# - Preparation -
robot.ajouter_evenement("echap", "stop")
robot.ajouter_evenement("C", "C")


# - Boucle -
def boucle_evenements():
    events = robot.check_events()
    if "stop" in events:
        robot.desactiver()
    if "C" in events:
        print("Vous appuyez sur C")


# --- BOUTONS ---
# - Preparation -
bouton_question: Button = robot.fenetre.creer_bouton(
    200, 60, 10, 200, Couleur.CYAN)
bouton_question.ajouter_texte("Poser question", 5, 20)
bouton_stop: Button = robot.fenetre.creer_bouton(
    200, 60, 10, 300, Couleur.ROUGE)
bouton_stop.ajouter_texte("Quitter", 10, 10, 20)
text_area: TextArea = robot.fenetre.creer_zone_de_texte(
    400, 100, 600, 200, Couleur.GRIS)
text_area.modifier_couleur_police(Couleur.VERT_SAPIN)


# - Boucle -
def boucle_boutons():
    global mettre_a_jour_affichage, discussion_commencer
    if bouton_question.est_actif():
        discussion_commencer = not discussion_commencer
        if discussion_commencer:
            robot.IA.demarrer_discussion()
            bouton_question.ajouter_texte("Arreter la discussion")
        else:
            bouton_question.ajouter_texte("Poser question")
            robot.IA.arreter_discussion()
        mettre_a_jour_affichage = True
    if bouton_stop.est_actif():
        robot.desactiver()
    if discussion_commencer and text_area.est_actif():
        texte_utilisateur = text_area.ecrire(robot)
        réponse = robot.IA.poser_question(texte_utilisateur)
        print(réponse)
        emotion = robot.IA.donner_emotion(réponse)
        image = robot.fenetre.obtenir_image_emotion(emotion)
        robot.fenetre.afficher_image(image, 300, 300)


if __name__ == "__main__":
    while robot.est_actif():
        boucle_evenements()
        boucle_fenetre()
        boucle_boutons()
        robot.fenetre.actualiser_affichage()
