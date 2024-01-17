import speech_recognition
from .filepath_schema import FilepathSchema

from speech_recognition import Recognizer, AudioData
from datetime import datetime
import openai

import logging


_debug = logging.getLogger("TraitementAudio").debug
_error = logging.getLogger("TraitementAudio").error
"""Custom Logger debug function. Print a message only shown when DEBUG mode is activated."""

_TXT_SAVED_AS = 'Fichier enregistré sous "{filepath}"'


class TraitementAudio(FilepathSchema):
    """
    Effectue des actions sur un fichier audio tel que sauvegarder le fichier ou transcrire la parole en texte.

    Attributes:
        recording (AudioData): Donnée audio d'entrée.
        filepath (str): Le chemin par défaut où sauvegarder le fichier.
        start_time (datetime|None): Le temps du début d'enregistrement.
        recognizer (Recognizer): Une instance du speech_recognition Recognizer.
    """

    def __init__(
        self,
        recording: AudioData | None = None,
        chemin: str = "/tmp/recording_%Y-%m-%d_%Hh%Mm%Ss.wav",
        start_time: datetime | None = None,
        recognizer: Recognizer = Recognizer(),
    ) -> None:
        super().__init__(
            allowed_extensions=[".wav"], chemin=chemin, timestamp=start_time
        )
        self.recording = recording
        self.r = recognizer

    def transcrire(self) -> str:
        """
        Retranscrit l'enregstrement audio en texte. Cette méthode est bloquante.

        Returns:
            str: Le texte reconnu dans l'enregistrement.
        """
        if self.recording is None:
            return ""
        try:
            return self.r.recognize_whisper_api(self.recording)
        except speech_recognition.exceptions.SetupError as e:
            _error(
                f"Une erreur est survenue, le texte n'a pas pu êre transcrit. Indication: {e}"
            )
            return ""
        except openai.error.AuthenticationError as e:
            _error(
                f"Une erreur est survenue, le texte n'a pas pu êre transcrit. Indication: {e}"
            )
            return ""

    def enregistrer_sous(self, filepath: str | None = None) -> "TraitementAudio":
        """
        Enregstre le fichier audio dans un fichier au chemin spécifié. Un chemin par défaut existe si celui-ci n'est pas précisé.
        Il est possible d'insérer l'heure est la date dans le chemin du fichier "./mon_fichier_%Y-%m-%d_%Hh%Mm.wav" sera par exemple remplacé par "./mon_fichier_2024-01-01_10h30m.wav" avec l'heure et la date du début de l'enregistrement.
        Voir [https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior] pour la liste des substitutions possibles.

        Args:
            filepath (str|None): Le chemin où sauvegarder le fichier.

        Returns:
            AudioProcessor: Retourne sa propre instance pour le chaînage de méthodes.
        """
        if self.recording is None:
            return self
        if filepath is not None:
            self.chemin = filepath
        with open(self.chemin, "wb") as f:
            # TODO Check what is convert_rate about, should it be configurable ?
            f.write(self.recording.get_wav_data(convert_rate=16000))
        _debug(_TXT_SAVED_AS.format(filepath=self.chemin))
        return self
