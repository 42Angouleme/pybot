import openai
import os
import logging


# When running the programme in DEBUG mode, every debug message of this module will be preffixed with this string
logger_name: str = "speech_to_text"

# A custom logger for this module
stt_logger = logging.getLogger(logger_name)

# This method prints a debug message
debug = stt_logger.debug


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
        response = openai.Audio.transcribe(
            "whisper-1", audio_file, language="fr"
        )  # TODO add prompt

    debug("OpenAI text received")
    transcribed_text = response["text"]
    return transcribed_text
