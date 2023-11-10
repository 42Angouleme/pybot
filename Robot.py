import module_ecran as ecran
# import module_camera as camera


class Robot:
    def __init__(self, webapp, debug=False):
        self.ecran = ecran
        self.visage = ""
        self.visages = {}
        self.debug = debug
        self.webapp = webapp
        # self.camera = camera

    def allumer_ecran(self):
        """
        Allume l'ecran pygame
        """
        self.ecran.run(self, self.debug)

    def switch_visage(self):
        # Temporary function
        import random
        face = random.choice(list(self.visages.keys()))
        self.configurer_visage(face)

    def configurer_visage(self, visage):
        self.visage = visage

    def recevoir_visage(self):
        return self.visage
    
    def recevoir_images_visages(self):
        return self.visages

    def recevoir_webapp(self):
        return self.webapp

    def enregistrer_les_visages(self, file):
        import random
        fichier = open(file, 'r')
        lignes = fichier.readlines()
        fichier.close()
        for ligne in lignes:
            ligne = ligne.replace(' ', '')
            if len(ligne) > 3:
                valeurs = ligne.split('=')
                valeurs[1] = valeurs[1].replace('\n', '')
                self.visages[valeurs[0]] = valeurs[1]
        premier_visage = random.choice(list(self.visages.keys()))
        self.configurer_visage(premier_visage)

    def configurer(self):
        self.enregistrer_les_visages("visages.txt")

    # def allumer_camera(self):
    #     self.camera.run()

    def demarrer(self):
        self.configurer()
        self.allumer_ecran()
