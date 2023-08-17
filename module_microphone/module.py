from .microphone import Microphone
from .speech_to_text import openai_setup, openai_speech_to_text

# TODO initialize this in entrypoint
# import logging
# logging.basicConfig(level=logging.DEBUG)


def run():
    print("Hello Module Microphone")

    openai_setup()

    micro = Microphone()
    audio_filepath = micro.record(5)
    if audio_filepath:
        transcribed_txt = openai_speech_to_text(audio_filepath)
        print(f"Transcribed text {transcribed_txt}")
