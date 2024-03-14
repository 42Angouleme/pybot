from pybot import Robot, Couleur


# --- GENERAL ---
robot = Robot()
robot.demarrer_webapp()
robot.attributs.mettre_a_jour_affichage = True
robot.attributs.discussion_commencee = False
largeur_fenetre = 1200
hauteur_fenetre = 500

# --- FENETRE ---


def initialiser_fenetre():
    robot.initialiser_module_fenetre()
    robot.fenetre.ouvrir_fenetre(largeur_fenetre, hauteur_fenetre)
    robot.fenetre.changer_couleur_fond(Couleur.NOIR)

# --- EVENEMENTS ---


def initialiser_evenements():
    robot.ajouter_evenement("echap", "stop")

# --- SESSION ---


def initialiser_session():
    robot.initialiser_module_camera()
    robot.initialiser_module_utilisateur()
    robot.initialiser_module_IA()
    robot.attributs.derniere_carte_detectee = None
    robot.attributs.session_ouverte = False


# --- BOUTONS ---
def initialiser_boutons():
    boutons = robot.attributs.boutons
    boutons.deconnexion = robot.fenetre.creer_bouton(
        200, 60, 980, 200, Couleur.ORANGE)
    boutons.deconnexion.ajouter_texte("Deconnexion", 5, 20)
    boutons.suppression = robot.fenetre.creer_bouton(
        200, 60, 980, 300, Couleur.ROUGE)
    boutons.suppression.ajouter_texte("Supprimer utilisateur", 5, 20)
    boutons.creation = robot.fenetre.creer_bouton(
        200, 60, 980, 100, Couleur.VERT)
    boutons.creation.ajouter_texte("Créer  utilisateur", 20, 20)
    # IA
    boutons.question = robot.fenetre.creer_bouton(
        200, 60, 50, 200, Couleur.CYAN)
    boutons.question.ajouter_texte("Poser question", 5, 20)
    boutons.texte = robot.fenetre.creer_zone_de_texte(
        220, 50, 40, 300, Couleur.BLANC)
