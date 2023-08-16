import os
import openai
import sounddevice as sd
import wavio


def record_audio(filename="output.wav", duration=5):
    """Record audio at `filename` for the specified `duration`"""
    sample_rate = 44100  # Samples per second (Hz)

    print("Recording audio...")
    recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1)
    input()  # Wait for the user to press Enter to stop recording
    sd.stop()  # Stop recording
    print("Recording finished.")

    wavio.write(filename, recording, sample_rate, sampwidth=2)
    print(f"Audio saved as {filename}")


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

    print("Opening audio file")
    with open(audio_file_path, "rb") as audio_file:
        print("Requesting OpenAI speech to text")
        response = openai.Audio.transcribe("whisper-1", audio_file, language="fr")

    print("OpenAI text received")
    transcribed_text = response["text"]
    return transcribed_text


def run():
    print("Hello Module Microphone")

    openai_setup()

    audio_filepath = "/tmp/output.wav"
    record_audio(filename=audio_filepath, duration=10)
    txt = openai_speech_to_text(audio_filepath)
    print(f"Transcribed text {txt}")
