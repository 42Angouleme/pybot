from pybot import Couleur
from main_initialisation import robot, largeur_fenetre, hauteur_fenetre

# --- AFFICHAGE ---

def boucle_affichage_fenetre_titre():
    robot.fenetre.actualiser_affichage()

    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    boutons = robot.attributs.boutons

    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()

        texte = "Démo Pybot made by"
        x, y = aligner_texte(texte, 30)
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        texte = "42Angoulême & Collège Val de Charente"
        x, y = aligner_texte(texte, 30)
        y += 45
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        boutons.quitter.afficher()
        boutons.connexion.afficher()
        boutons.creation.afficher()

        robot.fenetre.afficher_image("/images/42.png", (largeur_fenetre // 2) - 230, (hauteur_fenetre - 225) // 2)
        robot.fenetre.afficher_image("/images/College_Val_de_Charente.png", (largeur_fenetre // 2) + 5, (hauteur_fenetre - 80) // 2)

        robot.attributs.mettre_a_jour_affichage = False
    
def boucle_affichage_fenetre_creation():
    robot.fenetre.actualiser_affichage()

    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    zones_de_texte = robot.attributs.zones_de_texte
    boutons = robot.attributs.boutons

    robot.camera.afficher_camera((largeur_fenetre - 640) // 2, (hauteur_fenetre - 480) // 2)
    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()

        texte = "Création Utilisateur"
        x, y = aligner_texte(texte, 30)
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        texte = "Nom :"
        x, y = aligner_texte(texte, 30, "droite_centre")
        y -= 150
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        texte = "Prénom :"
        x, y = aligner_texte(texte, 30, "droite_centre")
        y += 50
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        boutons.retour.afficher()
        boutons.creer.afficher()

        zones_de_texte.nom.afficher()
        zones_de_texte.prenom.afficher()
        
        robot.attributs.mettre_a_jour_affichage = False

def boucle_affichage_fenetre_connexion():
    robot.fenetre.actualiser_affichage()

    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    boutons = robot.attributs.boutons

    robot.camera.afficher_camera((largeur_fenetre - 640) // 2, (hauteur_fenetre - 480) // 2)
    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()
    
        texte = "Connexion Utilisateur"
        x, y = aligner_texte(texte, 30)
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        texte = "Veuillez présenter"
        taille_texte = robot.fenetre.obtenir_taille_texte(texte, 30)
        x = ((largeur_fenetre - 640) // 2 - taille_texte[0]) // 2
        y = (hauteur_fenetre - taille_texte[1]) // 2
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        texte = "votre carte"
        taille_texte = robot.fenetre.obtenir_taille_texte(texte, 30)
        x = ((largeur_fenetre - 640) // 2 - taille_texte[0]) // 2
        y = (hauteur_fenetre - taille_texte[1]) // 2 + 45
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        boutons.retour.afficher()
        
        robot.attributs.mettre_a_jour_affichage = False

def boucle_affichage_fenetre_session():
    robot.fenetre.actualiser_affichage()

    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    boutons = robot.attributs.boutons

    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()

        texte = "Session Utilisateur"
        x, y = aligner_texte(texte, 30)
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        boutons.deconnexion.afficher()

        robot.attributs.mettre_a_jour_affichage = False

# --- EVENEMENTS ---
def boucle_evenements():
    events = robot.verifier_evenements()
    if "stop" in events:
        robot.desactiver()
    
    if "plein_ecran" in events:
        robot.attributs.plein_ecran = not robot.attributs.plein_ecran
        robot.fenetre.plein_ecran(robot.attributs.plein_ecran)
        robot.attributs.mettre_a_jour_affichage = True

# --- BOUTONS ---

def boucle_boutons_fenetre_titre():
    boutons = robot.attributs.boutons

    if boutons.quitter.est_actif():
        robot.desactiver()
    
    if boutons.connexion.est_actif():
        robot.attributs.page = 1
        robot.attributs.mettre_a_jour_affichage = True
        robot.camera.demarrer_la_capture_d_image()
        robot.dort(0.15)

    if boutons.creation.est_actif():
        robot.attributs.page = 2
        robot.attributs.mettre_a_jour_affichage = True
        robot.camera.demarrer_la_capture_d_image()
        robot.dort(0.15)

def boucle_boutons_fenetre_creation():
    boutons = robot.attributs.boutons

    if boutons.retour.est_actif():
        robot.attributs.page = 0
        robot.attributs.mettre_a_jour_affichage = True
        robot.attributs.derniere_carte_detectee = None
        robot.camera.arreter_la_capture_d_image()
        robot.dort(0.15)

def boucle_boutons_fenetre_connexion():
    boutons = robot.attributs.boutons

    if boutons.retour.est_actif():
        robot.attributs.page = 0
        robot.attributs.mettre_a_jour_affichage = True
        robot.attributs.derniere_carte_detectee = None
        robot.camera.arreter_la_capture_d_image()
        robot.dort(0.15)

def boucle_boutons_fenetre_session():
    boutons = robot.attributs.boutons

    if boutons.deconnexion.est_actif():
        robot.utilisateur.deconnecter()
        robot.attributs.page = 0
        robot.attributs.mettre_a_jour_affichage = True
        robot.dort(0.15)

# --- ZONES DE TEXTE ---

def boucle_zone_de_texte():
    zones_de_texte = robot.attributs.zones_de_texte

    if zones_de_texte.nom.est_actif():
        zones_de_texte.nom.ecrire(robot)

    if zones_de_texte.prenom.est_actif():
        zones_de_texte.prenom.ecrire(robot)

# --- CONNEXION ---

def boucle_connexion():
    # if not robot.attributs.session_ouverte:
    # Essai de connexion
    robot.utilisateur.connecter()
    if robot.utilisateur.verifier_session():
        user = robot.utilisateur.obtenir_utilisateur_connecte()
        robot.attributs.page = 3
        robot.attributs.mettre_a_jour_affichage = True
        robot.camera.arreter_la_capture_d_image()
    else:
        carte_detectee = robot.utilisateur.detecter_carte()
        if carte_detectee:
            robot.fenetre.afficher_carte_detectee(carte_detectee, (largeur_fenetre - 200) // 2 + 640, (hauteur_fenetre - 200) // 2)
            robot.attributs.derniere_carte_detectee = carte_detectee

def boucle_test_connexion():
    robot.utilisateur.connecter()
    if robot.utilisateur.verifier_session():
        user = robot.utilisateur.obtenir_utilisateur_connecte()
        print(f"Hello \033[96;1m{user.prenom} {user.nom}\033[0;0m !")
    else:
        carte_detectee = robot.utilisateur.detecter_carte()
        if carte_detectee:
            robot.fenetre.afficher_carte_detectee(carte_detectee, ((largeur_fenetre - 640) // 2 - 200) // 2, (hauteur_fenetre - 200) // 2)
            robot.attributs.derniere_carte_detectee = carte_detectee

# --- UTILITAIRE ---

def aligner_texte(texte, taille_police, alignement="centre_haut"):
    taille_texte = robot.fenetre.obtenir_taille_texte(texte, taille_police)
    taille_lettre = robot.fenetre.obtenir_taille_texte(" ", taille_police)
    if alignement == "centre_haut" :
        x = (largeur_fenetre - taille_texte[0] + taille_lettre[0]) // 2
        y = 20
    elif alignement == "centre_bas":
        x = (largeur_fenetre - taille_texte[0] + taille_lettre[0]) // 2
        y = hauteur_fenetre - taille_texte[1] - 20
    elif alignement == "centre":
        x = (largeur_fenetre - taille_texte[0] + taille_lettre[0]) // 2
        y = (hauteur_fenetre - taille_texte[1]) // 2
    elif alignement == "centre_gauche":
        x = 20
        y = (hauteur_fenetre - taille_texte[1]) // 2
    elif alignement == "centre_droit":
        x = largeur_fenetre - taille_texte[0] - 20
        y = (hauteur_fenetre - taille_texte[1]) // 2
    elif alignement == "gauche_centre":
        x = (largeur_fenetre // 2 - taille_texte[0]) // 2
        y = (hauteur_fenetre - taille_texte[1] + taille_lettre[1]) // 2
    elif alignement == "droite_centre":
        x = (largeur_fenetre // 2 - taille_texte[0]) // 2 + largeur_fenetre // 2
        y = (hauteur_fenetre - taille_texte[1] + taille_lettre[1]) // 2
    else:
        x = 0
        y = 0
    return x, y