from gtts import gTTS


def run():
    tts = gTTS('bonjour et bienvenue a 42!', lang='fr')
    with open('hello_bonjour.mp3', 'wb') as f:
        tts.write_to_fp(f)
