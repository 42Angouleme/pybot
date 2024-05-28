from pybot import Couleur
from main_initialisation import robot, largeur_fenetre, hauteur_fenetre, aligner_elements

# --- AFFICHAGE ---


def boucle_affichage_fenetre_titre():
    robot.fenetre.actualiser_affichage()

    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    boutons = robot.attributs.boutons

    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()

        texte = "Démo Pybot made by"
        x, y = aligner_texte(texte, 50)
        robot.fenetre.afficher_texte(texte, x, y, 50, Couleur.NOIR)

        texte = "42Angoulême & Collège Val de Charente"
        x, y = aligner_texte(texte, 50, "centre_haut", 0, 65)
        robot.fenetre.afficher_texte(texte, x, y, 50, Couleur.NOIR)

        boutons.quitter.afficher()
        boutons.connexion.afficher()
        boutons.creation.afficher()

        robot.fenetre.afficher_image(
            "/images/42.png", (largeur_fenetre // 2) - 230, (hauteur_fenetre - 225) // 2)
        robot.fenetre.afficher_image(
            "/images/College_Val_de_Charente.png", (largeur_fenetre // 2) + 5, (hauteur_fenetre - 80) // 2)

        robot.attributs.mettre_a_jour_affichage = False


def boucle_affichage_fenetre_creation():
    robot.fenetre.actualiser_affichage()

    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    zones_de_texte = robot.attributs.zones_de_texte
    boutons = robot.attributs.boutons

    robot.camera.afficher_camera(
        (largeur_fenetre - 640) // 2, (hauteur_fenetre - 480) // 2)
    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()

        texte = "Création Utilisateur"
        x, y = aligner_texte(texte, 50, "centre_haut", 20)
        robot.fenetre.afficher_texte(texte, x, y, 50, Couleur.BLANC)

        texte = "Nom :"
        x, y = aligner_texte(texte, 50, "droite_centre", -20, -150)
        robot.fenetre.afficher_texte(texte, x, y, 50, Couleur.BLANC)

        texte = "Prénom :"
        x, y = aligner_texte(texte, 50, "droite_centre", -20, 50)
        robot.fenetre.afficher_texte(texte, x, y, 50, Couleur.BLANC)

        if robot.attributs.manque_information:
            x, y = aligner_texte(texte, 40, "centre_haut", -270, 120)
            robot.fenetre.afficher_texte(
                "Veuillez remplir tous les champs", x, y, 40, Couleur.ROUGE_PASTEL)

        boutons.retour.afficher()

        if robot.user.verifier_session():
            boutons.deconnexion_creation.afficher()
            boutons.suppression.afficher()
            user = robot.user.obtenir_utilisateur_connecte()

            x, y = aligner_texte(user.nom, 40, "droite_centre", 270, -140)
            robot.fenetre.afficher_texte(user.nom, x, y, 40, Couleur.BLANC)

            x, y = aligner_texte(user.prenom, 40, "droite_centre", 270, 60)
            robot.fenetre.afficher_texte(user.prenom, x, y, 40, Couleur.BLANC)

        else:
            boutons.creer.afficher()
            zones_de_texte.nom.afficher()
            zones_de_texte.prenom.afficher()

        robot.attributs.mettre_a_jour_affichage = False


def boucle_affichage_fenetre_connexion():
    robot.fenetre.actualiser_affichage()

    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    boutons = robot.attributs.boutons

    robot.camera.afficher_camera(
        (largeur_fenetre - 640) // 2, (hauteur_fenetre - 480) // 2)
    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()

        texte = "Connexion Utilisateur"
        x, y = aligner_texte(texte, 50)
        robot.fenetre.afficher_texte(texte, x, y, 50, Couleur.BLANC)

        texte = "Veuillez présenter"
        taille_texte = robot.fenetre.obtenir_taille_texte(texte, 50)
        x = ((largeur_fenetre - 640) // 2 - taille_texte[0]) // 2
        y = (hauteur_fenetre - taille_texte[1]) // 2
        robot.fenetre.afficher_texte(texte, x, y, 50, Couleur.BLANC)

        texte = "votre carte"
        taille_texte = robot.fenetre.obtenir_taille_texte(texte, 50)
        x = ((largeur_fenetre - 640) // 2 - taille_texte[0]) // 2
        y = (hauteur_fenetre - taille_texte[1]) // 2 + 65
        robot.fenetre.afficher_texte(texte, x, y, 50, Couleur.BLANC)

        boutons.retour.afficher()

        robot.attributs.mettre_a_jour_affichage = False


def boucle_affichage_fenetre_session():
    robot.fenetre.actualiser_affichage()

    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    zones_de_texte = robot.attributs.zones_de_texte
    boutons = robot.attributs.boutons

    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()

        user = robot.user.obtenir_utilisateur_connecte()
        texte = "Bonjour {} {}".format(user.nom, user.prenom)
        x, y = aligner_texte(texte, 30)
        robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.BLANC)

        if robot.attributs.reponse and robot.attributs.etat_question == 4:
            robot.attributs.emotion = robot.IA.donner_emotion(
                robot.attributs.reponse)
            robot.attributs.etat_question = 0
        elif not robot.attributs.reponse and robot.attributs.etat_question == 4:
            robot.attributs.emotion = "neutre"
            robot.attributs.etat_question = 0

        image = robot.fenetre.obtenir_image_emotion(robot.attributs.emotion)
        robot.fenetre.afficher_image(image, 100, 100)

        boutons.deconnexion.afficher()
        boutons.posez_question_orale.afficher()
        boutons.posez_question_ecrite.afficher()
        boutons.supprimer_historique.afficher()

        boutons.charger_voix_homme.afficher()
        boutons.charger_voix_femme.afficher()
        boutons.charger_voix_quebecoise.afficher()

        if robot.attributs.question:
            texte = robot.attributs.question
            texte = robot.utilisateur.obtenir_utilisateur_connecte().prenom + " : " + texte
            afficher_long_texte(texte, 25, largeur_fenetre //
                                2 - 85, 120, largeur_fenetre - 30, Couleur.VIOLET)

        if robot.attributs.reponse:
            texte = robot.attributs.reponse
            afficher_long_texte(texte, 25, largeur_fenetre // 2 -
                                85, 460, largeur_fenetre - 30, Couleur.BLEU_CIEL)

        if robot.attributs.etat_question == 1:
            zones_de_texte.question.afficher()

        if robot.attributs.etat_question == 2:
            texte = "Ecoute en cours"
            x, y = aligner_texte(texte, 30, "bas_droit")
            robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.ROSE)
            robot.fenetre.afficher_image("/images/enregistre.png", 100, 100)

        if robot.attributs.etat_question == 3:
            texte = "Ecoute terminée"
            x, y = aligner_texte(texte, 30, "bas_droit")
            robot.fenetre.afficher_texte(texte, x, y, 30, Couleur.ROUGE_PASTEL)

        robot.attributs.mettre_a_jour_affichage = False
        robot.fenetre.actualiser_affichage()

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
        robot.fenetre.changer_couleur_fond(Couleur.NOIR)
        robot.dort(0.15)

    if boutons.creation.est_actif():
        robot.attributs.page = 2
        robot.attributs.mettre_a_jour_affichage = True
        robot.camera.demarrer_la_capture_d_image()
        robot.fenetre.changer_couleur_fond(Couleur.NOIR)
        robot.dort(0.15)


def boucle_boutons_fenetre_creation():
    boutons = robot.attributs.boutons

    if boutons.retour.est_actif():
        robot.attributs.page = 0
        robot.attributs.mettre_a_jour_affichage = True
        robot.attributs.derniere_carte_detectee = None
        robot.attributs.manque_information = False
        robot.camera.arreter_la_capture_d_image()
        robot.fenetre.changer_couleur_fond(Couleur.BLANC)
        if robot.user.verifier_session():
            robot.user.deconnecter()
        robot.dort(0.15)

    if robot.user.verifier_session():
        if boutons.deconnexion_creation.est_actif():
            robot.user.deconnecter()
            robot.attributs.mettre_a_jour_affichage = True
            robot.attributs.derniere_carte_detectee = None
            robot.dort(0.15)

        if boutons.suppression.est_actif():
            robot.user.supprimer()
            robot.attributs.mettre_a_jour_affichage = True
            robot.attributs.derniere_carte_detectee = None
            robot.dort(0.15)
    else:
        if boutons.creer.est_actif():
            cree_utilisateur()


def boucle_boutons_fenetre_connexion():
    boutons = robot.attributs.boutons

    if boutons.retour.est_actif():
        robot.attributs.page = 0
        robot.attributs.mettre_a_jour_affichage = True
        robot.attributs.derniere_carte_detectee = None
        robot.camera.arreter_la_capture_d_image()
        robot.fenetre.changer_couleur_fond(Couleur.BLANC)
        robot.dort(0.15)


def boucle_boutons_fenetre_session():
    boutons = robot.attributs.boutons
    zone_de_textes = robot.attributs.zones_de_texte

    if boutons.deconnexion.est_actif():
        historique = robot.IA.obtenir_historique_conversation()
        robot.utilisateur.sauvegarder_historique_conversation(historique)
        robot.IA.effacer_historique_conversation()
        robot.IA.arreter_discussion()
        robot.utilisateur.deconnecter()
        robot.attributs.page = 0
        robot.attributs.reponse = ""
        robot.attributs.question = ""
        robot.attributs.emotion = "neutre"
        robot.attributs.mettre_a_jour_affichage = True
        robot.fenetre.changer_couleur_fond(Couleur.BLANC)
        # robot.dort(0.15)

    if not robot.microphone.ecoute_en_cours:
        if boutons.posez_question_orale.est_actif():
            print("Posez une question")
            robot.attributs.mettre_a_jour_affichage = True
            robot.attributs.etat_question = 2
            boucle_affichage_fenetre_session()
            question = robot.microphone.une_phrase().transcrire()
            robot.attributs.mettre_a_jour_affichage = True
            robot.attributs.etat_question = 3
            boucle_affichage_fenetre_session()
            robot.attributs.question = question
            if question:
                réponse = robot.IA.poser_question(question)
                robot.attributs.reponse = réponse
                robot.haut_parleur.dire(réponse)
            else:
                robot.attributs.reponse = ""
            robot.attributs.etat_question = 4
            robot.attributs.mettre_a_jour_affichage = True

    if boutons.posez_question_ecrite.est_actif():
        if robot.attributs.etat_question == 0:
            robot.attributs.etat_question = 1
            robot.attributs.mettre_a_jour_affichage = True
        else:
            robot.attributs.mettre_a_jour_affichage = True
            question = zone_de_textes.question.obtenir_texte()
            robot.attributs.etat_question = 4
            if question:
                zone_de_textes.question.effacer_texte()
                robot.attributs.question = question
                réponse = robot.IA.poser_question(question)
                robot.attributs.reponse = réponse
                robot.haut_parleur.dire(réponse)
            else:
                robot.attributs.question = ""
                robot.attributs.reponse = ""
    else:
        if robot.attributs.etat_question == 5:
            robot.attributs.mettre_a_jour_affichage = True
            question = zone_de_textes.question.obtenir_texte()
            robot.attributs.etat_question = 4
            if question:
                zone_de_textes.question.effacer_texte()
                robot.attributs.question = question
                réponse = robot.IA.poser_question(question)
                robot.attributs.reponse = réponse
                robot.haut_parleur.dire(réponse)
            else:
                robot.attributs.question = ""
                robot.attributs.reponse = ""

    if boutons.supprimer_historique.est_actif():
        robot.attributs.reponse = ""
        robot.attributs.question = ""
        robot.IA.effacer_historique_conversation()
        robot.attributs.mettre_a_jour_affichage = True

    if boutons.charger_voix_homme.est_actif():
        robot.haut_parleur.utiliser_voix("homme")

    if boutons.charger_voix_femme.est_actif():
        robot.haut_parleur.utiliser_voix("femme")

    if boutons.charger_voix_quebecoise.est_actif():
        robot.haut_parleur.utiliser_voix("homme_quebec")

# --- ZONES DE TEXTE ---


def boucle_zone_de_texte_creation():
    zones_de_texte = robot.attributs.zones_de_texte

    if zones_de_texte.nom.est_actif():
        zones_de_texte.nom.ecrire(robot)

    if zones_de_texte.prenom.est_actif():
        zones_de_texte.prenom.ecrire(robot)


def boucle_zone_de_texte_fenetre_session():
    zones_de_texte = robot.attributs.zones_de_texte

    if zones_de_texte.question.est_actif():
        zones_de_texte.question.ecrire(robot)

# --- CONNEXION ---


def boucle_connexion():
    if not robot.utilisateur.verifier_session():
        robot.utilisateur.connecter()
        if robot.utilisateur.verifier_session():
            robot.camera.arreter_la_capture_d_image()
            robot.IA.demarrer_discussion()
            robot.haut_parleur.utiliser_voix("homme")
            historique = robot.utilisateur.obtenir_historique_conversation()
            robot.IA.charger_historique_conversation(historique)
            robot.attributs.mettre_a_jour_affichage = True
            robot.attributs.page = 3
        else:
            carte_detectee = robot.utilisateur.detecter_carte()
            if carte_detectee:
                robot.fenetre.afficher_carte_detectee(
                    carte_detectee, (largeur_fenetre - 200) // 2 + 640, (hauteur_fenetre - 200) // 2)
                robot.attributs.derniere_carte_detectee = carte_detectee


def boucle_test_connexion():
    if not robot.utilisateur.verifier_session():
        robot.utilisateur.connecter()
        if robot.utilisateur.verifier_session():
            robot.attributs.mettre_a_jour_affichage = True
            robot.attributs.utisateur_connecte = True
            robot.attributs.manque_information = False
        else:
            carte_detectee = robot.utilisateur.detecter_carte()
            if carte_detectee:
                robot.fenetre.afficher_carte_detectee(carte_detectee, ((
                    largeur_fenetre - 640) // 2 - 200) // 2, (hauteur_fenetre - 200) // 2)
                robot.attributs.derniere_carte_detectee = carte_detectee

# --- UTILITAIRE ---


def cree_utilisateur():
    nom = robot.attributs.zones_de_texte.nom.obtenir_texte()
    prenom = robot.attributs.zones_de_texte.prenom.obtenir_texte()
    if not nom or not prenom or robot.attributs.derniere_carte_detectee is None:
        robot.attributs.manque_information = True
        robot.attributs.mettre_a_jour_affichage = True
    else:
        robot.user.creer(prenom, nom, robot.attributs.derniere_carte_detectee)
        robot.attributs.derniere_carte_detectee = None
        robot.attributs.mettre_a_jour_affichage = True
        robot.attributs.manque_information = False
        robot.attributs.zones_de_texte.nom.effacer_texte()
        robot.attributs.zones_de_texte.prenom.effacer_texte()


def afficher_long_texte(texte, taille_police, x, y, end_x, couleur):
    mots = texte.split(" ")
    ligne = ""
    for mot in mots:
        if robot.fenetre.obtenir_taille_texte(ligne + mot, taille_police)[0] > end_x - x:
            robot.fenetre.afficher_texte(ligne, x, y, taille_police, couleur)
            y += robot.fenetre.obtenir_taille_texte(
                ligne, taille_police)[1] + 7
            ligne = mot + " "
        else:
            ligne += mot + " "
    if robot.fenetre.obtenir_taille_texte(ligne, taille_police)[0] < end_x - x:
        robot.fenetre.afficher_texte(ligne, x, y, taille_police, couleur)


def aligner_texte(texte, taille_police, alignement="centre_haut", modifier_x=0, modifier_y=0):
    taille_texte = robot.fenetre.obtenir_taille_texte(texte, taille_police)
    taille_lettre = robot.fenetre.obtenir_taille_texte(" ", taille_police)
    if alignement == "centre_haut":
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
        x = (largeur_fenetre // 2 -
             taille_texte[0]) // 2 + largeur_fenetre // 2
        y = (hauteur_fenetre - taille_texte[1] + taille_lettre[1]) // 2
    elif alignement == "bas_droit":
        x = largeur_fenetre - taille_texte[0] - 20
        y = hauteur_fenetre - taille_texte[1] - 20
    else:
        x = 0
        y = 0
    x += modifier_x
    y += modifier_y
    return x, y
