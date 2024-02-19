import sounddevice as sd
import numpy as np
from typing import Literal
import wave
import os, sys

from piper import PiperVoice

import threading
from functools import wraps


def warn(msg: str):
    print(f"\033[33mAttention: {msg}\033[00m", file=sys.stderr)


def thread(func):
    @wraps(func)
    def wrapper(*args, thread=True, **kwargs):
        if thread:
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()
        else:
            func(*args, **kwargs)

    return wrapper


VoiceKey = Literal["homme", "femme", "homme_quebec"]
default_voice_key = "femme"

current_folder = os.path.dirname(os.path.abspath(__file__))
voice_directory = os.path.join(current_folder, "voix")
audio_directory = os.path.join(current_folder, "fichiers_audio")


class Lecteur:
    _voices = {
        "homme": [
            os.path.join(voice_directory, "./fr_FR-tom2.onnx"),
            threading.Event(),
            None,
        ],
        "homme_quebec": [
            os.path.join(voice_directory, "./fr_FR-gilles-low.onnx"),
            threading.Event(),
            None,
        ],
        "femme": [
            os.path.join(voice_directory, "./fr_FR-siwis-low.onnx"),
            threading.Event(),
            None,
        ],
    }
    _last_tts_filepath: str = os.path.join(audio_directory, "./derniere_lecture.wav")
    _voice: PiperVoice | None = None
    voix_choisie: VoiceKey | None = None
    __reading_in_progress: bool = False
    __playing_audio_file: bool = False

    def __init__(
        self, charger_voix: list[VoiceKey] = [], utiliser_voix: VoiceKey | None = None
    ):
        [self.charger_voix(voice) for voice in charger_voix]
        if utiliser_voix is not None:
            self.utiliser_voix(utiliser_voix)

    @property
    def lecture_en_cours(self) -> bool:
        return Lecteur.__reading_in_progress

    @thread
    def charger_voix(self, voix: VoiceKey = default_voice_key):
        print(f"Chargement de la voix '{voix}'...")
        voice_path, loaded_event, voice = self._voices[voix]
        if voice is not None:
            print(f"La voix '{voix}' était déjà chargée...")
        self._voices[voix][2] = PiperVoice.load(voice_path)
        loaded_event.set()
        if self.voix_choisie is None:
            self.utiliser_voix(voix)
        print(f"Voix {voix} chargée.")

    def utiliser_voix(self, voix: VoiceKey):
        print(f"Choix de la voix {voix}...")
        self.voix_choisie = voix

    @thread
    def lire_fichier_audio(self, chemin: str):
        if Lecteur.__playing_audio_file:
            warn(
                f"Je suis déjà en lire un fichier audio, je ne peux pas lire 2 fichiers audio en même temps."
            )
            return
        Lecteur.__playing_audio_file = True

        sd.stop()

        print(f"Début de la lecture...")
        with wave.open(chemin, "rb") as wav_file:
            # Get the WAV file parameters
            params = wav_file.getparams()
            # Read the audio data from the WAV file
            audio_data = wav_file.readframes(params.nframes)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            # Play the audio using sounddevice
            sd.play(audio_array, params.framerate)
            # Wait for playback to finish
            sd.wait()
        print(f"Fin de lecture...")

        Lecteur.__playing_audio_file = False

    @thread
    def parler_dans_fichier(self, voix: VoiceKey, text: str, chemin: str):
        timeout = 10
        loaded_event = self._voices[voix][1]
        # If voice is not loaded after a few seconds, abort
        loaded = loaded_event.wait(timeout)
        if not loaded:
            warn(
                f"La voix choisie ({voix}) n'a pas été charger, je ne peux pas préparer la lecture."
            )
            return

        voice = self._voices[voix][2]

        # Open file for writing
        with wave.open(chemin, "wb") as wav_file:
            # Generate voice from text
            voice.synthesize(text, wav_file)

    @thread
    def dire(self, text: str):
        if Lecteur.__reading_in_progress:
            warn(
                f"Je suis déjà en train de lire, je ne peux pas lire 2 textes en même temps."
            )
            return

        Lecteur.__reading_in_progress = True

        print(f"Synthétisation de la voix...")

        if self.voix_choisie is None:
            warn(f"Aucune voix n'a été choisie, je ne peux pas préparer la lecture.")
            return

        self.parler_dans_fichier(
            self.voix_choisie, text, self._last_tts_filepath, thread=False
        )
        self.lire_fichier_audio(self._last_tts_filepath, thread=False)

        Lecteur.__reading_in_progress = False
