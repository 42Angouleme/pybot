from main_boucle import boucle_boutons, boucle_fenetre, boucle_session, boucle_evenements
from main_initialisation import robot, initialisation_boutons, initialisation_evenements, initialisation_fenetre, initialisation_session

#
# if __name__ == "__main__":
#     initialisation_fenetre()
#     initialisation_evenements()
#     initialisation_boutons()
#     initialisation_session()
#     while robot.est_actif():
#         boucle_evenements()
#         boucle_boutons()
#         boucle_fenetre()
#         boucle_session()
#         robot.actualiser_affichage()
from pybot import Robot, Couleur

robot = Robot()

robot.demarrer_webapp()

robot.demarrer_module_fenetre()

robot.fenetre.ouvrir_fenetre(1500, 1000)
robot.demarrer_module_camera()

robot.demarrer_module_utilisateur()

boutons = robot.attributs.boutons
boutons.quitter = robot.fenetre.creer_bouton(100, 50, 10, 80, Couleur.BLANC)
boutons.quitter.ajouter_texte("quitter", 10, 10, 20, Couleur.NOIR)

boutons.deconnecter = robot.fenetre.creer_bouton(
    200, 50, 10, 10, Couleur.BLANC)
boutons.deconnecter.ajouter_texte("deconnecter", 10, 10, 20, Couleur.NOIR)

robot.attributs.mettre_a_jour_affichage = False

while robot.est_actif():

    robot.verifier_evenements()
    boutons = robot.attributs.boutons
    boutons.quitter.afficher()
    boutons.deconnecter.afficher()

    if boutons.quitter.est_actif():
        robot.desactiver()

    if robot.utilisateur.verifier_session() == False:
        robot.utilisateur.connecter()
        if robot.utilisateur.verifier_session():
            user = robot.utilisateur.obtenir_utilisateur_connecte()
            robot.fenetre.afficher_fond()
            robot.fenetre.afficher_texte(
                "Bonjour " + user.prenom + " " + user.nom, 400, 600, 20, Couleur.BLANC)

    if boutons.deconnecter.est_actif():
        if robot.utilisateur.verifier_session():
            robot.utilisateur.deconnecter()
            robot.fenetre.afficher_fond()
            robot.fenetre.afficher_texte(
                "Deconnexion reussie", 400, 600, 20, Couleur.BLANC)
        else:
            robot.fenetre.afficher_fond()
            robot.fenetre.afficher_texte(
                "Personne n'est connectée", 400, 600, 20, Couleur.BLANC)

    robot.camera.afficher_camera(300, 10)
    robot.fenetre.actualiser_affichage()
