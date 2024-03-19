from pybot.module_fenetre.Interface import Button
from pybot import Robot, Couleur


# --- GENERAL ---
robot = Robot()
robot.demarrer_webapp()
mettre_a_jour_affichage = True
largeur_fenetre = 1200
hauteur_fenetre = 500

robot.demarrer_module_fenetre()

# --- FENETRE ---
# - Preparation -
robot.fenetre.ouvrir_fenetre(largeur_fenetre, hauteur_fenetre)
robot.demarrer_module_camera()
robot.demarrer_module_utilisateur()
robot.fenetre.changer_couleur_fond(Couleur.NOIR)

# - Boucle -
def boucle_fenetre():
    global mettre_a_jour_affichage
    robot.camera.afficher_camera(300, 10)
    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()
        if robot.attributs.session_ouverte:
            bouton_deconnexion.afficher()
            bouton_suppression.afficher()
        else:
            bouton_creation.afficher()
        robot.fenetre.afficher_texte("PROFIL", 80, 5, 30, (255, 255, 255))
        robot.fenetre.afficher_texte("CREATION", 1000, 5, 30, (255, 255, 255))
        mettre_a_jour_affichage = False


# --- SESSION ---
# - Preparation -
def initialisation_session():
    robot.attributs.session_ouverte = False
    robot.attributs.derniere_carte_detectee = None

# --- EVENEMENTS ---
# - Preparation -
robot.ajouter_evenement("echap", "stop")
initialisation_session()

# - Boucle -
def boucle_evenements():
    events = robot.verifier_evenements()
    if "stop" in events:
        robot.desactiver()

# - Boucle -
def boucle_session():
    if not robot.attributs.session_ouverte :
        # Essai de connexion
        robot.utilisateur.connecter()
        if robot.utilisateur.verifier_session():
            user = robot.utilisateur.obtenir_utilisateur_connecte()
            print(f"Hello \033[96;1m{user.prenom} {user.nom}\033[0;0m !")
        else:
            # Affichage de carte détéctée non connectée
            carte_detectee = robot.utilisateur.detecter_carte()
            if carte_detectee:
                robot.fenetre.afficher_carte_detectee(carte_detectee, 980, 200)
                robot.attributs.derniere_carte_detectee = carte_detectee


# --- BOUTONS ---
# - Preparation -
bouton_deconnexion : Button = robot.fenetre.creer_bouton(200, 60, 25, 200, Couleur.ORANGE)
bouton_deconnexion.ajouter_texte("Deconnexion", 5, 20)
bouton_suppression : Button = robot.fenetre.creer_bouton(200, 60, 25, 300, Couleur.ROUGE)
bouton_suppression.ajouter_texte("Supprimer utilisateur", 5, 20)
bouton_creation : Button = robot.fenetre.creer_bouton(200, 60, 980, 100, (0, 150, 0))
bouton_creation.ajouter_texte("Créer  utilisateur", 20, 20)

# - Boucle -
def boucle_boutons():
    global mettre_a_jour_affichage, carte_detectee
    # Mise à jour du status de la session
    if robot.utilisateur.verifier_session() != robot.attributs.session_ouverte:
        robot.attributs.session_ouverte = robot.utilisateur.verifier_session()
        mettre_a_jour_affichage = True
    elif robot.attributs.session_ouverte:
        # Vérification des boutons de session
        if bouton_suppression.est_actif():
            robot.utilisateur.supprimer_utilisateur()
            robot.attributs.session_ouverte = False
            mettre_a_jour_affichage = True
        if bouton_deconnexion.est_actif():
            robot.utilisateur.deconnecter()
            robot.attributs.session_ouverte = False
            mettre_a_jour_affichage = True
    if bouton_creation.est_actif():
        nom_utilisateur = "Ada"
        prenom_utilisateur = "Lovelace"
        robot.utilisateur.creer_utilisateur(prenom_utilisateur,
                                nom_utilisateur,
                                robot.attributs.derniere_carte_detectee)
        robot.attributs.session_ouverte = False
        mettre_a_jour_affichage = True


if __name__ == "__main__":
    while robot.est_actif():
        boucle_evenements()
        boucle_fenetre()
        boucle_session()
        boucle_boutons()
        robot.fenetre.actualiser_affichage()