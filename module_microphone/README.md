# Module microphone

## Setup

### Dependencies

```sh
# For pyaudio
$ sudo apt-get install portaudio19-dev

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


## Info

These dependencies are in `../requirement.txt`
```
PyAudio==0.2.13
PyAudio==0.2.13
sounddevice==0.4.6
wavio==0.0.7
```


## Research

- I tried SpeechRecognition python package that gathers many input api in a simple package but had complicated issues, many of them are posted on github issues with no answer
- OpenAI speech recognition is great but does not support audio stream which would result in latency and would require to break audio in chunk for file > 25mb
