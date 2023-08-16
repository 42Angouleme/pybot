import os
import openai
import sounddevice as sd
import wavio
import tempfile
import logging

# TODO initialize this in entrypoint
logging.basicConfig(level=logging.DEBUG)

# When running the programme in DEBUG mode, every debug message of this module will be preffixed with this string
logger_name: str = "speech_to_text"

# A custom logger for this module
stt_logger = logging.getLogger(logger_name)

# This method prints a debug message
debug = stt_logger.debug


def record_audio(filepath, duration):
    """
    Use the microphone to record an audio file. The recording starts immediatly and last for `duration` secondes. The file is stored at path `filepath`.

    Args:
        filepath (str): The path where to save the audio file
        duration (int): The duration is sec of the recording
    """
    sample_rate = 44100  # Samples per second (Hz)

    debug("Recording audio...")
    recording = sd.rec(
        int(sample_rate * duration), samplerate=sample_rate, channels=1
    )  # Start recording

    sd.wait()  # Wait for recording to complete
    debug("Recording finished.")

    wavio.write(filepath, recording, sample_rate, sampwidth=2)  # Save the audio file
    debug(f"Audio saved as {filepath}")


def openai_setup():
    """
    Setup OpenAI authentification, expect environment variables:
      - OPENAI_ORG_ID to contain your OpenAI organisation ID
      - OPENAI_API_KEY to contain your API Key.
    """
    openai.organization = os.getenv("OPENAI_ORG_ID")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.Model.list()


def openai_speech_to_text(audio_filepath: str) -> str:
    """
    Transcribe the audio file at path `audio_file_path` into text using OpenAI

    Args:
        audio_filepath (str): The path of the file to transcribe.

    Returns:
        str: The transcribed text.
    """

    debug("Opening audio file")
    with open(audio_filepath, "rb") as audio_file:
        debug("Requesting OpenAI speech to text")
        response = openai.Audio.transcribe("whisper-1", audio_file, language="fr")

    debug("OpenAI text received")
    transcribed_text = response["text"]
    return transcribed_text


def run():
    debug("Hello Module Microphone")

    openai_setup()

    extension = ".wav"
    audio_filepath = tempfile.NamedTemporaryFile(suffix=extension).name
    record_audio(filepath=audio_filepath, duration=10)
    transcribed_txt = openai_speech_to_text(audio_filepath)
    debug(f"Transcribed text {transcribed_txt}")
