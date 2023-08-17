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

then `cd` at the root of the project and run:

```sh
$ pip install -r requirements.txt
```

### Whisper API (OpenAi) configuration [paid option]

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


### Usage

The higher level function is `speech_to_text`. It records audio and give you back a string.

``` py
from module_microphone import speech_to_text

text = speech_to_text(10) # give the duration in second
print(text)
```
The Microphone class let you start recording audio and stop it. A timestamp suffix is added to the filepath you provide.

``` py
mic = Microphone(filepath="/tmp/myaudio.wav")
audio_filepath = mic.record(duration=10)
# The recording automatically stop after 10 sec
print(audio_filepath)
# The file is saved at path `/tmp/myaudio_2023-08-17_12h35m10s.wav`

```

#### No timestamp

``` py
mic = Microphone(filepath="/tmp/myaudio.wav", use_ts_suffix=False)
audio_filepath = mic.record() # default to 5 sec of recording
print(audio_filepath) # The file is saved at path `/tmp/myaudio.wav`

```

#### Customize timestamp

``` py
mic = Microphone(filepath="/tmp/myaudio.wav", filename_ts_suffix_format = "_at_%H-%M")
audio_filepath = mic.record() # default to 5 sec of recording
print(audio_filepath) # The file is saved at path `/tmp/myaudio_at_12-36.wav`

```

#### Debug

``` py
import logging

logging.basicConfig(level=logging.DEBUG)

mic = Microphone(filepath="/tmp/myaudio.wav")
audio_filepath = mic.record()

# Will print debug message when the recording start, stop...
```

## Info

The following dependencies are included in `../requirement.txt`
```
PyAudio==0.2.13
sounddevice==0.4.6
wavio==0.0.7
openai==0.27.8
```


## Research

- I tried SpeechRecognition python package that gathers many input api in a simple package but had complicated issues, many of them are posted on github issues with no answer
- OpenAI speech recognition is great but does not support audio stream which would result in latency and would require to break audio in chunk for file > 25mb
