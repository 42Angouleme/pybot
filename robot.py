from script import config
import module_ecran as ecran
import module_camera as camera


class Robot:
    def __init__(self):
        self.config = config
        self.ecran = ecran
        self.camera = camera

    def allumer_ecran(self):
        """
        Allume l'ecran pygame
        """
        self.ecran.run()

    def configurer(self):
        self.config.run()

    def allumer_camera(self):
        self.camera.run()
