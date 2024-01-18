from typing import Tuple, NamedTuple
from cv2.typing import MatLike


Couleur = Tuple[int, int, int]
class User(NamedTuple):
    prenom: str
    nom: str
    carte: MatLike
