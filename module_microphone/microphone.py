import datetime
import wavio
from .filepath_timestamp import FilepathTimestamp
import sounddevice as sd
import logging
import asyncio

# When running the programme in DEBUG mode, every debug message of this module will be preffixed with this string
logger_name: str = "microphone"

# A custom logger for this module
stt_logger = logging.getLogger(logger_name)

# This method prints a debug message
debug = stt_logger.debug


class Microphone(FilepathTimestamp):
    """
    Microphone recorder.

    Attributes:
        playing (bool): True while recording is in progress.
        recording : TODO doc
        filepath (str): The path where to save the file. Extension should match an audio type. A timestamp suffix might be automatically added.
        use_ts_suffix (bool): Whether to use timestamp suffix or not.

    """

    playing = False
    sample_rate = 44100  # Samples per second (Hz)

    def __init__(
        self,
        filepath="./recording.wav",
        use_ts_suffix=True,
        allowed_extensions=[".wav"],
    ) -> None:
        super().__init__(
            filepath=filepath,
            use_ts_suffix=use_ts_suffix,
            allowed_extensions=allowed_extensions,
        )

    def stop(self) -> str | None:
        """Stop the recording and save it."""
        filepath = None
        if self.playing:
            sd.stop()
            debug("Recording stopped.")
            filepath = self._save_recording()
            self.playing = False
        else:
            debug("Recording stopped but it was not playing.")
        return filepath

    def record(self, duration, filepath=None) -> str | None:
        """
        Use the microphone to record an audio file. The recording starts immediatly and last for `duration` secondes. The file is stored at path `filepath`.

        Args:
            filepath (str): The path where to save the audio file
            duration (int): The duration is sec of the recording
        """
        if filepath is None:
            filepath = self.filepath
        self.last_timestamp = datetime.datetime.now()
        debug("Recording audio...")
        self.playing = True
        self.recording = sd.rec(
            int(self.sample_rate * duration), samplerate=self.sample_rate, channels=1
        )  # Start recording

        sd.wait()  # Wait for recording to complete
        if self.playing:
            filepath = self.stop()
        debug("Recording finished.")
        return filepath

    def start_record(self, duration, filepath=None) -> str | None:
        """
        Use the microphone to record an audio file. The recording starts immediatly and last for `duration` secondes. The file is stored at path `filepath`.

        Args:
            filepath (str): The path where to save the audio file
            duration (int): The duration is sec of the recording
        """
        if filepath is None:
            filepath = self.filepath
        self.last_timestamp = datetime.datetime.now()
        debug("Recording audio...")
        self.playing = True
        self.recording = sd.rec(
            int(self.sample_rate * duration), samplerate=self.sample_rate, channels=1
        )  # Start recording

    async def _async_record(self, *args):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.start_record, *args)

    def async_record(self, *args):
        if self.playing:
            debug("Recording already in progress, cannot start a new recording")
            return
        asyncio.create_task(self._async_record(*args))

    def _save_recording(self) -> str:
        """Save the recording. Ensure to stop the recording before calling this function."""
        wavio.write(
            self.filepath, self.recording, self.sample_rate, sampwidth=2
        )  # Save the audio file
        debug(f"Audio saved as {self.filepath}")
        return self.filepath
