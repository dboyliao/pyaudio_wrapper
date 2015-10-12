__all__ = ["AudioAnalysor"]

import matplotlib.pyplot as _plt
import numpy as _np
import scipy.fftpack as _fftpack
import scipy.signal as _sg

from .audio_data import AudioData as _AudioData

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
        if not isinstance(audio_data, _AudioData):
            raise ValueError("`audio_data` must be of type {}.".format(AudioData))
        self.__audio_data = audio_data


    def fft(self, plot = False, colors = 'rb', normalize = False):
        
        coefs = []
        data = self.audio_data.data

        if normalize:
            if self.audio_data.dtype in [_np.uint8, _np.uint16, _np.uint32]:
                data = 2.*data/2**(8*self.audio_data.BIT_WIDTH) - 1
            elif self.audio_data.dtype in [_np.int8, _np.int16, _np.int32]:
                data = 2.*data/2**(4*self.audio_data.BIT_WIDTH) - 1
            else:
                print "[Warning] Unrecognized dtype detected."

        if self.audio_data.CHANNELS == 1: # mono audio data
            # Take only the coef for the positive freq since the data is real-valued.
            N = len(self.audio_data.data)
            c1 = _fftpack.fft(data)[:N/2]
            coefs.append(c1)
        else: # stereo audio data
            N = len(self.audio_data.data[0])
            c1 = _fftpack.fft(data[0])[:N/2]
            coefs.append(c1)
            c2 = _fftpack.fft(data[1])[:N/2]
            coefs.append(c2)

        if plot:
            _plt.title("Fast Fourier Transform")
            for i in range(len(coefs)):
                coef = coefs[i]
                color = colors[i]
                axe = _plt.subplot("{}1{}".format(self.audio_data.CHANNELS, i+1))
                axe.title.set_text("Channel {}".format(i+1))
                axe.plot(abs(coef[1:N/2]), color)
            _plt.show()
        return coefs
            

    def plot(self, by_sec = True, color = 'br'):

        if self.audio_data.CHANNELS == 1: # mono audio
            if by_sec:
                x = _np.linspace(0, len(self.audio_data.data)/self.audio_data.SAMPLE_RATE, num = len(self.audio_data.data))
                x_label = "Time (Seconds)"
            else:
                x = _np.linspace(0, len(self.audio_data.data), num = len(self.audio_data.data))
                x_label = "Samples"
            _plt.title("Channel 1")
            _plt.plot(x, self.audio_data.data, color[0])
            _plt.xlabel(x_label)
            _plt.ylabel("Altitude")
        else: # stereo audio 
            if by_sec:
                x = _np.linspace(0, len(self.audio_data.data[0])/self.audio_data.SAMPLE_RATE, num = len(self.audio_data.data[0]))
                x_label = "Time (Seconds)"
            else:
                x = _np.linspace(0, len(self.audio_data.data[0]), num = len(self.audio_data.data[0]))
                x_label = "Sambles"
            for i in range(self.audio_data.CHANNELS):
                axe = _plt.subplot("{}1{}".format(self.audio_data.CHANNELS, i+1))
                axe.title.set_text("Channel {}".format(i + 1))
                axe.plot(x, self.audio_data.data[i], color[i])
                axe.set_xlabel(x_label)
                axe.set_ylabel("Altitude")
        _plt.tight_layout()
        _plt.show()

    def get_analytic_signal(self):
        return _sg.hilbert(self.audio_data.data)

    def get_envelop(self):
        ana_sig = self.get_analytic_signal()
        return np.abs(ana_sig)

    def denoise(self, method = 'energy', **kwargs):
        """
        Denoise the audio data.

        `params`:
            `method` <string>: available values --> 'energy', .

        `return`:
            audio_data_denoised <AudioData>: An AudioData instance of denoised audio.
        """
        
        if method == 'energy':
            self.set_audio_data(self.__denoise_by_energy(**kwargs))
        elif method == 'freq':
            self.set_audio_data(self.__denoise_by_freq(**kwargs))
        else:
            pass

    def __denoise_by_energy(self, threshold = None):
        pass

    def __denoise_by_freq(self, threshold = None):
        pass

