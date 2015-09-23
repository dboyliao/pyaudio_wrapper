__all__ = ["Microphone"]

## Import necessary third party packages.
from scipy.io import wavfile
import pyaudio

## Import submodules.
from ._source_abc import AudioSource
from .exceptions import DeviceTypeError

class Microphone(AudioSource):

	## Reimplement all required abstract methods
	def __init__(self, device_index = None, sample_rate = None, device_type = "input", chunk_size = 1024, channels = 1):
		
		### Checking the parameters ###
		assert device_index is None or isinstance(device_index, int), "Device index must be None or an integer"
		if device_index is not None: # ensure device index is in range
			# obtain device count
			audio = pyaudio.PyAudio()
			count = audio.get_device_count()
			audio.terminate() 
			assert 0 <= device_index < count, "`device_index` out of range: {} out of {}".format(device_index, count)
		assert isinstance(chunk_size, int) and chunk_size > 0, "`chunck_size` must be positive."
		
		self.device_index = device_index
		self.device_type = device_type

		# 16-bit bit width. 
		# Note that the BYTE_WIDTH property is the size of each sample in term of bytes
		# which will be look up according to BIT_WIDTH property
		self.__bit_width = pyaudio.paInt16 
		
		# sampling rate in Hertz
		if sample_rate is None:
			# Using default device supported sample rate.
			default_device_info = self.__get_default_info()
			self.__sample_rate = int(default_device_info["defaultSampleRate"])
		else:
			assert isinstance(sample_rate, int) and sample_rate > 0, "`sample_rate` must be positive."
			self.__sample_rate = sample_rate

		self.__channels = channels # 1 for mono audio, 2 for stereor audio.
		self.__chunk_size = chunk_size # number of frames stored in each buffer

		# audio resource and streams.
		self.__audio = None
		self.__input_stream = None
		self.__output_stream = None

	def __get_default_info(self):
		"""
		Private helper function: get related parameters of default device.
		"""

		audio = pyaudio.PyAudio()
		info_funcs = {"input": audio.get_default_input_device_info,
					  "output": audio.get_default_output_device_info}
		device_info = info_funcs[self.device_type]()
		audio.terminate()
		return device_info


	def read(self):
		if not self.device_type == "input":
			raise DeviceTypeError("Can not read from a non-input device.")
		return self.input_stream.read(self.CHUNK_SIZE)

	def write(self):
		if not self.device_type == "output":
			raise DeviceTypeError("Can not write to a non-output device.")

		return self.output_stream.write(self.CHUNK_SIZE)

	def __enter__(self):
		assert self.__input_stream is None, "This audio source is already inside a context manager."

		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if self.device_type == "input":
			self.input_stream.stop_stream()
			self.input_stream.close()
			self.input_stream = None
		else:
			self.output_stream.stop_stream()
			self.output_stream.close()
			self.input_stream = None
		self.audio.terminate()

	## Reimplement all required properties.
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
		if not self.__sample_rate is None or not value is None:
			raise RuntimeError("It is not allowd to modifyt the `SAMEPLE_RATE`.")
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
	def audio(self):
		if self.__audio is not None:
			self.__audio.terminate()

		self.__audio = pyaudio.PyAudio()
		return self.__audio

	@audio.setter
	def audio(self, value):
		if not self.__audio is None:
			raise RuntimeError("Can not modify the `audio` attribute once it was assigned.")
		elif not isinstance(value, pyaudio.PyAudio):
			raise ValueError("`audio` must be of type {}".format(pyaudio.PyAudio))
		else:
			self.__audio = value

	@property
	def input_stream(self):
		if self.device_type is not "input":
			raise DeviceTypeError("The device type is not a input stream.")
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
		if not self.__input_stream is None:
			raise RuntimeError("Can not modify `input_stream` once it was assigned.")
		else:
			self.__input_stream = value

	@property
	def output_stream(self):
		if not self.device_type is "output":
			raise DeviceTypeError("The device type is not a output stream.")
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
		if not self.__output_stream is None:
			raise RuntimeError("Can not modify `output_stream` once it was assigned.")
		else:
			self.__output_stream = value
