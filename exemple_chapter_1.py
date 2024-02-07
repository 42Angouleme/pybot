# from pybot import Robot

# robot = Robot()

# robot.demarrer_module_fenetre()

# robot.fenetre.changer_titre("bonjour,pybot!")
# robot.fenetre.ouvrir_fenetre()
# robot.fenetre.changer_titre("bonjour,pybot!")
# robot.fenetre.actualiser_affichage()
# robot.dort(1)
# robot.fenetre.changer_titre("plein écran dans une seconde")
# robot.fenetre.actualiser_affichage()
# robot.dort(1)
# robot.fenetre.plein_ecran(True)
# robot.fenetre.actualiser_affichage()
# robot.dort(1)
# robot.fenetre.changer_titre("fin du programme dans une seconde")
# robot.fenetre.plein_ecran(False)
# robot.fenetre.actualiser_affichage()
# robot.dort(1)

from pybot import Robot, Couleur

robot = Robot()
robot.demarrer_module_fenetre()

robot.fenetre.ouvrir_fenetre(1200, 900)
robot.fenetre.changer_titre("Nouveau titre")
robot.fenetre.changer_couleur_fond(Couleur.BLANC)
robot.fenetre.afficher_fond()
robot.ajouter_evenement("echap", "sortir")

robot.fenetre.dessiner_rectangle(100, 50, 100, 100, Couleur.BLEU_CIEL)
robot.fenetre.afficher_texte("Bonjour", 100, 100, 20, Couleur.NOIR)
#robot.fenetre.afficher_image("images/photo.png", 100, 100) # à remplacer par le chemin de votre image

while robot.est_actif() :
    evenement = robot.verifier_evenements()
    if "sortir" in evenement:
        robot.desactiver()
        break # Sortie de la boucle
    robot.fenetre.actualiser_affichage()