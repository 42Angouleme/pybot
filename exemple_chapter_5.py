from pybot import Robot, Couleur


# --- GENERAL ---
robot = Robot()
robot.demarrer_webapp()
mettre_a_jour_affichage = True
largeur_fenetre = 1200
hauteur_fenetre = 500
session_ouverte = False

# --- FENETRE ---
# - Preparation -
robot.creer_fenetre(largeur_fenetre, hauteur_fenetre)
robot.couleur_fond(Couleur.NOIR)

# - Boucle -
def boucle_fenetre():
    global mettre_a_jour_affichage, session_ouverte
    robot.afficher_camera(300, 10)
    if mettre_a_jour_affichage:
        robot.afficher_fond()
        if robot.attributs.session_ouverte:
            bouton_deconnexion.afficher()
            bouton_suppression.afficher()
        else:
            bouton_creation.afficher()
        robot.afficher_texte("PROFIL", 80, 5, 30, (255, 255, 255))
        robot.afficher_texte("CREATION", 1000, 5, 30, (255, 255, 255))
        mettre_a_jour_affichage = False


# --- EVENEMENTS ---
# - Preparation -
robot.ajouter_evenement("echap", "stop")

# - Boucle -
def boucle_evenements():
    events = robot.verifier_evenements()
    if "stop" in events:
        robot.fermer_fenetre()


# --- SESSION ---
# - Preparation -
def initialisation_session():
    robot.attributs.session_ouverte = False
    robot.attributs.derniere_carte_detectee = None

# - Boucle -
def boucle_session():
    global session_ouverte, derniere_carte_detectee
    if not session_ouverte:
        # Essai de connexion
        robot.connecter()
        if robot.verifier_session():
            print(f"Hello \033[96;1m{robot.utilisateur_connecte.first_name} {robot.utilisateur_connecte.last_name}\033[0;0m !")
        else:
            # Affichage de carte détéctée non connectée
            carte_detectee = robot.detecter_carte()
            if carte_detectee:
                robot.afficher_carte_detectee(carte_detectee, 980, 200)
                derniere_carte_detectee = carte_detectee


# --- BOUTONS ---
# - Preparation -
bouton_deconnexion = robot.creer_bouton(200, 60, 25, 200, Couleur.ORANGE)
bouton_deconnexion.ajouter_texte("Deconnexion", 5, 20)
bouton_suppression = robot.creer_bouton(200, 60, 25, 300, Couleur.ROUGE)
bouton_suppression.ajouter_texte("Supprimer utilisateur", 5, 20)
bouton_creation = robot.creer_bouton(200, 60, 980, 100, (0, 150, 0))
bouton_creation.ajouter_texte("Créer  utilisateur", 20, 20)

# - Boucle -
def boucle_boutons():
    global mettre_a_jour_affichage, session_ouverte, carte_detectee
    # Mise à jour du status de la session
    if robot.verifier_session() != session_ouverte:
        session_ouverte = robot.verifier_session()
        mettre_a_jour_affichage = True
    elif session_ouverte:
        # Vérification des boutons de session
        if bouton_suppression.est_actif():
            robot.supprimer_utilisateur()
            session_ouverte = False
            mettre_a_jour_affichage = True
        if bouton_deconnexion.est_actif():
            robot.deconnecter()
            session_ouverte = False
            mettre_a_jour_affichage = True
    if bouton_creation.est_actif():
        nom_utilisateur = "Ada"
        prenom_utilisateur = "Lovelace"
        robot.creer_utilisateur(prenom_utilisateur,
                                nom_utilisateur,
                                derniere_carte_detectee)
        session_ouverte = False
        mettre_a_jour_affichage = True


if __name__ == "__main__":
    while robot.est_actif():
        boucle_evenements()
        boucle_fenetre()
        boucle_session()
        boucle_boutons()
        robot.actualiser_affichage()
