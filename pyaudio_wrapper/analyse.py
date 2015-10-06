__all__ = ["AudioAnalysor"]

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft

from .audio_data import AudioData

class AudioAnalysor(object):

    __doc__ = "Audio Analysor: object to analyse the audio data such as plot, fft,...etc."

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


    def fft(self, plot = False, colors = 'rb', normalize = False):
        
        coefs = []
        data = self.audio_data.data

        if normalize:
            if self.audio_data.dtype in [np.uint8, np.uint16, np.uint32]:
                data = 2.*data/2**(8*self.audio_data.BIT_WIDTH) - 1
            elif self.audio_data.dtype in [np.int8, np.int16, np.int32]:
                data = 2.*data/2**(4*self.audio_data.BIT_WIDTH) - 1
            else:
                print "[Warning] Unrecognized dtype detected."

        if self.audio_data.CHANNELS == 1: # mono audio data
            # Take only the coef for the positive freq since the data is real-valued.
            N = len(self.audio_data.data)
            c1 = fft(data)[:N/2]
            coefs.append(c1)
        else: # stereo audio data
            N = len(self.audio_data.data[0])
            c1 = fft(data[0])[:N/2]
            coefs.append(c1)
            c2 = fft(data[1])[:N/2]
            coefs.append(c2)

        if plot:
            plt.title("Fast Fourier Transform")
            for i in range(len(coefs)):
                coef = coefs[i]
                color = colors[i]
                axe = plt.subplot("{}1{}".format(self.audio_data.CHANNELS, i+1))
                axe.title.set_text("Channel {}".format(i+1))
                axe.plot(abs(coef[1:N/2]), color)
            plt.show()
        return coefs
            

    def plot(self, by_sec = True, color = 'br'):

        if self.audio_data.CHANNELS == 1: # mono audio
            if by_sec:
                x = np.linspace(0, len(self.audio_data.data)/self.audio_data.SAMPLE_RATE, num = len(self.audio_data.data))
                x_label = "Time (Seconds)"
            else:
                x = np.linspace(0, len(self.audio_data.data))
                x_label = "Samples"
            plt.title("Channel 1")
            plt.plot(x, self.audio_data.data, color[0])
            plt.xlabel(x_label)
            plt.ylabel("Altitude")
        else: # stereo audio 
            if by_sec:
                x = np.linspace(0, len(self.audio_data.data[0])/self.audio_data.SAMPLE_RATE, num = len(self.audio_data.data[0]))
                x_label = "Time (Seconds)"
            else:
                x = np.linspace(0, len(self.audio_data.data[0]))
                x_label = "Sambles"
            for i in range(self.audio_data.CHANNELS):
                axe = plt.subplot("{}1{}".format(self.audio_data.CHANNELS, i+1))
                axe.title.set_text("Channel {}".format(i + 1))
                axe.plot(x, self.audio_data.data[i], color[i])
                axe.set_xlabel(x_label)
                axe.set_ylabel("Altitude")
        plt.tight_layout()
        plt.show()

    def denoise(self, method = 'energy', **kwargs):
        """
        Denoise the audio data.

        `params`:
            `method` <string>: available values --> 'energy', (to be added).

        `return`:
            audio_data_denoised <AudioData>: An AudioData instance of denoised audio.
        """
        
        if method == 'energy':
            self.set_audio_data(self.__denoise_by_energy(**kwargs))
        else:
            pass

    def __denoise_by_energy(threshold = None):
        pass

