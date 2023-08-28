
import module_ecran as ecran
import module_camera as camera


class Robot:
    def __init__(self):
        self.ecran = ecran
        self.camera = camera

    def allumer_ecran(self):
        self.ecran.run()

    def configurer(self):
        self.ecran.option()

    def allumer_camera(self):
        self.camera.run()
