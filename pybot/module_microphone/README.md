# Module microphone

This module exposes function to record audio and perform speech-to-text.
Speech-to-text uses Whisper API solution (by OpenAI) and requires a billing account.

## Setup

### Dependencies

First install pyaudio dependencies:

```sh
# For Linux
$ sudo apt-get install portaudio19-dev
# For Macos
$ brew install portaudio

```

eventually create / activate a virtual environment then `cd` at the root of the project and install the pip dependencies with:

```sh
$ pip install -r requirements.txt
```

### Whisper API (OpenAi) configuration [paid option]

This API perform speech to text and requires an internet connection.

- Create an billing account on https://platform.openai.com/account/
- Generate an API key, copy the API key
- in a terminal 

``` sh
$ export OPENAI_API_KEY=replace_with_your_api_key
$ export OPENAI_ORG_ID=replace_with_your_organisation_id

# Find your organisation ID at https://platform.openai.com/account/org-settings
```

#### Price

The charge is 0,006 ct per minute. That is 0,36 ct per hour of recording.

## Demo

Follow JupyterLab [setup instruction](../main#setup) and at the root of the repo run:

``` sh
jupyter lab notebooks/modules/microphone.ipynb
```

## Usage

`ecoute` is an instance of `SpeechToText`. Method chaining make it easy to trigger an audio record then transcribe the spoken text.

``` py
from module_microphone import ecoute

print("J'écoute pendant 5 secondes...")
print("Tu as dis: " + ecoute.pendant("5 secondes").transcrire())
```

`une_phrase()` records audio and stop when the speaker takes a break.
`enregistrer_sous(chemin)` save the audio file and can format timestamp.

``` py
from module_microphone import ecoute

chemin = ecoute.une_phrase().enregistrer_sous("/tmp/my_sentence_%Y-%m-%d_%Hh%Mm%Ss.wav").chemin
print(chemin)
```

The return of `une_phrase()` and `une_phrase()` are instance of `TraitementAudio`

``` py
from module_microphone import ecoute

audio: TraitementAudio = ecoute.une_phrase()
texte: str = audio.transcrire()
print(texte)
```

`pour_chaque_phrase(callback)` repeatedly record in the background and every time you take a break, it calls the callback with a configured TraitementAudio instance as argument. This method is non-blocking.

``` py
from module_microphone import ecoute

def print_speech(audio: TraitementAudio):
    print("Je réfléchis...")
    print("Tu as dis: " + audio.transcrire())


ecoute.pour_chaque_phrase(print_speech)
print("Le microphone écoute en arrière plan, il écrira ce que tu dis.\n")

input("Appuies sur une touche pour arrêter.")

ecoute.stop()
print("Arrêt en cours...")
```

## Debug

``` py
import logging

logging.basicConfig(level=logging.DEBUG)

# Will print debug message when the recording start, stop...
```

## Dependencies

The following dependencies are included in `../requirement.txt`
```
PyAudio==0.2.13
openai==0.27.8
SpeechRecognition==3.10.0
dateparser==1.1.8
pytest==7.4.0
```

- [Dateparser](https://dateparser.readthedocs.io/en/latest/) Sert à convertir une date en toutes lettres et vis-versa
- [Pytest](https://docs.pytest.org/en/7.4.x/) Un framework de test en python
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) Rassemble plusieurs API de reconnaissance vocal et fournis des wrapper autour du microphone.
- [OpenAI](https://github.com/openai/openai-python) Wrapper officiel pour interroger OpenAI.
- [PyAudio](https://pypi.org/project/PyAudio/) Permet de jouer et d'enregistrer des fichiers audio.
