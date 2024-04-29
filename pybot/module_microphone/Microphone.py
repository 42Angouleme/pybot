import logging
from datetime import datetime
from typing import Callable
from speech_recognition import Microphone as SrMicrophone, Recognizer, AudioData
from .traitement_audio import TraitementAudio
from .utils import textual_duration_to_seconds
from ..alsa_err_remover import noalsaerr

_debug = logging.getLogger("Microphone").debug
_error = logging.getLogger("Microphone").error

"""Custom Logger debug function. Print a message only shown when DEBUG mode is activated."""


def _get_default_recognizer() -> Recognizer:
    """
    Get a configured recognizer that should be able to recognize voice in a loud environment. `Energy_threshold` will adjust itself over time.
    """
    r = Recognizer()
    r.energy_threshold = 4000
    return r


class Microphone:
    """
    Permet d'enregistrer l'audio de différentes manières. Les méthodes sont châinables pour ensuite pour effectuer des traitements sur le fichier audio comme l'enregistrer dans un fichier, ou le transcrire.
    """

    is_recording: bool = False
    __listening_in_progress : bool = False

    def __init__(self, recognizer: Recognizer = _get_default_recognizer()) -> None:
        with noalsaerr():
            self.r = recognizer
            self.mic = SrMicrophone()
    
    @property
    def is_listening(self) -> bool:
        """
        `True` si le robot est accuellement en train de dire quelque chose. Sinon `False`.
        """
        return Microphone.__listening_in_progress

    @property
    def ecoute_en_cours(self) -> bool:
        """
        `True` si le robot est accuellement en train de dire quelque chose. Sinon `False`.
        """
        return Microphone.__listening_in_progress

    def for_each_sentence(self, callback: Callable[[TraitementAudio], None]):
        """
        Listen to the microphone and call the given function for each sentence spoken. This method is non-blocking.
        At the beginning of the recording, you have to wait a few seconds without speaking, the microphone adjusts to the ambient noise to be able to detect silences afterwards.
        """

        def cb(r: Recognizer, recording: AudioData):
            return callback(TraitementAudio(recording, recognizer=r))

        _debug(
            "Je m'ajuste au bruit ambiant pour pouvoir détecter les silences, celà prend quelques secondes..."
        )
        with noalsaerr():
            with self.mic as source:
                self.r.adjust_for_ambient_noise(source)

            _debug("J'écoute la parole en arrière plan...")

            # TODO add attribute is_recording for when recording is running
            Microphone.__listening_in_progress = True
            self.stop = self.r.listen_in_background(self.mic, cb)
            Microphone.__listening_in_progress = False
            return self.stop

    def pour_chaque_phrase(self, callback: Callable[[TraitementAudio], None]):
        """
        Enregistre chaque phrase parlée. Dès qu'une phrase est terminée, la fonction donnée en paramètre est appellée. Cette méthode n'est pas bloquante.
        Au début de l'enregistrement, il faut attendre quelque secondes sans parler, le microphone s'ajuste au bruit ambiant pour être ensuite capable de détecter les silences.
        """

        return self.for_each_sentence(callback)

    def one_sentence(self) -> "TraitementAudio":
        """
        Listen to the microphone and record only one sentence. The recording starts when this method is called, and stops when the person stops speaking for more than a second.

        Returns:
            TraitementAudio: The recording ready to be manipulated.
        """
        with noalsaerr():
            Microphone.__listening_in_progress = True
            with self.mic as source:
                _debug("Écoute d'une phrase")
                start_time = datetime.now()
                self.r.pause_threshold = 1
                recording = self.r.listen(source)
                _debug("Écoute terminée...")
                Microphone.__listening_in_progress = False
                return TraitementAudio(recording, start_time=start_time, recognizer=self.r)

    def une_phrase(self) -> "TraitementAudio":
        """
        Enregistre uniquement une phrase. L'enregistrement commence quand cette méthode est appellée, et s'arrête quand la personne arrête de parler pendant plus d'une seconde.

        Retour:
            TraitementAudio: L'enregistrement prêt à être manipulé.
        """
        return self.one_sentence()

    def during(
        self, duree: str | float, delai: str | float | None = None
    ) -> "TraitementAudio":
        """
        Record audio for the specified duration, with an optional delay. The delay allows to wait a certain time before the recording starts.
        The duration and the delay can be given either in seconds (example: 5), or in full letters (example: "1 minute and 30 seconds").

        Parameters:
            duree (str|float): Either a number representing the duration of the recording in seconds, or a duration in full letters like "1 minute and 30 seconds".
            delai (float): A delay before the recording starts.

        Returns:
            TraitementAudio: The recording ready to be manipulated.
        """
        with noalsaerr():
            if isinstance(duree, str):
                try:
                    duree = textual_duration_to_seconds(duree)
                except ValueError as e:
                    _error(
                        f'L\'enregistrement n\'a pas pu commencer. Erreur dans la fonction "pendant", argument "duree" invalide: {e}',
                    )  # TODO humanize date
                    return TraitementAudio()

            if isinstance(delai, str):
                try:
                    delai = textual_duration_to_seconds(delai)
                except ValueError as e:
                    _error(
                        f'L\'enregistrement n\'a pas pu commencer. Erreur dans la fonction "pendant", argument "delai" invalide: {e}',
                    )  # TODO humanize date
                    return TraitementAudio()

            with SrMicrophone() as source:
                # TODO humanize date
                Microphone.__listening_in_progress = True
                _debug(f"J'écoute pendant {duree} secondes...")
                start_time = datetime.now()
                recording = self.r.listen(source, timeout=duree)
                _debug("Écoute terminée...")
                Microphone.__listening_in_progress = False
                return TraitementAudio(recording, start_time=start_time, recognizer=self.r)

    def pendant(
        self, duree: str | float, delai: str | float | None = None
    ) -> "TraitementAudio":
        """
        Enregistre l'audio pendant la durée specifiée, avec un délai optionel. Le délai, permet d'attendre un certain temps avant que l'enregistrement ne commence.
        La durée et le délai peuvent être données soit en secondes (exemple: 5), soit en toutes lettres (exemple: "1 minute et 30 secondes").

        Paramètres:
            duree (str|float): Soit un nombre qui représente la durée de l'enregistrement en secondes, soit une durée en toutes lettres comme "1 minute et 30 secondes".
            decalage (float): Un délai avant que l'enregistrement ne commence.

        Retour:
            TraitementAudio: L'enregistrement prêt à être manipulé.
        """
        return self.during(duree, delai)
