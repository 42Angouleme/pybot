import pyttsx3

def run(txt = "welcome to the audio module"):
    print("Hello Module Audio")

    # To initialize the motor
    engine = pyttsx3.init()

    # Define the text to be converted into speech:
    txt_1 = "life is a game"
    txt_2 = "coucou alex le bo gosse"
    txt_3 = "42 est la meilleure ecole du monde"
    txt_4 = "ces l'heure de la débauche"
    txt_5 = "YOUPI!!!"

    # Adjusting speech rate and volume:
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-80)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume +0.50)

    voices = engine.getProperty('voices')
    #engine.setProperty('voice', voices[26].id)
    engine.setProperty('voice', 'fr')
    #for voice in voices:
     #   print("id " , voice)
    engine.say(txt_3)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume +2.50)
    engine.say(txt_5)
    engine.runAndWait()

    #=============================================
    # voices[0] est pour la voix masculine.
    # voices[26] est pour la voix francaise..
    # Changeons de voix :
    
