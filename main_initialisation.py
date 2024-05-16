from pybot import Robot, Couleur

# --- GENERAL ---

robot = Robot()
robot.demarrer_webapp()

# --- ATTRIBUTS ---
robot.attributs.derniere_carte_detectee = None
robot.attributs.mettre_a_jour_affichage = True
robot.attributs.manque_information = False
robot.attributs.plein_ecran = False
robot.attributs.emotion = "neutre"
robot.attributs.question = ""
robot.attributs.reponse = ""
robot.attributs.page = 0

largeur_fenetre = 1900
hauteur_fenetre = 1000

# --- FENETRE ---

def initialiser_fenetre():
    robot.initialiser_module_fenetre()
    robot.fenetre.ouvrir_fenetre(largeur_fenetre, hauteur_fenetre)
    robot.fenetre.changer_couleur_fond(Couleur.BLANC)
    robot.fenetre.changer_titre("Demo Pybot")
    robot.fenetre.plein_ecran(robot.attributs.plein_ecran)

# --- MODULES ---

def initialiser_modules():
    robot.initialiser_module_camera()
    robot.initialiser_module_utilisateur()
    robot.initialiser_module_IA()
    robot.initialiser_module_haut_parleur()
    robot.initialiser_module_microphone()

    robot.haut_parleur.charger_voix("homme")
    robot.haut_parleur.charger_voix("femme")
    robot.haut_parleur.charger_voix("homme_quebec")

# --- EVENEMENTS ---

def initialiser_evenements():
    robot.ajouter_evenement("echap", "stop")
    robot.ajouter_evenement("p", "plein_ecran")

# --- BOUTONS ---

def initialiser_boutons():
    boutons = robot.attributs.boutons

    # --- FENETRE TITRE ---
    boutons.quitter = creation_bouton("Quitter", Couleur.ROUGE, 200, 60, 20, "bas_droit")
    boutons.connexion = creation_bouton("Connexion", Couleur.VERT_SAPIN, 200, 60, 20, "centre_droit")
    boutons.creation = creation_bouton("Créer utilisateur", Couleur.VIOLET, 200, 60, 20, "centre_gauche")

    # --- BOUTON RETOUR ---
    boutons.retour = creation_bouton("Retour", Couleur.ORANGE, 200, 60, 20, "bas_droit")

    # --- FENETRE CREATION ---
    boutons.creer = creation_bouton("Créer Utilisateur", Couleur.VERT_SAPIN, 200, 60, 20, "centre_bas", 0, -130)
    boutons.deconnexion_creation = creation_bouton("Déconnexion", Couleur.ORANGE, 300, 60, 20, "centre_haut", -170, 100)
    boutons.suppression = creation_bouton("Supprimer Utilisateur", Couleur.ROUGE, 300, 60, 20, "centre_haut", 170, 100)

    # --- FENETRE SESSION ---
    boutons.deconnexion = creation_bouton("Déconnexion", Couleur.ORANGE, 200, 60, 20, "bas_droit")
    boutons.posez_question_orale = creation_bouton("Poser une question à l'oral", Couleur.ROSE, 350, 60, 20, "centre_gauche", 150, -50)
    boutons.posez_question_ecrite = creation_bouton("Poser une question à l'écrit", Couleur.VIOLET, 350, 60, 20, "centre_gauche", 150, 50)
    boutons.supprimer_historique = creation_bouton("Supprimer Historique", Couleur.ROUGE, 350, 60, 20, "bas_gauche")

    boutons.charger_voix_homme = creation_bouton("Voix Homme", Couleur.BLEU_CIEL, 200, 60, 20, "centre_bas", -225, -75)
    boutons.charger_voix_femme = creation_bouton("Voix Femme", Couleur.BLEU_CIEL, 200, 60, 20, "centre_bas", 0, -75)
    boutons.charger_voix_quebecoise = creation_bouton("Voix Québécoise", Couleur.BLEU_CIEL, 200, 60, 20, "centre_bas", 225, -75)


# --- ZONES DE TEXTE ---

def initialiser_zones_de_texte():
    zones_de_texte = robot.attributs.zones_de_texte

    zones_de_texte.nom = creation_zone_de_texte(350, 60, Couleur.GRIS, "droit_centre", -30, -130)
    zones_de_texte.nom.modifier_taille_police(30)
    
    zones_de_texte.prenom = creation_zone_de_texte(350, 60, Couleur.GRIS, "droit_centre", -30, 70)
    zones_de_texte.prenom.modifier_taille_police(30)

    zones_de_texte.question = creation_zone_de_texte(500, 120, Couleur.GRIS, "centre_gauche", 150, 150)
    zones_de_texte.question.modifier_taille_police(18)

# --- UTILITAIRE ---

def creation_bouton(texte, couleur, longueur, hauteur, taille_texte, alignement="centre_haut", modifier_x=0, modifier_y=0):
    x, y = aligner_elements(longueur, hauteur, alignement)
    x += modifier_x
    y += modifier_y
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

def creation_zone_de_texte(longueur, hauteur, couleur, alignement="centre_haut", modifier_x=0, modifier_y=0):
    x, y = aligner_elements(longueur, hauteur, alignement)
    x += modifier_x
    y += modifier_y
    zone_de_texte = robot.fenetre.creer_zone_de_texte(longueur, hauteur, x, y, couleur)
    return zone_de_texte