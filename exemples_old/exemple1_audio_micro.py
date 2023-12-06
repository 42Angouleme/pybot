#! venv/bin/python3

from pybot import module_audio as audio
from pybot import module_microphone as micro

# TODO an import is missing for skimage
# import module_ia as ia

# from module_micro import listen


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
    # asyncio.run(chat_bot())
    micro.run()
    # audio.run()
    # ia.run()
    # ecran.run()


if __name__ == "__main__":
    print("=" * 12)
    print("Robot Python")
    print("=" * 12)
    main()
