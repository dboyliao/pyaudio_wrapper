#!/usr/bin/env python

from pyaudio_wrapper.audio_data import WavFileAudioData
from pyaudio_wrapper.analyse import AudioAnalysor

def main():
    # w = WavFileAudioData("./data/trump_speech.wav")[:10000]
    w = WavFileAudioData("./data/my_voice.wav")
    a = AudioAnalysor(w)
    a.plot()
    a.plot_spectrum()
    a.show()

if __name__ == "__main__":
    main()
