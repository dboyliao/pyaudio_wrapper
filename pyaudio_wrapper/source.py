__all__ = ["Microphone"]

## Import standard libraries.
from functools import wraps

## Import necessary third party packages.
from scipy.io import wavfile
import pyaudio

## Import submodules.
from ._source_abc import AudioSource
from .exceptions import DeviceTypeError

def _under_audio_context(method):
	"""
	A decorator which makes the instance method can only work
	under audio context.

	ex:
		with AudioSource() as source: .....

	Raise:
		RunTimeError
	"""

	@wraps(method)
	def wrapped(self, *args, **kwargs):
		if self.audio is None:
			raise RuntimeError("Working outside of source context")
		return method(self, *args, **kwargs)

	return wrapped

class Microphone(AudioSource):

	## Reimplement all required abstract methods
	def __init__(self, device_index = None, sample_rate = None, bit_width = None, chunk_size = 1024, channels = 1):
		
		### Checking the parameters ###
		audio = pyaudio.PyAudio()
		if device_index is not None:
			assert isinstance(device_index, int), "Device index must be None or an integer"
			# ensure device index is in range
			# obtain device count
			count = audio.get_device_count()
			assert 0 <= device_index < count, "`device_index` out of range: {} out of {}".format(device_index, count)
			self.device_index = device_index
			if self.device_info["maxInputChannels"] > 0:
				self.device_type = "input"
			else:
				self.device_type = "output"
		else:
			# if device_index is None, using default input index.
			self.device_index = audio.get_default_input_device_info()["index"]
			self.device_type = "input"
		audio.terminate()

		assert isinstance(chunk_size, int) and chunk_size > 0, "`chunck_size` must be positive."

		# 16-bit bit width. 
		# Note that the BYTE_WIDTH property is the size of each sample in term of bytes
		# which will be look up according to BIT_WIDTH property
		if bit_width is None:
			self.__format = pyaudio.paInt16
		else:
			self.__format = pyaudio.get_format_from_width(bit_width)

		self.__bit_width = pyaudio.get_sample_size(self.__format)
		
		# sampling rate in Hertz
		if sample_rate is not None:
			assert isinstance(sample_rate, int), "`sample_rate` must be integer."
			self.__sample_rate = sample_rate
		else:
			self.__sample_rate = int(self.device_info["defaultSampleRate"])

		# 1 for mono audio, 2 for stereor audio.
		assert channels in (1, 2), "`channels` can be either 1 or 2."
		self.__channels = channels 

		# number of frames stored in each buffer
		self.__chunk_size = chunk_size 

		# audio resource and streams.
		self.__audio = None
		self.__input_stream = None
		self.__output_stream = None

	@property
	def device_info(self):
		"""
		Private helper function: get related parameters of default device.
		"""

		audio = pyaudio.PyAudio()
		device_info = audio.get_device_info_by_index(self.device_index)
		audio.terminate()
		return device_info

	def __enter__(self):
		assert self.audio is None, "This audio source is already inside a context manager."
		self.audio = pyaudio.PyAudio()
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.close()

	## Reimplement all required properties.
	@property
	def audio(self):
		return self.__audio

	@audio.setter
	def audio(self, value):
		if value is not None and not isinstance(value, pyaudio.PyAudio):
			raise ValueError("`audio` can only be of type {} or `None`".format(pyaudio.PyAudio))
		else:
			self.__audio = value

	@property
	def BIT_WIDTH(self):
		return self.__bit_width

	@BIT_WIDTH.setter
	def BIT_WIDTH(self, value):
		if not self.__bit_width is None:
			raise RuntimeError("It is not allowed to modify the `BIT_WIDTH`.")
		else:
			self.__bit_width = value

	@property
	def BYTE_WIDTH(self):
		return pyaudio.get_sample_size(self.BIT_WIDTH)

	@BYTE_WIDTH.setter
	def BYTE_WIDTH(self, value):
		raise RuntimeError("It is not allowed to modify the `BYTE_WIDTH`.")

	@property
	def SAMPLE_RATE(self):
		return self.__sample_rate

	@SAMPLE_RATE.setter
	def SAMPLE_RATE(self, value):
		if isinstance(value, int):
			raise ValueError("The sample")
		else:
			self.__sample_rate = value

	@property
	def CHANNELS(self):
		return self.__channels

	@CHANNELS.setter
	def CHANNELS(self, value):
		if not self.__channels is None:
			raise RuntimeError("It is not allowd to modifyt the `CHANNELS`.")
		else:
			self.__channels = value

	@property
	def CHUNK_SIZE(self):
		return self.__chunk_size

	@CHUNK_SIZE.setter
	def CHUNK_SIZE(self, value):
		if not self.__chunk_size is None:
			raise RuntimeError("It is not allowd to modifyt the `CHUNK_SIZE`.")
		else:
			self.__chunk_size = value

	@property
	def FORMAT(self):
		return self.__format

	@FORMAT.setter
	def FORMAT(self, value):
		raise RuntimeError("Not allow to modify the format.")

	## Other useful properties and methods
	@_under_audio_context
	def read(self, chunk_size = None):
		
		if not self.device_type == "input":
			raise DeviceTypeError("Can not read from a non-input device.")

		if chunk_size is None:
			data = bytes(self.input_stream.read(self.CHUNK_SIZE))
		else:
			assert isinstance(chunk_size, int), "`chunk_size` must be integer."
			data = bytes(self.input_stream.read(chunk_size))
		return data

	@_under_audio_context
	def write(self, data):
		if not self.device_type == "output":
			raise DeviceTypeError("Can not write to a non-output device.")

		self.output_stream.write(chunk_size)

	@_under_audio_context
	def close(self):
		if self.device_type == "output":
			self.output_stream.stop_stream()
			self.output_stream.close()
		elif self.device_type == "input":
			self.input_stream.stop_stream()
			self.input_stream.close()
		self.audio.terminate()
		self.audio = None

	@property
	def input_stream(self):
		if self.device_type is not "input":
			raise DeviceTypeError("The device type is not a input stream.")

		if self.audio is None:
			raise RuntimeError("Working outside of source context")

		self.__input_stream = self.audio.open(
			input_device_index = self.device_index,
			format = self.BIT_WIDTH,
			rate = self.SAMPLE_RATE,
			channels = self.CHANNELS,
			frames_per_buffer = self.CHUNK_SIZE,
			input = True
			)
		return self.__input_stream

	@input_stream.setter
	def input_stream(self, value):
		if value is not None:
			raise RuntimeError("Can not modify `input_stream` once it was assigned.")
		else:
			self.__input_stream = value

	@property
	def output_stream(self):

		if not self.device_type is "output":
			raise DeviceTypeError("The device type is not a output stream.")
		
		if self.audio is None:
			raise RuntimeError("Working outside of source context")
		self.__output_stream = self.audio.open(
			input_device_index = self.device_index,
			format = self.BIT_WIDTH,
			rate = self.SAMPLE_RATE,
			channels = self.CHANNELS,
			frames_per_buffer = self.CHUNK_SIZE,
			output = True
			)
		return self.__output_stream

	@output_stream.setter
	def output_stream(self, value):
		if value is not None:
			raise RuntimeError("Can not modify `output_stream` once it was assigned.")
		else:
			self.__output_stream = value

class WavAudio(AudioSource):

	def __init__(self):
		pass

	def __enter__(self):
		pass

	def __exit__(self):
		pass

	@property
	def audio(self):
		pass

	@property
	def CHUNK_SIZE(self):
		pass

	@property
	def BIT_WIDTH(self):
		pass

	@property
	def BYTE_WIDTH(self):
		pass

	@property
	def SAMEPLE_RATE(self):
		pass

	@property
	def CHANNELS(self):
		pass

	@_under_audio_context
	def read(self):
		pass

	@_under_audio_context
	def write(self):
		pass

	@_under_audio_context
	def play(self, start = None, end = None):
		pass
