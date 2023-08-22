#! /bin/python3
import module_microphone as microphone
import module_audio as audio
import module_camera as camera
import module_ia as ia
import module_ecran as ecran
from module_microphone.speech_to_text import (
    speech_to_text,
    openai_setup,
    openai_speech_to_text,
)
from module_microphone import Microphone
import asyncio


# def main():
#    # microphone.run()
#    txt = speech_to_text(10)
#    if txt:
#        audio.run(txt)
# camera.run()
# ia.run()
# ecran.run()


async def user_flow():
    openai_setup()
    # txt = speech_to_text()

    while True:
        input("Press anything to continue")
        micro = Microphone()
        # Run the recording for 4 sec maximum, without blocking
        micro.start_record(10)
        input("Press enter to stop recording...")
        filepath = micro.stop()
        if not filepath:
            return
        question = openai_speech_to_text(filepath)
        if not question:
            return
        answer = ia.run(question)
        if not answer:
            return
        audio.run(answer)


def main():
    asyncio.run(user_flow())
    # microphone.run()
    # camera.run()
    # ia.run()
    # ecran.run()


if __name__ == "__main__":
    print("=" * 42)
    print("HACKATHON : Robot Python - 16/17 Aout 2023")
    print("=" * 42)
    main()
