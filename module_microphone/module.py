from .speech_to_text import listen, AudioProcessor
import logging

# Uncomment for debug message
# logging.basicConfig(level=logging.DEBUG)


def speech_to_text(audio: AudioProcessor):
    print("Je réfléchis...")
    print("Tu as dis: " + audio.as_text())


def scrib():
    listen.in_background(speech_to_text)
    print("Le microphone écoute en arrière plan, il écrira ce que tu dis.\n")
    input("Appuies sur une touche pour arrêter.")
    listen.stop()
    print("Arrêt en cours...")


def text_to_speech_5_sec():
    print("J'écoute pendant 5 secondes...")
    print("Tu as dis: " + listen.during("5 secondes").as_text())


def record_1_sentence():
    """Record one spoken sentence and save it at default path."""
    filepath = (
        listen.one_sentence().save("/tmp/my_sentence_%Y-%m-%d_%Hh%Mm%Ss.wav").filepath
    )

    print("Fichier sauvegardé au chemin " + filepath)


def run():
    # Comment / Uncomment functions to try them
    text_to_speech_5_sec()
    # scrib()
    # record_1_sentence()
