from pybot import Robot, Couleur


# --- GENERAL ---
robot = Robot()
robot.demarrer_webapp()
robot.attributs.mettre_a_jour_affichage = True
largeur_fenetre = 1200
hauteur_fenetre = 500


# --- FENETRE ---
robot.creer_fenetre(largeur_fenetre, hauteur_fenetre)
robot.couleur_fond(Couleur.NOIR)

# --- EVENEMENTS ---
robot.ajouter_evenement("echap", "stop")

# --- SESSION ---
robot.attributs.session_ouverte = False
robot.attributs.derniere_carte_detectee = None


# --- BOUTONS ---
boutons = robot.attributs.boutons
boutons.deconnexion = robot.creer_bouton(200, 60, 25, 200, Couleur.ORANGE)
boutons.deconnexion.ajouter_texte("Deconnexion", 5, 20)
boutons.suppression = robot.creer_bouton(200, 60, 25, 300, Couleur.ROUGE)
boutons.suppression.ajouter_texte("Supprimer utilisateur", 5, 20)
boutons.creation = robot.creer_bouton(200, 60, 980, 100, (0, 150, 0))
boutons.creation.ajouter_texte("Créer  utilisateur", 20, 20)
