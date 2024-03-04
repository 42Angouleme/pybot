import time
from pybot.module_audio import Lecteur


lecteur = Lecteur()

lecteur.charger_voix("femme")
lecteur.charger_voix("homme")

lecteur.utiliser_voix("femme")

phrase = """Maître Corbeau, sur un arbre perché, tenait en son bec un fromage."""

lecteur.dire(phrase)

while lecteur.lecture_en_cours:
    time.sleep(1)

lecteur.utiliser_voix("homme")
lecteur.dire(phrase)
