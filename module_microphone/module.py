from .speech_to_text import speech_to_text
from .microphone import Microphone
from .openai_stt import openai_setup, openai_speech_to_text


def using_high_level_function():
    print("recording for 10 secs")
    txt = speech_to_text(duration=10)
    print("Transcribed text:")
    print(txt)


def using_low_level_function():
    openai_setup()
    micro = Microphone()
    print("recording for 5 secs")
    audio_filepath = micro.record(5)
    if audio_filepath:
        transcribed_txt = openai_speech_to_text(audio_filepath)
        print(f"Transcribed text {transcribed_txt}")


def run():
    print("Hello Module Microphone")
    using_high_level_function()
    using_low_level_function()
