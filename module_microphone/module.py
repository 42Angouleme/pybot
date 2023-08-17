from .speech_to_text import speech_to_text
from .microphone import Microphone
from .openai_stt import openai_setup, openai_speech_to_text

import logging
import asyncio

logging.basicConfig(level=logging.DEBUG)


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


async def async_recording():
    openai_setup()
    micro = Microphone()
    # Run the recording for 4 sec maximum, without blocking
    micro.async_record(4)
    # Wait 2 sec
    await asyncio.sleep(2)
    # Stop the recording
    audio_filepath = micro.stop()
    #
    print(audio_filepath)


def run():
    print("Hello Module Microphone")
    using_high_level_function()
    using_low_level_function()
    asyncio.run(async_recording())
