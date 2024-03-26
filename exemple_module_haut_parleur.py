# import time
# from pybot.module_haut_parleur import HautParleur


# haut_parleur = HautParleur()

# haut_parleur.charger_voix("femme")
# haut_parleur.charger_voix("homme")

# haut_parleur.utiliser_voix("femme")

# phrase = """Maître Corbeau, sur un arbre perché, tenait en son bec un fromage."""

# haut_parleur.dire(phrase)

# while haut_parleur.lecture_en_cours:
#     time.sleep(1)

# haut_parleur.utiliser_voix("homme")
# haut_parleur.dire(phrase)

from pybot.module_fenetre.Interface import Button, TextArea
from pybot import Robot, Couleur

# --- GENERAL ---
robot = Robot()
robot.demarrer_webapp()
mettre_a_jour_affichage = True
largeur_fenetre = 1000
hauteur_fenetre = 500
discussion_commencer = False

robot.initialiser_module_fenetre()
robot.initialiser_module_haut_parleur()

# --- FENETRE ---
# - Preparation -
robot.fenetre.ouvrir_fenetre(largeur_fenetre, hauteur_fenetre)
robot.fenetre.change_background_color(Couleur.NOIR)
robot.fenetre.changer_titre("Bonjour Robot!")

# --- LECTEUR ---
# - Preparation -
robot.haut_parleur.charger_voix("homme")
robot.haut_parleur.utiliser_voix("homme")

# - Boucle -


def boucle_fenetre():
    global mettre_a_jour_affichage
    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()
        bouton_question.afficher()
        bouton_stop.afficher()
        if (discussion_commencer):
            text_area.afficher()
        mettre_a_jour_affichage = False


# --- EVENEMENTS ---
# - Preparation -
robot.ajouter_evenement("echap", "stop")

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
    300, 60, 10, 200, Couleur.CYAN)
bouton_question.ajouter_texte("Faire dire une phrase", 5, 20)
bouton_stop: Button = robot.fenetre.creer_bouton(
    200, 60, 10, 300, Couleur.ROUGE)
bouton_stop.ajouter_texte("Quitter", 10, 10, 20)
text_area: TextArea = robot.fenetre.creer_zone_de_texte(
    400, 100, 400, 200, Couleur.GRIS)
text_area.modifier_couleur_police(Couleur.VERT_SAPIN)

# - Boucle -


def boucle_boutons():
    global mettre_a_jour_affichage, discussion_commencer, text_area
    if bouton_question.est_actif():
        discussion_commencer = not discussion_commencer
        if discussion_commencer:
            bouton_question.ajouter_texte("Arreter de faire dire une phrase")
        else:
            bouton_question.ajouter_texte("Faire dire une phrase")
        mettre_a_jour_affichage = True
    if bouton_stop.est_actif():
        robot.desactiver()
    if discussion_commencer and text_area.est_actif():
        texte_utilisateur = text_area.ecrire(robot)
        robot.haut_parleur.dire(texte_utilisateur)
        while robot.haut_parleur.lecture_en_cours:
            robot.dort(1)


if __name__ == "__main__":
    while robot.est_actif():
        boucle_evenements()
        boucle_fenetre()
        boucle_boutons()
        robot.fenetre.actualiser_affichage()
