from module_microphone.traitement_audio import TraitementAudio
from os import path
from speech_recognition import Recognizer, AudioFile
import re


def test_audiofile_to_text():
    EXPECT_REG = r"bonjour.*bienvenue.*42"
    AUDIO_FILEPATH = "bonjour42.wav"
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), AUDIO_FILEPATH)

    with AudioFile(AUDIO_FILE) as source:  # use the audio file as the audio source
        recording = Recognizer().record(source)  # read the entire audio file

    ANSWER = TraitementAudio(recording).transcrire()
    assert re.search(EXPECT_REG, ANSWER, flags=re.I)
