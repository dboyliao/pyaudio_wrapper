from pyaudio_wrapper import audio_data
import wave

wav_file = wave.open("./tests/data/my_voice.wav")
data_buffer = wav_file.readframes(1024)
data = [data_buffer]
while True:
    if len(data_buffer) == 0: break
    data_buffer = wav_file.readframes(1024)
    data.append(data_buffer)

byte_data = b''.join(data)