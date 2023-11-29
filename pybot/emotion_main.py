#! venv/bin/python3

import asyncio

import module_ia as ia
from time import sleep


async def emotion_bot():
    choices = ["colère", "ennui", "bonheur", "fatigue", "salutation"]
    print(
        f"Écrit moi, après chaque phrase, je choisirais le mot qui correspond parmis [{', '.join(choices)}]. Si rien ne correspond je répondrait 'unknown'. Ecrit 'stop' pour arrêter."
    )
    while True:
        try:
            question = input()
            if "stop" in question.lower():
                break
            answer = ia.get_emotion(question, choices)
            print(answer)
        except Exception as e:
            print(f"Une erreur est survenue: {e}")
            break
        print("--- (wait 2sec)")
        sleep(2)
    print("Bye !")


def main():
    asyncio.run(emotion_bot())


if __name__ == "__main__":
    print("=" * 42)
    print("HACKATHON : Robot Python - 16/17 Aout 2023")
    print("=" * 42)
    main()
