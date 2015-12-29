"""
The `source` submodule: a module which defines all available audio source.
"""

__all__ = ["Microphone", "AudioSource"]

## Import standard libraries.
from functools import wraps
import os, sys

## Import necessary third party packages.
from scipy.io import wavfile
import pyaudio

## Import submodules.
from ._source_abc import AudioSourceABC
from ._utils import _under_audio_context
from .audio_data import AudioData, WavAudioData
from .exceptions import DeviceTypeError

if sys.version_info >= (3, ):
    long = int

class AudioSource(AudioSourceABC):

    ## Reimplement all required abstract methods
    def __init__(self, device_index, sample_rate, bit_width, chunk_size = 8092, channels = 1):

        audio = pyaudio.PyAudio()
        ## Checking the device_index is valid or not.
        assert isinstance(device_index, (int, long)), "Device index must be an integer."
        device_count = audio.get_device_count()
        assert 0 <= device_index < device_count, "`device_index` out of range: {} out of {}".format(device_index, count)
        audio.terminate()
        self.__device_index = device_index

        if not self.device_info["maxInputChannels"] > 0:
            raise DeviceTypeError("Can not source from a non-input device.")

        self.__format = pyaudio.get_format_from_width(bit_width)
        self.__bit_width = pyaudio.get_sample_size(self.FORMAT)

        assert isinstance(sample_rate, (int, long)), "`sample_rate` must be integer."
        
        max_sample_rate = self.device_info["defaultSampleRate"]
        assert 0 < sample_rate <= max_sample_rate, "`sample_rate` out of range: {} out of {}".format(sample_rate, max_sample_rate)
        self.__sample_rate = sample_rate

        assert isinstance(chunk_size, (int, long)), "`chunk_size` must be integer."
        self.__chunk_size = chunk_size

        assert channels in [1, 2], '`channels` can be either 1 or 2. 1 for mono audio, 2 for stereo.' 
        self.__channels = channels

        # audio resource and streams.
        self.__audio = None
        self.__input_stream = None

    @property
    def device_index(self):
        return self.__device_index


    @property
    def device_info(self):
        audio = pyaudio.PyAudio()
        info = audio.get_device_info_by_index(self.device_index)
        audio.terminate()
        return info

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def start(self):
        assert self.audio is None, "This audio source is already inside a context manager."
        self.audio = pyaudio.PyAudio()
        self.input_stream.start_stream()

    @_under_audio_context
    def close(self):
        
        self.input_stream.stop_stream()
        self.input_stream.close()
        self.input_stream = None

        self.audio.terminate()
        self.audio = None

    @_under_audio_context
    def read(self, chunk_size = None):

        if chunk_size is None:
            data = bytes(self.input_stream.read(self.CHUNK_SIZE))
        else:
            assert isinstance(chunk_size, int), "`chunk_size` must be integer."
            data = bytes(self.input_stream.read(chunk_size))
        return data

    @property
    def audio(self):
        return self.__audio

    @audio.setter
    def audio(self, value):
        if value is not None and not isinstance(value, pyaudio.PyAudio):
            raise ValueError("`audio` can only be of type {} or `None`".format(pyaudio.PyAudio))
        else:
            self.__audio = value

    ## Reimplement all required properties.
    @property
    def BIT_WIDTH(self):
        return self.__bit_width

    @BIT_WIDTH.setter
    def BIT_WIDTH(self, value):
        raise RuntimeError("It is not allowed to modify the `BIT_WIDTH`.")

    @property
    def SAMPLE_RATE(self):
        return self.__sample_rate

    @SAMPLE_RATE.setter
    def SAMPLE_RATE(self, value):
        raise RuntimeError("It is not allowed to modify the `SAMPLE_RATE`.")
        
    @property
    def CHANNELS(self):
        return self.__channels

    @CHANNELS.setter
    def CHANNELS(self, value):
        raise RuntimeError("It is not allowd to modifyt the `CHANNELS`.")
        
    @property
    def CHUNK_SIZE(self):
        return self.__chunk_size

    @CHUNK_SIZE.setter
    def CHUNK_SIZE(self, value):
        raise RuntimeError("It is not allowd to modifyt the `CHUNK_SIZE`.")
        
    @property
    def FORMAT(self):
        return self.__format

    @FORMAT.setter
    def FORMAT(self, value):
        raise RuntimeError("Not allow to modify the format.")

    ## Other useful properties and methods
    @property
    @_under_audio_context
    def input_stream(self):

        if self.__input_stream is not None:
            return self.__input_stream
        else:
            self.__input_stream = self.audio.open(
                input_device_index = self.device_index,
                format = self.audio.get_format_from_width(self.BIT_WIDTH),
                rate = self.SAMPLE_RATE,
                channels = self.CHANNELS,
                frames_per_buffer = self.CHUNK_SIZE,
                input = True,
                start = False)
            return self.__input_stream

    @input_stream.setter
    def input_stream(self, value):
        if value is not None:
            raise RuntimeError("Can not modify `input_stream` once it was assigned.")
        else:
            self.__input_stream = value


class Microphone(AudioSource):

    
    def __init__(self, bit_width = 2, chunk_size = 8092, channels = 1):
        
        audio = pyaudio.PyAudio()
        info = audio.get_default_input_device_info()
        audio.terminate()
        
        device_index = int(info["index"])
        sample_rate = int(info["defaultSampleRate"])

        super(Microphone, self).__init__(device_index = device_index,
                                         sample_rate = sample_rate,
                                         bit_width = bit_width,
                                         chunk_size = chunk_size,
                                         channels = channels)
