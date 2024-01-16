from pybot import Robot

robot = Robot()
robot.demarrer_webapp()

# Initialisation des couleurs
noir = (0, 0, 0)
rouge_sombre = (117, 23, 16)
jaune_sombre = (171, 128, 19)

# Preparation des variables
session_ouverte = False
mettre_a_jour_affichage = True
derniere_carte_detectee = None

robot.creer_fenetre(1200, 500)
robot.couleur_fond(noir)

# Ajout des boutons
robot.ajouter_evenement("echap", "stop")
bouton_deconnexion = robot.creer_bouton(200, 60, 25, 200, jaune_sombre)
bouton_deconnexion.ajouter_texte("Deconnexion", 5, 20)
bouton_suppression = robot.creer_bouton(200, 60, 25, 300, rouge_sombre)
bouton_suppression.ajouter_texte("Supprimer utilisateur", 5, 20)
bouton_creation = robot.creer_bouton(200, 60, 980, 100, (0, 150, 0))
bouton_creation.ajouter_texte("Créer  utilisateur", 20, 20)

def affichage_ecran():
    global mettre_a_jour_affichage, session_ouverte
    if mettre_a_jour_affichage:
        robot.afficher_fond()
        if session_ouverte:
            bouton_deconnexion.afficher()
            bouton_suppression.afficher()
        else:
            bouton_creation.afficher()
        robot.afficher_texte("PROFIL", 80, 5, 30, (255, 255, 255))
        robot.afficher_texte("CREATION", 1000, 5, 30, (255, 255, 255))
        mettre_a_jour_affichage = False

def verifier_boutons():
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

def boucle_programme():
    global mettre_a_jour_affichage, session_ouverte, derniere_carte_detectee
    while robot.est_actif():
        events = robot.verifier_evenements()
        if "stop" in events:
            robot.fermer_fenetre()
        robot.afficher_camera(300, 10)
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
        affichage_ecran()
        verifier_boutons()
        robot.actualiser_affichage()


if __name__ == "__main__":
    boucle_programme()
