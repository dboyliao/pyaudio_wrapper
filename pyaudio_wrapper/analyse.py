__all__ = ["AudioAnalysor"]

from itertools import cycle as _cycle

import matplotlib.pyplot as _plt
from matplotlib.widgets import SpanSelector
import numpy as _np
import scipy.fftpack as _fftpack
import scipy.signal as _sg

from .audio_data import AudioData as _AudioData

class AudioAnalysor(object):

    __doc__ = "Audio Analysor: object to analyse the audio data such as plot, fft,...etc."

    def __init__(self, audio_data):

        self.set_audio_data(audio_data)
        self.__temp_selector = []

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


    def fft(self, colors = 'rb', normalize = False, plot = False):
        
        coefs = []
        data = self.audio_data.data
        colors = _cycle(colors)

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

        # plot the spectrum.
        if plot:
            fig, axs = _plt.subplots(len(coefs), 1)
            fig.suptitle("Fast Fourier Transform")

            for i in range(len(coefs)):
                coef = coefs[i]
                color = colors.next()
                ax = axs[i]

                ax.title.set_text("Channel {}".format(i+1))
                ax.plot(abs(coef[1:N/2]), color)
        return coefs

    def plot(self, by_sec = True, colors = None):
        if colors is None:
            colors = _cycle(["#FF6600", "#0033CC"])
        else:
            colors = _cycle(colors)
        
        num_subplots = self.audio_data.CHANNELS + 1
        fig, axs = _plt.subplots(num_subplots, 1)
        fig.suptitle(repr(self.audio_data))
        frames = [self.audio_data.data[i] for i in range(2)] if self.audio_data.CHANNELS == 2 else [self.audio_data.data]

        if by_sec:
            x = _np.linspace(0, len(frames[0])/self.audio_data.SAMPLE_RATE, num = len(frames[0]))
            x_label = "Time (Seconds)"
        else:
            x = _np.linspace(0, len(frames[0]), num = len(frames[0]))
            x_label = "Frame"

        zoom_ax = axs[-1]
        zoom_ax.set_axis_bgcolor("#E6E6B8")
        zoom_ax.xaxis.set_label_text(x_label)
        zoom_ax.yaxis.set_label_text("Altitude")
        zoom_line, = zoom_ax.step([], [], "#008A2E")

        temp = []
        for i, item in enumerate(zip(axs[:-1], frames)):
            color = colors.next()
            ax, frame = item

            ax.title.set_text("Channel {}".format(i+1))
            ax.set_axis_bgcolor("#E6E6B8")
            ax.step(x, frame, color)
            ax.xaxis.set_label_text(x_label)
            ax.yaxis.set_label_text("Altitude")

            def onselect_callback(xmin, xmax):

                indmin, indmax = _np.searchsorted(x, (xmin, xmax))
                indmax = min(len(frames[0]) - 1, indmax)
                x_segment = x[indmin:indmax]
                y_segment = frame[indmin:indmax]
                zoom_line.set_data(x_segment, y_segment)
                zoom_ax.set_xlim(x_segment[0], x_segment[-1])
                zoom_ax.set_ylim(y_segment.min(), y_segment.max())
                _plt.draw()

                start_time = self.audio_data.duration * float(indmin) / len(x)
                stop_time = self.audio_data.duration * float(indmax) / len(x)
                self.audio_data.play(start_time, stop_time)

            self.__temp_selector.append(SpanSelector(ax, onselect_callback, 'horizontal', span_stays = True, 
                                        rectprops = dict(alpha = 0.5, facecolor = 'cyan')))
        
        fig.tight_layout()

    def show(self):
        _plt.show()
        self.__temp_selector = []

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

