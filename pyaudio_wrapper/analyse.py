__all__ = ["AudioAnalysor"]

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft

from .audio_data import AudioData

class AudioAnalysor(object):

    def __init__(self, audio_data):

        self.set_audio_data(audio_data)

    @property
    def audio_data(self):
        return self.__audio_data

    @audio_data.setter
    def audio_data(self, value):
        raise RuntimeError("Use `set_audio_data` method to set the current audio data.")

    def set_audio_data(self, audio_data):
        if not isinstance(audio_data, AudioData):
            raise ValueError("`audio_data` must be of type {}.".format(AudioData))
        self.__audio_data = audio_data


    def fft(self):
        pass

    def plot(self, title = "WAV Signal", xlabel = "Time (seconds)", ylabel = "Altitude", by_sec = True):
        if self.audio_data.CHANNELS == 1: # mono audio
            plt.title(title)
            if by_sec:
                seconds = np.linspace(0, len(self.audio_data.data)/self.audio_data.SAMPLE_RATE, num = len(self.audio_data.data))
                plt.plot(seconds, self.audio_data.data)
            else:
                plt.plot(self.audio_data.data)
        elif self.audio_data.CHANNELS == 2: # stereo audio
            plt.title(title)
            plt.subplot('211')
            

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def denoice(self, audio_data):
        pass