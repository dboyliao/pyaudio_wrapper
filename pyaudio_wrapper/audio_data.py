__all__ = ["AudioData", "WavAudioData", "WavFileAudioData"]

import io, wave, os
import numpy as np
from scipy.io import wavfile
import pyaudio

from ._audio_data_abc import AudioDataABC

class AudioData(AudioDataABC):

	def __init__(self, byte_data, sample_rate, bit_width, channels):
		"""
		byte_data: A byte string containing the raw data.
		BIT_WIDTH: bit width in bytes.
		"""
		
		try:
			assert isinstance(bit_width, (int, long)) and bit_width > 0, \
					"`bit_width` must be positive integer."
			bit_width = pyaudio.get_sample_size(pyaudio.get_format_from_width(bit_width))
		
		except ValueError as e:
			raise e
		
		assert isinstance(channels, int) and channels in [1, 2], \
				"`channels` can be either 1(mono) or 2(stereo)."
		assert channels in (1, 2), \
				"`channels` can be either 1(mono) or 2(stereo) only."
		
		assert sample_rate > 0, "`sample_rate` must be positive."

		self.__bit_width = bit_width
		self.__channels = channels
		self.__sample_rate = sample_rate
		self.__byte_data = byte_data # a byte string

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
			data_array = np.fromstring(self.BYTE_DATA, dtype = np.int8)
		elif self.BIT_WIDTH == 2:
			data_array = np.fromstring(self.BYTE_DATA, dtype = np.int16)
		elif self.BIT_WIDTH == 4:
			data_array = np.fromstring(self.BYTE_DATA, dtype = np.int32)
		elif self.BIT_WIDTH == 3:
			# Since numpy does not have 3 bytes data type, 
			# using np.int32 instead. Be caution with 24-bits audio data.
			data_array = np.fromstring(self.BYTE_DATA, dtype = np.int32)
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
		Duration in second.
		"""
		if self.CHANNELS == 2:
			return len(self.data[0])/self.SAMPLE_RATE
		return len(self.data)/self.SAMPLE_RATE

	def __getitem__(self, i):
		return self.data[:,i]


class WavAudioData(AudioData):

	def __init__(self, *args, **kwargs):
		super(WavAudioData, self).__init__(*args, **kwargs)
		self.format = pyaudio.get_format_from_width(self.BIT_WIDTH)

	@property
	def raw_wav_data(self):
		"""
		Raw WAV audio data.
		"""
		return self.__get_raw_wav_data_from_byte(self.BYTE_DATA, self.CHANNELS)

	@raw_wav_data.setter
	def raw_wav_data(self, value):
		raise RuntimeError("It is not allowed to modify this attribute.")

	def __get_raw_wav_data_from_byte(self, byte_data, channels):
		"""
		Convert original byte data into wav formated byte data.
		"""
		with io.BytesIO() as wav_file:
			try:
				wav_writer = wave.open(wav_file, "wb")
				wav_writer.setframerate(self.SAMPLE_RATE)
				wav_writer.setsampwidth(self.BIT_WIDTH)
				wav_writer.setnchannels(channels)
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
		if not array.shape[1] == 2:
			array = array.T

		with io.BytesIO() as wav_file:
			wavfile.write(wav_file, self.SAMPLE_RATE, array)
			data = wav_file.getvalue()
		return data


	def play(self, start = 0, stop = None):
		"""
		Play the audio data by default output device.

		`start` <float>: where to start playing the audio (in seconds).
		`stop` <float>: where to stop playing the audio (in seconds).
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
			output_stream.write(self.raw_wav_data)
		else:
			start_index = int(round(self.SAMPLE_RATE * start))
			if stop is not None:
				stop_index = int(round(self.SAMPLE_RATE * stop))
			else:
				stop_index = stop

			data = self.__get_raw_wav_data_from_array(self[start_index:stop_index])
			output_stream.write(data)

		output_stream.stop_stream()
		output_stream.close()
		audio.terminate()

	def save(self, fname, path = None):
		"""
		Save audio data as wav file.

		Params:
			fname (string): wav file name.
			path (string): path to the directory where to save this wav file. It
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
		wav_file = wave.open(fname, "rb")
		data_buffer = wav_file.readframes(1024)
		data = []
		while len(data_buffer) > 0:
			data.append(data_buffer)
			data_buffer = wav_file.readframes(1024)
		else:
			byte_data = b''.join(data)
		super(WavFileAudioData, self).__init__(byte_data = byte_data, 
											   sample_rate = wav_file.getframerate(),
											   bit_width = wav_file.getsampwidth(),
											   channels = wav_file.getnchannels())
