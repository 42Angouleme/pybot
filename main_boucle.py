from pybot import Couleur
from main_initialiser import robot

# --- FENETRE ---


def boucle_fenetre():
    # Récupérer variables dans robot
    boutons = robot.attributs.boutons
    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    session_ouverte = robot.attributs.session_ouverte

    robot.camera.afficher_camera(300, 10)
    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()
        if session_ouverte:
            boutons.deconnexion.afficher()
            boutons.suppression.afficher()
        else:
            boutons.creation.afficher()
        boutons.question.afficher()
        if robot.attributs.discussion_commencee:
            boutons.texte.afficher()
        robot.fenetre.afficher_texte("CHAT IA", 90, 5, 30, Couleur.BLANC)
        robot.fenetre.afficher_texte("SESSION", 1015, 5, 30, Couleur.BLANC)
        robot.attributs.mettre_a_jour_affichage = False


# --- EVENEMENTS ---
def boucle_evenements():
    events = robot.verifier_evenements()
    if "stop" in events:
        robot.fermer_fenetre()


# --- SESSION ---
def boucle_session():
    # Récupérer variables dans robot
    attributs = robot.attributs
    session_ouverte = robot.attributs.session_ouverte

    if not session_ouverte:
        # Essai de connexion
        robot.utilisateur.connecter()
        if robot.utilisateur.verifier_session():
            utilisateur = robot.utilisateur.obtenir_utilisateur_connecte()
            print("Bonjour", utilisateur.prenom, utilisateur.nom, "!")
        else:
            # Affichage de carte détéctée non connectée
            carte_detectee = robot.utilisateur.detecter_carte()
            if carte_detectee:
                robot.fenetre.afficher_carte_detectee(
                    carte_detectee, 980, 200)
                attributs.derniere_carte_detectee = carte_detectee


# --- BOUTONS ---
def boucle_boutons():
    # Récupérer variables dans robot
    attributs = robot.attributs
    boutons = robot.attributs.boutons
    chat_commence = attributs.discussion_commencee

    # Mise à jour du status de la session
    if robot.utilisateur.verifier_session() != attributs.session_ouverte:
        attributs.session_ouverte = robot.utilisateur.verifier_session()
        attributs.mettre_a_jour_affichage = True
    elif attributs.session_ouverte:
        # Vérification des boutons de session
        if boutons.suppression.est_actif():
            robot.utilisateur.supprimer_utilisateur()
            attributs.session_ouverte = False
            attributs.mettre_a_jour_affichage = True
        if boutons.deconnexion.est_actif():
            robot.utilisateur.deconnecter()
            attributs.session_ouverte = False
            attributs.mettre_a_jour_affichage = True
    if boutons.creation.est_actif():
        nom_utilisateur = "Ada"
        prenom_utilisateur = "Lovelace"
        robot.utilisateur.creer_utilisateur(prenom_utilisateur,
                                            nom_utilisateur,
                                            attributs.derniere_carte_detectee)
        attributs.session_ouverte = False
        attributs.mettre_a_jour_affichage = True
    if boutons.question.est_actif():
        chat_commence = not chat_commence
        robot.attributs.discussion_commencee = chat_commence
        if chat_commence:
            boutons.question.ajouter_texte("Arreter la discussion")
            robot.IA.demarrer_discussion()
        else:
            boutons.question.ajouter_texte("Poser question")
            robot.IA.arreter_discussion()
        robot.attributs.mettre_a_jour_affichage = True
    if chat_commence and boutons.texte.est_actif():
        # texte_utilisateur = robot.fenetre.ecrire(boutons.texte)
        boutons.texte.effacer_texte()
        # print("Texte entré par utilisateur:", texte_utilisateur)
        # robot.repondre_question(texte_utilisateur)
