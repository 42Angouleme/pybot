# Lancer cette démo depuis la racine du projet en faisant
# python3 -m pybot.module_microphone.examples.ecoute_une_phrase_transcrit

from pybot.module_microphone import ecoute

import logging

logging.basicConfig(level=logging.DEBUG)

texte = ecoute.une_phrase().transcrire()
print(texte)
