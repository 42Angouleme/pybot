#! /bin/python3
import module_microphone as microphone
import module_audio as audio

# TODO an import is missing for skimage
# import module_camera as camera
import module_ia as ia
import module_ecran as ecran

from module_microphone import listen
import asyncio


async def chat_bot():
    print('J\'écoute... à tout moment tu peux dire le mot "STOP" pour arrêter.')
    while True:
        try:
            question = listen.one_phrase().as_text()
            print("Tu as dis: " + question)
            if "stop" in question.lower():
                audio.run(txt="Tu as dis STOP... au revoir, humain.")
                break
            answer = ia.run(question)
            if answer:
                audio.run(txt=answer)
        except Exception as e:
            print(f"Une erreur est survenue: {e}")
            break
        print('J\'écoute... à tout moment tu peux dire le mot "STOP" pour arrêter.')

    print("Bye !")


def main():
    asyncio.run(chat_bot())
    # microphone.run()
    # camera.run()
    # ia.run()
    # ecran.run()


if __name__ == "__main__":
    print("=" * 42)
    print("HACKATHON : Robot Python - 16/17 Aout 2023")
    print("=" * 42)
    main()
