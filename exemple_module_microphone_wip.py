from pybot.module_fenetre.Interface import Button
from pybot.module_microphone import Microphone
from pybot import Robot, Couleur

# --- GENERAL ---
robot = Robot()
robot.demarrer_webapp()
mettre_a_jour_affichage = True
largeur_fenetre = 1200
hauteur_fenetre = 500
discussion_commencer = False

robot.demarrer_module_fenetre()
robot.demarrer_module_haut_parleur()

# --- FENETRE ---
# - Preparation -
robot.fenetre.ouvrir_fenetre(largeur_fenetre, hauteur_fenetre)
robot.fenetre.change_background_color(Couleur.NOIR)
robot.fenetre.changer_titre("Bonjour Robot!")

# --- LECTEUR ---
# - Preparation -
robot.haut_parleur.charger_voix("homme")
robot.haut_parleur.utiliser_voix("homme")


# - Boucle -
def boucle_fenetre():
    global mettre_a_jour_affichage
    if mettre_a_jour_affichage:
        robot.fenetre.afficher_fond()
        bouton_microphone.afficher()
        bouton_question.afficher()
        bouton_stop.afficher()
        mettre_a_jour_affichage = False


# --- EVENEMENTS ---
# - Preparation -
robot.ajouter_evenement("echap", "stop")
robot.ajouter_evenement("C", "C")


# - Boucle -
def boucle_evenements():
    events = robot.check_events()
    if "stop" in events:
        robot.desactiver()
    if "C" in events:
        print("Vous appuyez sur C")


# --- BOUTONS ---
# - Preparation -

# Bouton pour lancer un enregistrement
bouton_microphone: Button = robot.fenetre.creer_bouton(
    300, 60, 10, 400, Couleur.ROSE)
bouton_microphone.ajouter_texte("Enregistrer une phrase", 5, 20)

# Bouton pour lire le fichier audio
bouton_question: Button = robot.fenetre.creer_bouton(
    300, 60, 10, 200, Couleur.CYAN)
bouton_question.ajouter_texte("Faire dire une phrase", 5, 20)

# Bouton pour quitter
bouton_stop: Button = robot.fenetre.creer_bouton(
    200, 60, 10, 300, Couleur.ROUGE)
bouton_stop.ajouter_texte("Quitter", 10, 10, 20)

# --- MICROPHONE ---
microphone = Microphone()


# - Boucle -
def boucle_boutons():
    if bouton_microphone.est_actif():
        microphone.pendant("5 secondes").enregistrer_sous(
            "example_microphone.wav").transcrire()
    if bouton_question.est_actif():
        robot.haut_parleur.lire_fichier_audio("example_microphone.wav")
        while robot.haut_parleur.lecture_en_cours:
            robot.dort(1)
    if bouton_stop.est_actif():
        robot.desactiver()


if __name__ == "__main__":
    while robot.est_actif():
        boucle_evenements()
        boucle_boutons()
        boucle_fenetre()
        robot.fenetre.actualiser_affichage()
