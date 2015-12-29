__all__ = ["AudioData", "WavAudioData", "WavFileAudioData"]

import io, wave, os, audioop, sys
import numpy as np
from scipy.io import wavfile
import pyaudio

from ._audio_data_abc import AudioDataABC

if sys.version_info > (3,):
    long = int

class AudioData(AudioDataABC):

    def __init__(self, byte_data, sample_rate, bit_width, channels, dtype = None):
        """
        byte_data: A byte string containing the raw data.
        BIT_WIDTH: bit width in bytes.
        """
        
        assert isinstance(bit_width, (int, long)) and bit_width > 0, \
                "`bit_width` must be positive integer."
        bit_width = pyaudio.get_sample_size(pyaudio.get_format_from_width(bit_width))
        
        assert isinstance(channels, int) and channels in [1, 2], \
                "`channels` can be either 1(mono) or 2(stereo)."
        assert channels in (1, 2), \
                "`channels` can be either 1(mono) or 2(stereo) only."
        
        assert sample_rate > 0, "`sample_rate` must be positive."

        self.__bit_width = bit_width
        self.__channels = channels
        self.__sample_rate = sample_rate
        self.__byte_data = byte_data # a byte string

        if dtype is None:
            dtype = self._get_dtype_by_bit_width()

        if not self._validate_dtype(dtype):
            raise ValueError("`dtype` is not compatible with the `bit_width`.")

        self.__dtype = dtype
        self.format = pyaudio.get_format_from_width(self.BIT_WIDTH)

    def _validate_dtype(self, dtype):

        if self.BIT_WIDTH == 1 and dtype in [np.int8, np.uint8]:
            return True
        elif self.BIT_WIDTH == 2 and dtype in [np.int16, np.uint16]:
            return True
        elif self.BIT_WIDTH == 3 and dtype in [np.int32, np.uint32]:
            return True
        elif self.BIT_WIDTH == 4 and dtype in [np.int32, np.uint32]:
            return True

        return False

    def _get_dtype_by_bit_width(self):

        if self.BIT_WIDTH == 1:
            return np.int8
        elif self.BIT_WIDTH == 2:
            return np.int16
        elif self.BIT_WIDTH in [3, 4]:
            return np.int32

    @property
    def dtype(self):
        return self.__dtype

    @dtype.setter
    def dtype(self, value):
        raise RuntimeError("It is not allowed to modify this attribute.")

    @property
    def BIT_WIDTH(self):
        """
        bit width in bytes.
        """
        return self.__bit_width

    @BIT_WIDTH.setter
    def BIT_WIDTH(self, value):
        raise RuntimeError("It is not allowed to modify this attribute.")

    @property
    def CHANNELS(self):
        """
        number of channels.
        """
        return self.__channels

    @CHANNELS.setter
    def CHANNELS(self, value):
        raise RuntimeError("It is not allowed to modify this attribute.")

    @property
    def SAMPLE_RATE(self):
        """
        sample rate. (# of sample / sec)
        """
        return self.__sample_rate

    @SAMPLE_RATE.setter
    def SAMPLE_RATE(self, value):
        raise RuntimeError("It is not allowed to modify this attribute.")

    @property
    def BYTE_DATA(self):
        """
        raw byte data of frames.
        """
        return self.__byte_data

    @BYTE_DATA.setter
    def BYTE_DATA(self):
        raise RuntimeError("It is not allowed to modify this attribute.")

    @property
    def data(self):
        """
        Numeric presentation of the raw data.
        """
        if self.BIT_WIDTH == 1:
            data_array = np.fromstring(self.BYTE_DATA, dtype = self.dtype)
        elif self.BIT_WIDTH == 2:
            data_array = np.fromstring(self.BYTE_DATA, dtype = self.dtype)
        elif self.BIT_WIDTH == 4:
            data_array = np.fromstring(self.BYTE_DATA, dtype = self.dtype)
        elif self.BIT_WIDTH == 3:
            # Since numpy does not have 3 bytes data type, 
            # using np.int32 instead. Be caution with 24-bits audio data.
            data_array = np.fromstring(self.BYTE_DATA, dtype = self.dtype)
        if self.CHANNELS == 1:
            return data_array.T
        elif self.CHANNELS == 2:
            return data_array.reshape((len(data_array)/2, 2)).T
        else:
            return None

    @data.setter
    def data(self, value):
        raise RuntimeError("It is not allowed to modify this attribute.")

    @property
    def duration(self):
        """
        Duration in millisecond.
        """
        
        return int(round(len(self)*1000/float(self.SAMPLE_RATE)))

    def play(self, start = 0, stop = None):
        """
        params:
          `start`: start time in millisecond.
          `stop`: stop time in millisecond
        """
        
        assert isinstance(start, (float, int)) and start >= 0, "`start` must be non-negative number."
        assert isinstance(stop, (float, int)) and stop > start or stop is None, "`stop` can be either non-negative number or None. If it is a number, it must be larger than `start`."

        audio = pyaudio.PyAudio()
        output_device_info = audio.get_default_output_device_info()
        output_stream = audio.open(
                        output_device_index = output_device_info["index"],
                        output = True,
                        format = self.format,
                        rate = self.SAMPLE_RATE,
                        channels = self.CHANNELS)
        if start == 0 and stop is None:
            output_stream.write(self.BYTE_DATA)
        else:
            start_index = int(round(self.SAMPLE_RATE * start / 1000.))
            if stop is not None:
                stop_index = int(round(self.SAMPLE_RATE * stop / 1000.))
            else:
                stop_index = stop

            data = self.data[start_index:stop_index] if self.CHANNELS == 1 else self.data[:, start_index:stop_index].T
            output_stream.write(data.tostring())

        output_stream.stop_stream()
        output_stream.close()
        audio.terminate()

    def convert_sample_rate(self, out_rate):
        new_byte_data, _ = audioop.ratecv(self.BYTE_DATA,
                                       self.BIT_WIDTH,
                                       self.CHANNELS,
                                       self.SAMPLE_RATE,
                                       out_rate,
                                       None)
        self.__sample_rate = out_rate
        self.__byte_data = new_byte_data

    def __getitem__(self, i):

        start = i.start
        step = i.step
        stop = i.stop

        assert start is None or round(start) == start, "The start index must be integer or integer like (in millisecond)."
        assert stop is None or round(stop) == stop, "The stop index must be integer or integer like (in millisecond)."
        assert step is None or round(step) == step, "The step index must be integer or integer like (in millisecond)."


        start_index = round(start/1000. * self.SAMPLE_RATE) if start is not None else start
        stop_index = round(stop/1000. * self.SAMPLE_RATE) if stop is not None else stop

        s = slice(start_index, stop_index, step)

        if self.CHANNELS == 1:
            data = self.data[s].T
        elif self.CHANNELS == 2:
            data = self.data[:, s].T

        return type(self)(data.tostring(), 
                          self.SAMPLE_RATE,
                          self.BIT_WIDTH, 
                          self.CHANNELS,
                          self.dtype)

    def __len__(self):
        if self.CHANNELS == 1:
            return len(self.data)
        elif self.CHANNELS == 2:
            return len(self.data[0])
        else:
            return None

    def __repr__(self):
        samprate = self.SAMPLE_RATE
        bit_width = self.BIT_WIDTH
        channels = 'mono' if self.CHANNELS == 1 else "stereo"
        return "WAV Audio: %s, %s, %s" % (samprate, bit_width, channels)

    def __str__(self):
        dest_string = "data: {}\nbit width: {}\nsample rate: {}\nnumber of frames: {}\n"
        return dest_string.format(repr(self.data), self.BIT_WIDTH, self.SAMPLE_RATE, len(self))

    def __add__(self, other):
        """
        Concatenate two audio data.
        """

        if not isinstance(other, AudioData):
            raise ValueError("Can concatenate with object of type {} only.".format(AudioData))
        if not self.BIT_WIDTH == other.BIT_WIDTH:
            raise ValueError("Both audio data should have the same bit width.")
        if not self.SAMPLE_RATE == other.SAMPLE_RATE:
            raise ValueError("Both audio data should have the same sample rate.")

        new_byte_data = b''.join([self.BYTE_DATA, other.BYTE_DATA])
        return type(self)(new_byte_data, self.SAMPLE_RATE, self.BIT_WIDTH, self.CHANNELS, self.dtype)


    def __mul__(self, factor):
        """
        Implement audio_data * factor
        """

        if not isinstance(factor, (int, float)):
            return NotImplemented # passing the job to factor.__rmul__
        new_byte_data = audioop.mul(self.BYTE_DATA, self.BIT_WIDTH, factor)
        return type(self)(new_byte_data, self.SAMPLE_RATE, self.BIT_WIDTH, self.CHANNELS, self.dtype)

    def __rmul__(self, factor):
        """
        Implement factor * audio_data
        """

        if not isinstance(factor, (int, float)):
            raise ValueError("Can only multiply audio data by number.")
        
        return self * factor


