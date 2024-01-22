from pybot import Robot, Couleur


# --- PREPARATION ---
# - Global -
robot = Robot()
robot.demarrer_webapp()
robot.attributs.mettre_a_jour_affichage = True
mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
largeur_fenetre = 1200
hauteur_fenetre = 500


# - Fenetre -
robot.creer_fenetre(largeur_fenetre, hauteur_fenetre)
robot.couleur_fond(Couleur.NOIR)

# - Evenements -
robot.ajouter_evenement("echap", "stop")

# - Session -
robot.attributs.session_ouverte = False
robot.attributs.derniere_carte_detectee = None

# - Boutons -
boutons = robot.attributs.boutons
boutons.deconnexion = robot.creer_bouton(200, 60, 25, 200, Couleur.ORANGE)
boutons.deconnexion.ajouter_texte("Deconnexion", 5, 20)
boutons.suppression = robot.creer_bouton(200, 60, 25, 300, Couleur.ROUGE)
boutons.suppression.ajouter_texte("Supprimer utilisateur", 5, 20)
boutons.creation = robot.creer_bouton(200, 60, 980, 100, (0, 150, 0))
boutons.creation.ajouter_texte("Créer  utilisateur", 20, 20)


# ---   BOUCLE   ---
# - Fenetre -
def boucle_fenetre():
    # Récupérer variables dans robot
    boutons = robot.attributs.boutons
    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    session_ouverte = robot.attributs.session_ouverte

    robot.afficher_camera(300, 10)
    if mettre_a_jour_affichage:
        robot.afficher_fond()
        if session_ouverte:
            boutons.deconnexion.afficher()
            boutons.suppression.afficher()
        else:
            boutons.creation.afficher()
        robot.afficher_texte("PROFIL", 80, 5, 30, (255, 255, 255))
        robot.afficher_texte("CREATION", 1000, 5, 30, (255, 255, 255))
        robot.attributs.mettre_a_jour_affichage = False

# - Evenements -
def boucle_evenements():
    events = robot.verifier_evenements()
    if "stop" in events:
        robot.fermer_fenetre()

# - Session -
def boucle_session():
    # Récupérer variables dans robot
    attributs = robot.attributs
    session_ouverte = robot.attributs.session_ouverte

    if not session_ouverte:
        # Essai de connexion
        robot.connecter()
        if robot.verifier_session():
            utilisateur = robot.recuperer_utilisateur_connecte()
            print("Bonjour", utilisateur.prenom, utilisateur.nom, "!")
        else:
            # Affichage de carte détéctée non connectée
            carte_detectee = robot.detecter_carte()
            if carte_detectee:
                robot.afficher_carte_detectee(carte_detectee, 980, 200)
                attributs.derniere_carte_detectee = carte_detectee

# - Boutons -
def boucle_boutons():
    # Récupérer variables dans robot
    attributs = robot.attributs
    boutons = robot.attributs.boutons

    # Mise à jour du status de la session
    if robot.verifier_session() != attributs.session_ouverte:
        attributs.session_ouverte = robot.verifier_session()
        attributs.mettre_a_jour_affichage = True
    elif attributs.session_ouverte:
        # Vérification des boutons de session
        if boutons.suppression.est_actif():
            robot.supprimer_utilisateur()
            attributs.session_ouverte = False
            attributs.mettre_a_jour_affichage = True
        if boutons.deconnexion.est_actif():
            robot.deconnecter()
            attributs.session_ouverte = False
            attributs.mettre_a_jour_affichage = True
    if boutons.creation.est_actif():
        nom_utilisateur = "Ada"
        prenom_utilisateur = "Lovelace"
        robot.creer_utilisateur(prenom_utilisateur,
                                nom_utilisateur,
                                attributs.derniere_carte_detectee)
        attributs.session_ouverte = False
        attributs.mettre_a_jour_affichage = True


if __name__ == "__main__":
    while robot.est_actif():
        boucle_evenements()
        boucle_fenetre()
        boucle_session()
        boucle_boutons()
        robot.actualiser_affichage()
