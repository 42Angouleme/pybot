from pybot import Robot, Couleur


# --- GENERAL ---
robot = Robot()
robot.demarrer_webapp()
mettre_a_jour_affichage = True
largeur_fenetre = 1200
hauteur_fenetre = 500
discussion_commencer = False


# --- FENETRE ---
# - Preparation -
robot.creer_fenetre(largeur_fenetre, hauteur_fenetre)
robot.couleur_fond(Couleur.NOIR)
robot.changer_titre("Bonjour Robot!")

# - Boucle -
def boucle_fenetre():
    global mettre_a_jour_affichage, session_ouverte
    if mettre_a_jour_affichage:
        robot.afficher_fond()
        bouton_question.afficher()
        bouton_stop.afficher()
        if (discussion_commencer):
            text_area.afficher()
        mettre_a_jour_affichage = False


# --- EVENEMENTS ---
# - Preparation -
robot.ajouter_evenement("echap", "stop")
robot.ajouter_evenement("C", "C")

# - Boucle -
def boucle_evenements():
    events = robot.verifier_evenements()
    if "stop" in events:
        robot.fermer_fenetre()
    if "C" in events:
        print("Vous appuyez sur C")


# --- BOUTONS ---
# - Preparation -
bouton_question = robot.creer_bouton(200, 60, 10, 200, Couleur.CYAN)
bouton_question.ajouter_texte("Poser question", 5, 20)
bouton_stop = robot.creer_bouton(200, 60, 10, 300, Couleur.ROUGE)
bouton_stop.ajouter_texte("Quitter", 10, 10, 20)
text_area = robot.creer_zone_texte(400, 100, 600, 200, Couleur.GRIS)
text_area_bis = robot.creer_zone_texte(400, 100, 600, 350, Couleur.GRIS)
text_area.modifier_couleur_police(Couleur.VERT_SAPIN)

# - Boucle -
def boucle_boutons():
    global mettre_a_jour_affichage, discussion_commencer, text_area, text_area_bis
    if bouton_question.est_actif():
        discussion_commencer = not discussion_commencer
        if discussion_commencer:
            robot.demarrer_discussion()
            bouton_question.ajouter_texte("Arreter la discussion")
        else:
            bouton_question.ajouter_texte("Poser question")
            robot.arreter_discussion()
        mettre_a_jour_affichage = True
    if bouton_stop.est_actif():
        robot.desactiver()
    if discussion_commencer and text_area.est_actif():
        texte_utilisateur = robot.ecrire(text_area)
        # robot.repondre_question(texte_utilisateur)
    if discussion_commencer and text_area_bis.est_actif():
        texte_utilisateur = robot.ecrire(text_area_bis)
        text_area_bis.effacer_texte()
        # robot.repondre_question(texte_utilisateur)


if __name__ == "__main__":
    while robot.est_actif():
        boucle_evenements()
        boucle_fenetre()
        boucle_boutons()
        robot.actualiser_affichage()
