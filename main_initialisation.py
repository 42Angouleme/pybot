from pybot import Robot, Couleur

# --- GENERAL ---

robot = Robot()
robot.demarrer_webapp()

# --- ATTRIBUTS ---
robot.attributs.mettre_a_jour_affichage = True
robot.attributs.plein_ecran = True
robot.attributs.page = 0

largeur_fenetre = 1900
hauteur_fenetre = 1000

# --- FENETRE ---

def initialiser_fenetre():
    robot.initialiser_module_fenetre()
    robot.fenetre.ouvrir_fenetre(largeur_fenetre, hauteur_fenetre)
    robot.fenetre.changer_couleur_fond(Couleur.NOIR)
    robot.fenetre.changer_titre("Demo Pybot")

# --- MODULES ---

def initialiser_modules():
    robot.initialiser_module_camera()
    robot.initialiser_module_utilisateur()
    robot.initialiser_module_IA()
    robot.initialiser_module_haut_parleur()
    robot.initialiser_module_microphone()

# --- EVENEMENTS ---

def initialiser_evenements():
    robot.ajouter_evenement("echap", "stop")

