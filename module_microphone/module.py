import os
import openai


def openai_setup():
    """
    Setup OpenAI authentification, expect environment variables:
      - OPENAI_ORG_ID to contain your OpenAI organisation ID
      - OPENAI_API_KEY to contain your API Key.
    """
    openai.organization = os.getenv("OPENAI_ORG_ID")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.Model.list()


def openai_speech_to_text(audio_file_path: str) -> str:
    """
    Transcribe the audio file at path `audio_file_path` into text using OpenAI
    """
    with open(audio_file_path, "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)
    transcribed_text = response["text"]
    return transcribed_text


def run():
    print("Hello Module Microphone")
    openai_setup()
    txt = openai_speech_to_text("./module_microphone/bonjour42.mp3")
    print(txt)
