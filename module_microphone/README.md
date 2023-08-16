# Module microphone

## Setup

### Dependencies

```sh
# For pyaudio
$ sudo apt-get install portaudio19-dev

```

### OpenAi API configuration [paid option]

- Create an account on https://platform.openai.com/account/
- Setup a billing account, the charge is 0,006 ct per minute. That is 0,36 ct per hour of recording.
- Generate an API key, copy the API key
- in a terminal 

``` sh
$ export OPENAI_API_KEY=replace_with_your_api_key
$ export OPENAI_ORG_ID=replace_with_your_organisation_id

# Find your organisation ID at https://platform.openai.com/account/org-settings
```


## Info

These dependencies are in `../requirement.txt`
```
SpeechRecognition  3.10.0
PyAudio            0.2.13
pydub              0.25.1
```



