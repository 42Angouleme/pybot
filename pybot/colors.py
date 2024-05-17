from enum import Enum

class Couleur(Enum):
    ROUGE = (255, 0, 0)
    ROUGE_PASTEL = (239, 75, 75)
    VERT = (0, 255, 0)
    BLEU = (0, 0, 255)
    JAUNE = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    BLANC = (255, 255, 255)
    GRIS = (205, 205, 205)
    NOIR = (0, 0, 0)
    ORANGE = (230, 161, 87)
    ROSE = (255, 192, 203)
    VIOLET = (166, 133, 226)
    BLEU_CIEL = (135, 206, 235)
    VERT_SAPIN = (35, 139, 34)
    VERT_FONCE = (155, 182, 124)

    def __get__(self, instance, owner):
        return self.value

    @staticmethod
    def get_item(index):
        for i, col in enumerate(list(Couleur)):
            if i == index:
                return col
        return Couleur.NOIR
