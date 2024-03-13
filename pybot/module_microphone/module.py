from .traitement_audio import TraitementAudio
from .Microphone import Microphone
import logging

# Uncomment for debug message
# logging.basicConfig(level=logging.DEBUG)


def print_speech(audio: TraitementAudio):
    print("Je réfléchis...")
    print("Tu as dis: " + audio.transcrire())


def scrib():
    ecoute.pour_chaque_phrase(print_speech)
    print("Le microphone écoute en arrière plan, il écrira ce que tu dis.\n")
    input("Appuies sur une touche pour arrêter.")
    ecoute.stop()
    print("Arrêt en cours...")


def text_to_speech_5_sec():
    print("J'écoute pendant 5 secondes...")
    print("Tu as dis: " + ecoute.pendant("5 secondes").transcrire())


def save_one_phrase():
    """Record one spoken sentence and save it at default path."""
    chemin = (
        ecoute.une_phrase()
        .enregistrer_sous("/tmp/my_sentence_%Y-%m-%d_%Hh%Mm%Ss.wav")
        .chemin
    )

    print("Fichier sauvegardé au chemin " + chemin)


ecoute = Microphone()


def run():
    # Comment / Uncomment functions to try them
    # text_to_speech_5_sec()
    scrib()
    # save_one_phrase()
