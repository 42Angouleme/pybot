from pybot import Robot
robot = Robot()


def afficher_camera():
    robot.supprimer_bouton("Afficher camera")
    robot.supprimer_bouton("Afficher photo")
    robot.supprimer_bouton("Quitter robot")
    robot.ajouter_bouton("Enregistrer photo", robot.enregistrer_photo)
    robot.ajouter_bouton("Eteindre camera", eteindre_camera)
    robot.afficher_camera()


def eteindre_camera():
    robot.supprimer_bouton("Enregistrer photo")
    robot.supprimer_bouton("Eteindre camera")
    robot.ajouter_bouton("Quitter robot", robot.eteindre_ecran)
    robot.ajouter_bouton("Afficher photo", afficher_photo)
    robot.ajouter_bouton("Afficher camera", afficher_camera)
    robot.eteindre_camera()


def photo_boutons():
    robot.ajouter_bouton("Filtre NB", robot.appliquer_filtre_noir_et_blanc)
    robot.ajouter_bouton("Filtre Amour", robot.appliquer_filtre_amour)
    robot.ajouter_bouton("Tourner Photo", robot.tourner_photo)

def afficher_photo():
    if robot.verifier_photo():
        robot.afficher_photo()
    else:
        robot.afficher_visage_triste()

def supprimer_photo():
    if robot.verifier_photo():
        robot.supprimer_photo()
    else:
        robot.afficher_visage_colere()

def lancer_robot():
    longueur = 1024
    hauteur = 800

    robot.allumer_ecran(longueur, hauteur)
    robot.changer_titre("Exemple 3")

    robot.ajouter_bouton("Quitter robot", robot.eteindre_ecran)
    robot.ajouter_bouton("Afficher camera", afficher_camera)
    robot.ajouter_bouton("Afficher photo", afficher_photo)
    robot.ajouter_bouton("Supprimer photo", supprimer_photo)
    photo_boutons()

    robot.lancer_boucle()


lancer_robot()
