import time

# Lancer cette démo depuis la racine du projet en faisant
# python3 -m pybot.module_microphone.examples.transcrit_chaque_phrase

import logging

from pybot.module_microphone import TraitementAudio
from pybot.module_microphone import ecoute

logging.basicConfig(level=logging.DEBUG)


def retranscrire(audio: TraitementAudio):
    print("Tu as dis: ", audio.transcrire())


# fonction non bloquante
ecoute.pour_chaque_phrase(retranscrire)

# garde le programme en vie 30 secondes
time.sleep(60)
