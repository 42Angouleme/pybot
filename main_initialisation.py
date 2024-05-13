from pybot import Robot, Couleur

# --- GENERAL ---

robot = Robot()
robot.demarrer_webapp()

# --- ATTRIBUTS ---
robot.attributs.mettre_a_jour_affichage = True
robot.attributs.plein_ecran = False
robot.attributs.page = 0

largeur_fenetre = 1900
hauteur_fenetre = 1000

# --- FENETRE ---

def initialiser_fenetre():
    robot.initialiser_module_fenetre()
    robot.fenetre.ouvrir_fenetre(largeur_fenetre, hauteur_fenetre)
    robot.fenetre.changer_couleur_fond(Couleur.NOIR)
    robot.fenetre.changer_titre("Demo Pybot")
    robot.fenetre.plein_ecran(robot.attributs.plein_ecran)

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
    robot.ajouter_evenement("p", "plein_ecran")

# --- BOUTONS ---

def initialiser_boutons():
    boutons = robot.attributs.boutons

    boutons.quitter = creation_bouton("Quitter", Couleur.ROUGE, 200, 60, 20, "bas_droit")
    boutons.connexion = creation_bouton("Connexion", Couleur.VERT, 200, 60, 20, "centre_droit")
    boutons.creation = creation_bouton("Créer utilisateur", Couleur.BLEU_CIEL, 200, 60, 20, "centre_gauche")

# --- UTILITAIRE ---

def creation_bouton(texte, couleur, longueur, hauteur, taille_texte, alignement="centre_haut"):
    x, y = aligner_bouton(longueur, hauteur, alignement)
    bouton = robot.fenetre.creer_bouton(
        longueur, hauteur, x, y, couleur)
    x, y = centrer_texte_dans_bouton(texte, taille_texte, longueur, hauteur)
    bouton.ajouter_texte(texte, x, y, taille_texte)
    return bouton

def aligner_bouton(longueur_bouton, hauteur_bouton, alignement="centre_haut"):
    if alignement == "centre_haut":
        x = (largeur_fenetre - longueur_bouton) // 2
        y = 20
    elif alignement == "centre_bas":
        x = (largeur_fenetre - longueur_bouton) // 2
        y = hauteur_fenetre - hauteur_bouton - 20
    elif alignement == "centre":
        x = (largeur_fenetre - longueur_bouton) // 2
        y = (hauteur_fenetre - hauteur_bouton) // 2
    elif alignement == "centre_gauche":
        x = 20
        y = (hauteur_fenetre - hauteur_bouton) // 2
    elif alignement == "centre_droit":
        x = largeur_fenetre - longueur_bouton - 20
        y = (hauteur_fenetre - hauteur_bouton) // 2
    elif alignement == "bas_droit":
        x = largeur_fenetre - longueur_bouton - 20
        y = hauteur_fenetre - hauteur_bouton - 20
    elif alignement == "bas_gauche":
        x = 20
        y = hauteur_fenetre - hauteur_bouton - 20
    else:
        x = 0
        y = 0
    return x, y

def centrer_texte_dans_bouton(texte, taille_police, longueur_bouton, hauteur_bouton):
    taille_texte = robot.fenetre.obtenir_taille_texte(texte, taille_police)
    x = (longueur_bouton - taille_texte[0]) // 2
    y = (hauteur_bouton - taille_texte[1]) // 2
    return x, y