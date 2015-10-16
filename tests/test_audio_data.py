#!/usr/bin/env python

from pyaudio_wrapper import audio_data
import wave

wav_file = wave.open("./data/my_voice.wav")
data_buffer = wav_file.readframes(1024)
data = [data_buffer]
while True:
    if len(data_buffer) == 0: break
    data_buffer = wav_file.readframes(1024)
    data.append(data_buffer)

byte_data = b''.join(data)

a = audio_data.AudioData(byte_data, wav_file.getframerate(), wav_file.getsampwidth(), wav_file.getnchannels())
a.play()
