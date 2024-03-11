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


class HautParleur:
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
    def is_currently_reading(self) -> bool:
        """
        `True` if the robot is currently reading something. Otherwise `False`.
        """
        return HautParleur.__reading_in_progress
    
    @property
    def lecture_en_cours(self) -> bool:
        """
        `True` si le robot est accuellement en train de dire quelque chose. Sinon `False`.
        """
        return HautParleur.__reading_in_progress

    @thread
    def load_voice(self, voice: VoiceKey = default_voice_key):
        """
        Load a voice to be used for speaking.

        Args:
        -----
            voice (str): The name of the voice to load.

        Returns:
        -------
            None
        """
        # print(f"Chargement de la voix '{voix}'...")
        voice_path, loaded_event, _voice = self._voices[voice]
        # if voice is not None:
        #     print(f"La voix '{voix}' était déjà chargée...")
        self._voices[voice][2] = PiperVoice.load(voice_path)
        loaded_event.set()
        # print(f"Voix {voix} chargée.")

    @thread
    def charger_voix(self, voix: VoiceKey = default_voice_key):
        """
        Charge une voix qui pourra ensuite être utilisée pour parler.

        Paramètres:
        ----------
            voix (str): Le nom de la voix à charger.

        Retour:
        -------
            Aucun
        """
        self.load_voice(voix, thread=False)

    def use_voice(self, voice: VoiceKey) -> None:
        """
        Use a voice so it can be used by the `say` function. You must call the `load_voice` function before calling `say`.

        Args:
        -----
            voice (str): The name of the voice to load.

        Returns:
        -------
            None
        """
        self.voix_choisie = voice
    
    def utiliser_voix(self, voix: VoiceKey) -> None:
        """
        Utilise une voix, pour qu'elle soit ensuite utilisée par la fonction `dire`. Il faut penser à charger cette voix en appelant la fonction `charger_voix` avant d'appeler `dire`.

        Paramètres:
        ----------
            voix (str): Le nom de la voix à charger.

        Retour:
        -------
            Aucun
        """
        self.use_voice(voix)

    @thread
    def play_audio_file(self, path: str) -> None:
        """
        Play an audio file.

        Args:
        -----
            path (str): The full path to the audio file.

        Returns:
        --------
            None
        """
        if HautParleur.__playing_audio_file:
            warn(
                f"I am already playing an audio file, I cannot play 2 audio files at the same time."
            )
            return
        HautParleur.__playing_audio_file = True

        sd.stop()

        print(f"Début de la lecture...")
        with wave.open(path, "rb") as wav_file:
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

        HautParleur.__playing_audio_file = False

    @thread
    def lire_fichier_audio(self, chemin: str) -> None:
        """
        Lire un fichier audio.

        Paramètres:
        ----------
            chemin (str): Le chemin complet du fichier audio.

        Retour:
        -------
            Aucun
        """
        if HautParleur.__playing_audio_file:
            warn(
                f"Je suis déjà en lire un fichier audio, je ne peux pas lire 2 fichiers audio en même temps."
            )
            return

        self.play_audio_file(chemin, thread=False)

    @thread
    def record_audio_to_file(self, voice: VoiceKey, text: str, path: str) -> bool:
        """
        Transform the text into an audio file and save it at the specified path. You must have called the `load_voice` function with the same voice as a parameter before.

        Args:
        -----
            voice (str): The name of the voice to use.
            text (str): The text to synthesize.
            path (str): The path where to save the audio file.

        Returns:
        --------
            `False` if a problem occurred, otherwise `True`
        """
        timeout = 10
        loaded_event = self._voices[voice][1]
        # If voice is not loaded after a few seconds, abort
        loaded = loaded_event.wait(timeout)
        if not loaded:
            warn(
                f"The chosen voice ({voice}) was not loaded, I cannot prepare the reading."
            )
            return False

        voice = self._voices[voice][2]

        # Open file for writing
        with wave.open(path, "wb") as wav_file:
            # Generate voice from text
            voice.synthesize(text, wav_file)

        return True

    @thread
    def enregistrer_audio_dans_fichier(self, voix: VoiceKey, texte: str, chemin: str) -> bool:
        """
        Transforme le texte en fichier audio et l'enregistre au chemin spécifié.

        Il faut au préalable avoir appelé la fonction `charger_voix` avec cette même voix en paramètre.

        Paramètres:
        ----------
            voix (str): Le nom de la voix à utiliser.
            texte (str): Le texte à synthétiser.
            chemin (str): Le chemin où enregistrer le fichier audio.

        Retour:
        -------
            `False` si un problème est survenu, sinon `True`
        """
        timeout = 10
        loaded_event = self._voices[voix][1]
        # If voice is not loaded after a few seconds, abort
        loaded = loaded_event.wait(timeout)
        if not loaded:
            warn(
                f"La voix choisie ({voix}) n'a pas été charger, je ne peux pas préparer la lecture."
            )
            return False

        return self.record_audio_to_file(voix, texte, chemin, thread=False)

    @thread
    def say(self, text: str) -> bool:
        """
        Say the given text with a human voice.

        You must have prepared a voice by calling the `load_voice` and `use_voice` functions.  

        The robot must not already be speaking.

        Args:
        -----
            text (str): The text to say.

        Returns:
        -------
            `False` if a problem occurred, otherwise `True`
        """
        if HautParleur.__reading_in_progress:
            warn(
                f"I am already reading, I cannot read 2 texts at the same time."
            )
            return False

        HautParleur.__reading_in_progress = True

        if self.voix_choisie is None:
            warn(f"No voice has been chosen, I cannot prepare the reading.")
            return False

        self.enregistrer_audio_dans_fichier(
            self.voix_choisie, text, self._last_tts_filepath, thread=False
        )
        self.lire_fichier_audio(self._last_tts_filepath, thread=False)

        HautParleur.__reading_in_progress = False

        return True
    
    @thread
    def dire(self, texte: str) -> bool:
        """
        Récite le texte donné en paramètre avec une voix humaine.
        Il faut au préalable avoir préparé une voix en appelant les fonction `charger_voix` et `utiliser_voix`.
        Le robot ne doit pas déjà être en train de parler.

        Paramètres:
        ----------
            texte (str): Le texte à réciter.

        Retour:
        -------
            `False` si un problème est survenu, sinon `True`
        """
        if HautParleur.__reading_in_progress:
            warn(
                f"Je suis déjà en train de lire, je ne peux pas lire 2 textes en même temps."
            )
            return False

        if self.voix_choisie is None:
            warn(f"Aucune voix n'a été choisie, je ne peux pas préparer la lecture.")
            return False

        self.say(texte, thread=False)
