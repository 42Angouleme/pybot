#! venv/bin/python3

from . import module_haut_parleur as speaker
from . import module_microphone as micro
from . import module_ia as ia

async def chat_bot():
    print('J\'écoute... à tout moment tu peux dire le mot "STOP" pour arrêter.')
    while True:
        try:
            question = listen.one_phrase().as_text()
            print("Tu as dis: " + question)
            if "stop" in question.lower():
                speaker.run(txt="Tu as dis STOP... au revoir, humain.")
                break
            answer = ia.run(question)
            if answer:
                speaker.run(txt=answer)
        except Exception as e:
            print(f"Une erreur est survenue: {e}")
            break
        print('J\'écoute... à tout moment tu peux dire le mot "STOP" pour arrêter.')
    print("Bye !")


def main():
    # asyncio.run(chat_bot())
    micro.run()
    # speaker.run()
    # ia.run()
    # fenetre.run()


if __name__ == "__main__":
    print("=" * 12)
    print("Robot Python")
    print("=" * 12)
    main()
