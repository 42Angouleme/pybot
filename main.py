#! venv/bin/python3

import module_audio as audio
from robot import Robot

robot = Robot()

# import module_ia as ia
from module_microphone import listen


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
    # microphone.run()
    # audio.run()
    # ia.run()
    # ecran.run()
    robot.configurer()
    robot.allumer_ecran()
    robot.allumer_camera()


if __name__ == "__main__":
    print("=" * 42)
    print("HACKATHON : Robot Python - 16/17 Aout 2023")
    print("=" * 42)
    main()
