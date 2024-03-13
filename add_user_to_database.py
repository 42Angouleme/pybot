from pybot.module_fenetre.Interface import Button
from pybot import Robot, Couleur


# --- GENERAL ---
robot = Robot()
robot.demarrer_webapp()

largeur_fenetre = 1200
hauteur_fenetre = 800

robot.attributs.mettre_a_jour_affichage = True
robot.attributs.manque_information = False

## initialiser ##


def initialiser_module():
    robot.initialiser_module_fenetre()
    robot.fenetre.ouvrir_fenetre(largeur_fenetre, hauteur_fenetre)
    robot.initialiser_module_camera()
    robot.initialiser_module_utilisateur()


def parametrer_fenetre():
    robot.fenetre.changer_couleur_fond(Couleur.NOIR)
    robot.fenetre.changer_titre("Ajouter un utilisateur")


def initialiser_evenements():
    robot.ajouter_evenement("echap", "stop")
    robot.ajouter_evenement("espace", "photo")


def initialiser_boutons():
    boutons = robot.attributs.boutons
    boutons.creation = robot.fenetre.creer_bouton(
        200, 60, 980, 70, Couleur.CYAN)
    boutons.creation.ajouter_texte("Créer  utilisateur", 20, 20)

    boutons.deconnexion = robot.fenetre.creer_bouton(
        200, 60, 360, 510, Couleur.ORANGE)
    boutons.deconnexion.ajouter_texte("Deconnexion", 5, 20)

    boutons.suppression = robot.fenetre.creer_bouton(
        200, 60, 670, 510, Couleur.ROUGE)
    boutons.suppression.ajouter_texte("Supprimer utilisateur", 5, 20)


def initialiser_session():
    robot.attributs.session_ouverte = False
    robot.attributs.derniere_carte_detectee = None


def initialiser_zone_de_texte():
    zones_de_texte = robot.attributs.zones_de_texte

    zones_de_texte.nom = robot.fenetre.creer_zone_de_texte(
        200, 60, 980, 200, Couleur.GRIS)

    zones_de_texte.prenom = robot.fenetre.creer_zone_de_texte(
        200, 60, 980, 400, Couleur.GRIS)

## BOUCLES ##


def boucle_evenements():
    zones_de_texte = robot.attributs.zones_de_texte
    events = robot.verifier_evenements()
    if "stop" in events:
        robot.desactiver()
    if "photo" in events:
        nom = zones_de_texte.nom.obtenir_texte()
        prenom = zones_de_texte.prenom.obtenir_texte()
        if not nom or not prenom or robot.attributs.derniere_carte_detectee is None:
            robot.attributs.manque_information = True
            robot.attributs.mettre_a_jour_affichage = True
            robot.attributs.derniere_carte_detectee = None
            return

        robot.utilisateur.creer_utilisateur(
            nom, prenom, robot.attributs.derniere_carte_detectee)
        zones_de_texte.nom.effacer_texte()
        zones_de_texte.prenom.effacer_texte()
        robot.attributs.derniere_carte_detectee = None
        # affichage d'un message de succès dans la fenêtre
        # ou affichage d'un message de succès dans le terminal
        robot.attributs.mettre_a_jour_affichage = True


def boucle_zone_de_texte():
    zones_de_texte = robot.attributs.zones_de_texte
    if zones_de_texte.nom.est_actif():
        zones_de_texte.nom.ecrire(robot)
    if zones_de_texte.prenom.est_actif():
        zones_de_texte.prenom.ecrire(robot)


def boucle_d_affichage():
    bouttons = robot.attributs.boutons
    zones_de_texte = robot.attributs.zones_de_texte
    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    robot.camera.afficher_camera(300, 10)
    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()
        if robot.attributs.manque_information:
            robot.attributs.manque_information = False
            robot.fenetre.afficher_texte(
                "Veuillez remplir tous les champs", 360, 510, 20, Couleur.ROUGE)
        if robot.attributs.session_ouverte:
            bouttons.deconnexion.afficher()
            bouttons.suppression.afficher()
            user = robot.utilisateur.obtenir_utilisateur_connecte()
            robot.fenetre.afficher_texte(user.nom, 25, 200, 30, Couleur.BLANC)
            robot.fenetre.afficher_texte(
                user.prenom, 25, 300, 30, Couleur.BLANC)
        else:
            bouttons.creation.afficher()
            robot.fenetre.afficher_texte("Nom", 980, 150, 20, Couleur.BLANC)
            zones_de_texte.nom.afficher()
            robot.fenetre.afficher_texte("Prenom", 980, 350, 20, Couleur.BLANC)
            zones_de_texte.prenom.afficher()

        robot.fenetre.afficher_texte("PROFIL", 80, 5, 30, Couleur.BLANC)
        robot.fenetre.afficher_texte("CREATION", 1000, 5, 30, Couleur.BLANC)

        robot.attributs.mettre_a_jour_affichage = False


def boucle_session():
    if not robot.attributs.session_ouverte:
        # Essai de connexion
        robot.utilisateur.connecter()
        if robot.utilisateur.verifier_session():
            user = robot.utilisateur.obtenir_utilisateur_connecte()
            print(f"Hello \033[96;1m{user.prenom} {user.nom}\033[0;0m !")
        else:
            # Affichage de carte détéctée non connectée
            carte_detectee = robot.utilisateur.detecter_carte()
            if carte_detectee:
                robot.fenetre.afficher_carte_detectee(carte_detectee, 60, 150)
                robot.attributs.derniere_carte_detectee = carte_detectee


def boucle_boutons():
    bouttons = robot.attributs.boutons
    zones_de_texte = robot.attributs.zones_de_texte

    if robot.utilisateur.verifier_session() != robot.attributs.session_ouverte:
        robot.attributs.session_ouverte = robot.utilisateur.verifier_session()
        robot.attributs.mettre_a_jour_affichage = True
    elif robot.attributs.session_ouverte:
        if bouttons.suppression.est_actif():
            robot.utilisateur.supprimer_utilisateur()
            robot.attributs.session_ouverte = False
            robot.attributs.mettre_a_jour_affichage = True
        if bouttons.deconnexion.est_actif():
            robot.utilisateur.deconnecter()
            robot.attributs.session_ouverte = False
            robot.attributs.mettre_a_jour_affichage = True

    if bouttons.creation.est_actif():
        nom = zones_de_texte.nom.obtenir_texte()
        prenom = zones_de_texte.prenom.obtenir_texte()
        if not nom or not prenom or robot.attributs.derniere_carte_detectee is None:
            robot.attributs.manque_information = True
            robot.attributs.mettre_a_jour_affichage = True
            robot.attributs.derniere_carte_detectee = None
            return

        robot.utilisateur.creer_utilisateur(
            nom, prenom, robot.attributs.derniere_carte_detectee)
        zones_de_texte.nom.effacer_texte()
        zones_de_texte.prenom.effacer_texte()
        robot.attributs.derniere_carte_detectee = None
        robot.attributs.mettre_a_jour_affichage = True


if __name__ == "__main__":
    initialiser_module()
    parametrer_fenetre()
    initialiser_session()
    initialiser_evenements()
    initialiser_boutons()
    initialiser_zone_de_texte()

    while robot.est_actif():
        boucle_zone_de_texte()
        boucle_evenements()
        boucle_boutons()
        boucle_session()
        boucle_d_affichage()
        robot.fenetre.actualiser_affichage()
