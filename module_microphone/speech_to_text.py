from .openai_stt import openai_setup, openai_speech_to_text
from .microphone import Microphone


def speech_to_text(duration: int = 5) -> str | None:
    """
    High level function to record audio and get back the transcribed text.

    Args:
        duration (int): Duration of the recording in seconds. Defaults to 5 sec.
    """
    openai_setup()
    micro = Microphone()
    audio_filepath = micro.record(5)
    if audio_filepath:
        return openai_speech_to_text(audio_filepath)
    return None
