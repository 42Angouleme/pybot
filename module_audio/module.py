import pyttsx3


# il faut que ma string soit en global/static sur ce fichier.
def run(txt="Bonjour et Bienvenue dans le projet ROBOTECH!"):
    print("Hello Module Audio")
    print("\ten cours...")

    # To initialize the motor
    engine = pyttsx3.init('espeak')

    # Define the text to be converted into speech:
    txt_1 = "42 est une des meilleure écoles du monde."

    # Adjusting speech rate and volume:
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 100)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.50)

    # Select language and track type:
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'mb-fr1')
    # engine.setProperty('voice', 'fr')

    # Print the message:
    engine.say(txt)
    engine.runAndWait()
    print("\tfin.")
