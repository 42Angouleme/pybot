from pybot import Couleur
from main_initialiser import robot

# --- FENETRE ---


def boucle_fenetre():
    # Récupérer variables dans robot
    boutons = robot.attributs.boutons
    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    session_ouverte = robot.attributs.session_ouverte
    image_emotion = robot.attributs.image_emotion

    robot.camera.afficher_camera(1200, 500)
    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()
        if session_ouverte:
            utilisateur = robot.utilisateur.obtenir_utilisateur_connecte()
            robot.fenetre.afficher_texte(
                f"Bonjour, {utilisateur.prenom} {utilisateur.nom}", 425, 5, 30, Couleur.BLANC)
            robot.fenetre.afficher_image(image_emotion, 50, 200)
            boutons.deconnexion.afficher()
            boutons.question.afficher()
            boutons.texte.afficher()
        if robot.attributs.discussion_commencee:
            boutons.texte.afficher()
        if not session_ouverte:
            robot.fenetre.afficher_image(
                "/images/emotions/amuser.png", 550, 200)
            robot.fenetre.afficher_texte(
                "Scan ta carte", 450, 100, 50, Couleur.BLANC)
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
                attributs.derniere_carte_detectee = carte_detectee


# --- BOUTONS ---
def boucle_boutons():
    # Récupérer variables dans robot
    attributs = robot.attributs
    boutons = robot.attributs.boutons
    chat_commence = attributs.discussion_commencee
    image = attributs.image_emotion

    # Mise à jour du status de la session
    if robot.utilisateur.verifier_session() != attributs.session_ouverte:
        attributs.session_ouverte = robot.utilisateur.verifier_session()
        attributs.mettre_a_jour_affichage = True
    elif attributs.session_ouverte:
        if boutons.deconnexion.est_actif():
            robot.utilisateur.deconnecter()
            attributs.session_ouverte = False
            attributs.mettre_a_jour_affichage = True
    if boutons.question.est_actif():
        chat_commence = not chat_commence
        robot.attributs.discussion_commencee = chat_commence
        boutons.texte.effacer_texte()
        if chat_commence:
            robot.IA.demarrer_discussion()
            texte_utilisateur = robot.microphone.pendant(
                "1 seconde").transcrire()
            print(texte_utilisateur)
            boutons.texte.ajouter_texte(texte_utilisateur)
            reponse = robot.IA.poser_question(texte_utilisateur)
            print(reponse)
            boutons.texte.ajouter_texte(texte_utilisateur + " " + reponse)
            emotion = robot.IA.donner_emotion(reponse)
            image = robot.fenetre.obtenir_image_emotion(emotion)
            robot.fenetre.afficher_image(image, 50, 200)
            robot.haut_parleur.dire(reponse)
            while robot.haut_parleur.lecture_en_cours:
                robot.dort(1)
        else:
            robot.IA.arreter_discussion()
        robot.attributs.mettre_a_jour_affichage = True
