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

## Usage

`listen` is an instance of `SpeechToText`. Method chaining make it easy to trigger an audio record then transcribe the spoken text.

``` py
from module_microphone import listen

print("J'écoute pendant 5 secondes...")
print("Tu as dis: " + listen.during("5 secondes").as_text())
```

`one_phrase()` records audio and stop when the speaker takes a break.
`save(filepath)` save the audio file and can format timestamp.

``` py
from module_microphone import listen

filepath = listen.one_phrase().save("/tmp/my_sentence_%Y-%m-%d_%Hh%Mm%Ss.wav").filepath
print(filepath)
```

The return of `one_phrase()` and `one_sentence()` are instance of `AudioProcessor`

``` py
from module_microphone import listen

audio_processor: AudioProcessor = listen.one_phrase()
txt: str = audio_processor.as_text()
print(txt)
```

`for_each_phrase(callback)` repeatedly record in the background and every time you take a break, it calls the callback with a configured AudioProcessor instance as argument. This method is non-blocking.

``` py
from module_microphone import listen

def print_speech(audio: AudioProcessor):
    print("Je réfléchis...")
    print("Tu as dis: " + audio.as_text())


listen.for_each_phrase(print_speech)
print("Le microphone écoute en arrière plan, il écrira ce que tu dis.\n")

input("Appuies sur une touche pour arrêter.")

listen.stop()
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
