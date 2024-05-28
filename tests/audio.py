import pyaudio
import wave
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
# import whisper
# import openai

def read_audio(file: str):
    # length of data to read.
    chunk = 1024

    '''
    ************************************************************************
        This is the start of the "minimum needed to read a wave"
    ************************************************************************
    '''
    # open the file for reading.
    wav_file = wave.open(file, 'rb')

    # create an audio object
    audio = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = audio.open(
        format=audio.get_format_from_width(wav_file.getsampwidth()),
        channels=wav_file.getnchannels(),
        rate=wav_file.getframerate(),
        output=True
    )

    # read data (based on the chunk size)
    data = wav_file.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    while data:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wav_file.readframes(chunk)

    # cleanup stuff.
    wav_file.close()
    stream.close()
    audio.terminate()

def record_audio(filename, duration, fs=44100):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, recording.astype(np.int16))  # Save as WAV file
    print("Recording finished.")

record_audio("tmp.wav", 4)
read_audio("tmp.wav")
