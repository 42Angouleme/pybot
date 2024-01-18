# Lancer cette démo depuis la racine du projet en faisant
# python3 -m pybot.module_microphone.examples.ecoute_5_secondes_enregistre_transcrit

from pybot.module_microphone import ecoute

import logging

logging.basicConfig(level=logging.DEBUG)

texte = (
    ecoute.pendant("5 secondes").enregistrer_sous("./fichier_audio.wav").transcrire()
)
print(texte)
