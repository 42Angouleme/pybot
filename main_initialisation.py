from pybot import Robot, Couleur

# --- GENERAL ---

robot = Robot()
robot.demarrer_webapp()

# --- ATTRIBUTS ---
robot.attributs.derniere_carte_detectee = None
robot.attributs.mettre_a_jour_affichage = True
robot.attributs.manque_information = False
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

    # --- FENETRE TITRE ---
    boutons.quitter = creation_bouton("Quitter", Couleur.ROUGE, 200, 60, 20, "bas_droit")
    boutons.connexion = creation_bouton("Connexion", Couleur.VERT, 200, 60, 20, "centre_droit")
    boutons.creation = creation_bouton("Créer utilisateur", Couleur.BLEU_CIEL, 200, 60, 20, "centre_gauche")

    # --- BOUTON RETOUR ---
    boutons.retour = creation_bouton("Retour", Couleur.ORANGE, 200, 60, 20, "bas_droit")

    # --- BOUTON DECONNEXION ---
    boutons.deconnexion = creation_bouton("Deconnexion", Couleur.ORANGE, 200, 60, 20, "bas_droit")

# --- ZONES DE TEXTE ---

def initialiser_zones_de_texte():
    zones_de_texte = robot.attributs.zones_de_texte

    x, y = aligner_elements(350, 60, "droit_centre")
    x -= 30
    y -= 130
    zones_de_texte.nom = robot.fenetre.creer_zone_de_texte(350, 60, x, y, Couleur.GRIS)
    zones_de_texte.nom.modifier_taille_police(30)
    
    x, y = aligner_elements(350, 60, "droit_centre")
    x -= 30
    y += 70
    zones_de_texte.prenom = robot.fenetre.creer_zone_de_texte(350, 60, x, y, Couleur.GRIS)
    zones_de_texte.prenom.modifier_taille_police(30)

# --- UTILITAIRE ---

def creation_bouton(texte, couleur, longueur, hauteur, taille_texte, alignement="centre_haut"):
    x, y = aligner_elements(longueur, hauteur, alignement)
    bouton = robot.fenetre.creer_bouton(
        longueur, hauteur, x, y, couleur)
    x, y = centrer_texte_dans_bouton(texte, taille_texte, longueur, hauteur)
    bouton.ajouter_texte(texte, x, y, taille_texte)
    return bouton

def aligner_elements(longueur_bouton, hauteur_bouton, alignement="centre_haut"):
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
    elif alignement == "droit_centre":
        x = largeur_fenetre - longueur_bouton
        y = (hauteur_fenetre - hauteur_bouton) // 2
    else:
        x = 0
        y = 0
    return x, y

def centrer_texte_dans_bouton(texte, taille_police, longueur_bouton, hauteur_bouton):
    taille_texte = robot.fenetre.obtenir_taille_texte(texte, taille_police)
    x = (longueur_bouton - taille_texte[0]) // 2
    y = (hauteur_bouton - taille_texte[1]) // 2
    return x, y

def creation_zone_de_texte(longueur, hauteur, couleur, alignement="centre_haut"):
    x, y = aligner_elements(longueur, hauteur, alignement)
    zone_de_texte = robot.fenetre.creer_zone_de_texte(longueur, hauteur, x, y, couleur)
    return zone_de_texte