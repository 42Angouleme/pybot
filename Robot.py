import module_ecran as ecran
# import module_camera as camera


class Robot:
    def __init__(self):
        self.ecran = ecran
        self.visage = ""
        self.visages = {}
        # self.camera = camera

    def allumer_ecran(self):
        """
        Allume l'ecran pygame
        """
        self.ecran.run(self)

    def set_visage(self, visage):
        self.visage = visage

    def get_visage(self):
        return self.visage

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
        # a, b = random.choice(list(self.visages.items()))
        # print(a, b)

    def configurer(self):
        self.enregistrer_les_visages("visages.txt")

    # def allumer_camera(self):
    #     self.camera.run()

    def demarrer(self):
        self.configurer()
        self.allumer_ecran()
