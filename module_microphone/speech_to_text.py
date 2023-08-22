from speech_recognition import Microphone, Recognizer, AudioData
import logging
from datetime import datetime
import dateparser

from typing import Callable
from .audio_processor import AudioProcessor


_debug = logging.getLogger("SpeechToText").debug
"""Custom Logger debug function. Print a message only shown when DEBUG mode is activated."""

_ERR_DEHUMANIZATION_FAILED = '"{textual_duration}" is not a valid duration.'


def get_default_recognizer() -> Recognizer:
    """
    Get a configured recognizer that should be able to recognize voice in a loud environment. `Energy_threshold` will adjust itself over time.
    """
    r = Recognizer()
    r.energy_threshold = 4000
    return r


def textual_duration_to_seconds(textual_duration: str) -> float:
    """
    Convert a textual duration such as "1min and 42 seconds" into seconds.

    Args:
        textual_duration (str): The human readable duration.

    Returns:
        float: The converted duration in seconds.
    """

    # TODO One issue here, is that absolute date like "2023/01/01" would be accepted, should be restricted to duration
    # TODO Fix debug msg "No localtime found"
    relative_base = datetime.now()
    future_date = dateparser.parse(
        textual_duration, settings={"RELATIVE_BASE": relative_base}
    )
    # in case textutal_duration is absolute, it can be in the past. # TODO I had to reverse the condition (<= with >) I have no idea why
    if (not future_date) or future_date > relative_base:
        raise ValueError(
            _ERR_DEHUMANIZATION_FAILED.format(textual_duration=textual_duration)
        )
    duration_sec = (relative_base - future_date).total_seconds()
    return duration_sec


class SpeechToText:
    """
    Conveninent class with chainable methods to record audio and perform speech to text.
    """

    is_recording: bool = False

    def __init__(self, recognizer: Recognizer = get_default_recognizer()) -> None:
        self.r = recognizer
        self.mic = Microphone()

    def for_each_phrase(self, callback: Callable[[AudioProcessor], None]):
        """
        Repeatedly record to spoken phrases and call the callback with a configured AudioProcessor instance as argument. This method is non-blocking.
        """

        def cb(r: Recognizer, recording: AudioData):
            return callback(AudioProcessor(recording, recognizer=r))

        _debug("Adjusting microphone energy threshold, this takes a few seconds...")

        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)

        _debug("Listening for phrases in background...")

        # TODO add attribute is_recording for when recording is running
        self.stop = self.r.listen_in_background(self.mic, cb)
        return self.stop

    def one_phrase(self) -> "AudioProcessor":
        """
        Wait for one sentence to be pronounce and record it.

        Returns:
            AudioProcessor: An AudioProcessor instance that can manipulate the recording.
        """
        with Microphone() as source:
            _debug("Listening to one sentence...")
            start_time = datetime.now()
            self.r.pause_threshold = 1
            recording = self.r.listen(source, timeout=2)
            _debug("Recording done...")
            return AudioProcessor(recording, start_time=start_time, recognizer=self.r)

    def during(
        self, duration: str | float, offset: float | None = None
    ) -> "AudioProcessor":
        """
        Record audio for the specified duration with an optional offset.

        Args:
            duration (str|float): Give a float to specify the duration in second, or provide a human formatted duration ex: "1min and 42 seconds".
            offfset (float): a delay in second before the recording starts.

        Returns:
            AudioProcessor: An AudioProcessor instance that can manipulate the recording.
        """
        if isinstance(duration, str):
            duration = textual_duration_to_seconds(duration)

        with Microphone() as source:
            _debug(f"Listening for {duration} secondes...")  # TODO humanize date
            start_time = datetime.now()
            recording = self.r.record(source, duration=duration, offset=offset)
            _debug("Recording done...")
            return AudioProcessor(recording, start_time=start_time, recognizer=self.r)


listen = SpeechToText()
"""A ready to use SpeechToText instance."""