class WavAudioData(AudioData):        

    @property
    def raw_wav_data(self):
        """
        Raw WAV audio data.
        """
        
        return self.__get_raw_wav_data_from_byte(self.BYTE_DATA)

    @raw_wav_data.setter
    def raw_wav_data(self, value):
        raise RuntimeError("It is not allowed to modify this attribute.")

    def __get_raw_wav_data_from_byte(self, byte_data):
        """
        Convert original byte data into wav formated byte data.
        """

        with io.BytesIO() as wav_file:
            try:
                wav_writer = wave.open(wav_file, "wb")
                wav_writer.setframerate(self.SAMPLE_RATE)
                wav_writer.setsampwidth(self.BIT_WIDTH)
                wav_writer.setnchannels(self.CHANNELS)
                wav_writer.writeframes(byte_data)
            except ValueError as e:
                raise e
            finally:
                wav_writer.close()
            wav_data = wav_file.getvalue()
        return wav_data

    def __get_raw_wav_data_from_array(self, array):
        """
        `array`: a 1-D or a 2-D numpy array.
        """

        if array.ndim == 2:
            array = array.T

        with io.BytesIO() as wav_file:
            wavfile.write(wav_file, self.SAMPLE_RATE, array)
            data = wav_file.getvalue()
        return data

    def save(self, fname, path = None):
        """
        Save audio data as wav file.

        Params:
            fname <string>: wav file name.
            path <string>: path to the directory where to save this wav file. It
                           is by default the current working directory. 
        """

        assert fname.endswith("wav"), "The file extension must be wav."
        if path is None:
            path = os.getcwd()
        else:
            path = os.path.abspath(path)
        fname = os.path.abspath(fname)

        file_path = os.path.abspath(os.path.join(path, fname))

        with open(file_path, "wb") as wav_file:
            wav_file.write(self.raw_wav_data)

