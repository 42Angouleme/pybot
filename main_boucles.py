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

    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    boutons = robot.attributs.boutons

    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()

        texte = "Création Utilisateur"
        x, y = aligner_texte(texte, 30)
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        boutons.retour.afficher()
        
        robot.attributs.mettre_a_jour_affichage = False

def boucle_affichage_fenetre_connexion():

    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    boutons = robot.attributs.boutons

    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()

        texte = "Connexion Utilisateur"
        x, y = aligner_texte(texte, 30)
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        boutons.retour.afficher()
        
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
        robot.dort(0.15)

    if boutons.creation.est_actif():
        robot.attributs.page = 2
        robot.attributs.mettre_a_jour_affichage = True
        robot.dort(0.15)

def boucle_boutons_fenetre_creation():
    boutons = robot.attributs.boutons

    if boutons.retour.est_actif():
        robot.attributs.page = 0
        robot.attributs.mettre_a_jour_affichage = True
        robot.dort(0.15)

def boucle_boutons_fenetre_connexion():
    boutons = robot.attributs.boutons

    if boutons.retour.est_actif():
        robot.attributs.page = 0
        robot.attributs.mettre_a_jour_affichage = True
        robot.dort(0.15)


# --- UTILITAIRE ---
def aligner_texte(texte, taille_police, alignement="centre_haut"):
    taille_texte = robot.fenetre.obtenir_taille_texte(texte, taille_police)
    taille_lettre = robot.fenetre.obtenir_taille_texte(" ", taille_police)
    if alignement == "centre_haut" :
        x = (largeur_fenetre - taille_texte[0] + taille_lettre[0]) // 2
        y = 20
    else:
        x = 0
        y = 0
    return x, y