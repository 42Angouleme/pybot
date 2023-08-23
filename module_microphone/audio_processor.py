from .filepath_schema import FilepathSchema

from speech_recognition import Recognizer, AudioData
from datetime import datetime

import logging


_debug = logging.getLogger("AudioProcessor").debug
"""Custom Logger debug function. Print a message only shown when DEBUG mode is activated."""

_TXT_SAVED_AS = "File saved at {filepath}"


class AudioProcessor(FilepathSchema):
    """
    Performs action on an audio file such as saving to file, speech to text.

    Attributes:
        recording (AudioData): Input audio data.
        filepath (str): The default path where to save the file.
        start_time (datetime|None): The time when the recording started.
        recognizer (Recognizer): An instance of the speech recognizer class.
    """

    def __init__(
        self,
        recording: AudioData,
        filepath: str = "/tmp/recording_%Y-%m-%d_%Hh%Mm%Ss.wav",
        start_time: datetime | None = None,
        recognizer: Recognizer = Recognizer(),
    ) -> None:
        super().__init__(
            allowed_extensions=[".wav"], filepath=filepath, timestamp=start_time
        )
        self.recording = recording
        self.r = recognizer

    def as_text(self) -> str:
        """
        Transcribe `recording` to text. This method is blocking.

        Returns:
            str: The transcribed text.
        """
        txt = self.r.recognize_whisper_api(self.recording)
        return txt

    def save(self, filepath: str | None = None) -> "AudioProcessor":
        """
        Save the audio data to file. If `filepath` is not provided, uses the `filepath` attribute.
        Format strings such as `%H`, `%M` or `%S` inside `filepath` are evaluated using `strftime`,
        given the timestamp of when the recording started.

        Args:
            filepath (str|None): The path the file get saved at.

        Returns:
            AudioProcessor: It's own instance for method chaining.
        """
        if filepath is None:
            filepath = self.filepath
        with open(self.filepath, "wb") as f:
            # TODO Check what is convert_rate about, should it be configurable ?
            f.write(self.recording.get_wav_data(convert_rate=16000))
        _debug(_TXT_SAVED_AS.format(filepath=self.filepath))
        return self