class WavFileAudioData(WavAudioData):

    def __init__(self, fname):

        fname = os.path.abspath(fname)
        sample_rate, data = wavfile.read(fname)
        if data.ndim == 2:
            channels = 2
        else:
            channels = 1

        if data.dtype in [np.int8, np.uint8]:
            bit_width = 1
        elif data.dtype in [np.int16, np.uint16]:
            bit_width = 2
        else:
            bit_width = 4
        
        byte_data = data.tostring()
        
        super(WavFileAudioData, self).__init__(byte_data = byte_data, 
                                               sample_rate = sample_rate,
                                               bit_width = bit_width,
                                               channels = channels,
                                               dtype = data.dtype)
        self.fname = fname

    def __repr__(self):

        return 'WAV File: %s' % self.fname

    def __add__(self, other):
        """
        Concatenate two audio data.
        """

        if not isinstance(other, AudioData):
            raise ValueError("Can concatenate with object of type {} only.".format(AudioData))
        if not self.BIT_WIDTH == other.BIT_WIDTH:
            raise ValueError("Both audio data should have the same bit width.")
        if not self.SAMPLE_RATE == other.SAMPLE_RATE:
            raise ValueError("Both audio data should have the same sample rate.")

        new_byte_data = b''.join([self.BYTE_DATA, other.BYTE_DATA])
        return WavAudioData(new_byte_data, self.SAMPLE_RATE, self.BIT_WIDTH, self.CHANNELS, self.dtype)


    def __mul__(self, factor):
        """
        Implement audio_data * factor
        """

        if not isinstance(factor, (int, float)):
            return NotImplemented # passing the job to factor.__rmul__
        new_byte_data = audioop.mul(self.BYTE_DATA, self.BIT_WIDTH, factor)
        
        return WavAudioData(new_byte_data, self.SAMPLE_RATE, self.BIT_WIDTH, self.CHANNELS, self.dtype)

    def __rmul__(self, factor):
        """
        Implement factor * audio_data
        """
        
        if not isinstance(factor, (int, float)):
            raise ValueError("Can only multiply audio data by number.")
        
        return self * factor

    def __getitem__(self, i):
        
        start = i.start
        step = i.step
        stop = i.stop

        assert start is None or round(start) == start, "The start index must be integer or integer like (in millisecond)."
        assert stop is None or round(stop) == stop, "The stop index must be integer or integer like (in millisecond)."
        assert step is None or round(step) == step, "The step index must be integer or integer like (in millisecond)."

        start_index = round(start/1000. * self.SAMPLE_RATE) if start is not None else start
        stop_index = round(stop/1000. * self.SAMPLE_RATE) if stop is not None else stop

        s = slice(start_index, stop_index, step)

        if self.CHANNELS == 1:
            data = self.data[s].T
        elif self.CHANNELS == 2:
            data = self.data[:, s].T

        return WavAudioData(data.tostring(), 
                            self.SAMPLE_RATE,
                            self.BIT_WIDTH, 
                            self.CHANNELS,
                            self.dtype)
