from pybot import Robot, Couleur


# --- GENERAL ---
robot = Robot()
robot.demarrer_webapp()
robot.attributs.mettre_a_jour_affichage = True
robot.attributs.discussion_commencee = False
robot.attributs.image_emotion = "/images/emotions/amuser.png"
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


def initialiser_audio():
    robot.initialiser_module_microphone()
    robot.initialiser_module_haut_parleur()
    robot.haut_parleur.charger_voix("homme")
    robot.haut_parleur.utiliser_voix("homme")

# --- BOUTONS ---


def initialiser_boutons():
    boutons = robot.attributs.boutons

    boutons.deconnexion = robot.fenetre.creer_bouton(
        200, 60, 1000, 440, Couleur.ORANGE)
    boutons.deconnexion.ajouter_texte("Deconnexion", 5, 20)

    boutons.question = robot.fenetre.creer_bouton(
        200, 60, 0, 440, Couleur.CYAN)
    boutons.question.ajouter_texte("Parler", 5, 20)

    boutons.texte = robot.fenetre.creer_zone_de_texte(
        800, 450, 200, 50, Couleur.BLANC)
