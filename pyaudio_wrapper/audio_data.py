__all__ = ["AudioData", "WavAudioData"]

import io, wave
from scipy.io import wavfile
import pyaudio

class AudioData(object):

	def __init__(self, byte_data, sample_rate, bit_width, channels):
		"""
		byte_data: A byte string containing the raw data.
		bit_width: bit width in bytes.
		"""
		
		try:
			bit_width = pyaudio.get_sample_size(pyaudio.get_format_from_width(bit_width))
		except ValueError as e:
			raise e
		
		assert isinstance(channels, int) and channels in [1, 2], "`channels` can be either 1(mono) or 2(stereo)."
		assert channels in (1, 2), "`channels` can be either 1(mono) or 2(stereo) only."
		
		assert sample_rate > 0, "`sample_rate` must be positive."
		
		assert isinstance(bit_width, int) and bit_width > 0, "`bit_width` must be positive integer."
		

		self.bit_width = bit_width
		self.byte_data = byte_data # a byte string
		self.channels = channels
		self.sample_rate = sample_rate

	@property
	def data(self):
		"""
		Convert raw byte data ot numeric data.
		"""
		if self.bit_width == 1:
			data_array = np.fromstring(self.byte_data, dtype = np.int8)
		elif self.bit_width == 2:
			data_array = np.fromstring(self.byte_data, dtype = np.int16)
		elif self.bit_width == 4:
			data_array = np.fromstring(self.byte_data, dtype = np.int32)
		elif self.bit_width == 3:
			# Since numpy does not have 3 bytes data type, 
			# using np.int32 instead. Be caution with 24-bits audio data.
			data_array = np.fromstring(self.byte_data, dtype = np.int32)
		if self.channels == 1:
			return data_array
		elif self.channels == 2:
			return data_array.reshape((data_array/2, 2))
		else:
			return None

	@data.setter
	def data(self, value):
		raise RuntimeError("It is not allowed to modify this attribute.")

	@property
	def duration(self):
		if self.channels == 2:
			return len(self.data.T[0])/self.sample_rate
		return len(self.data)/self.sample_rate


class WavAudioData(AudioData):

	def __init__(self, *args, **kwargs):
		super(WavAudioData, self).__init__(*args, **kwargs)
		self.format = pyaudio.get_format_from_width(self.bit_width)

	@property
	def raw_wav_data(self):
		"""
		Convert original byte string into wav formated data.
		"""

		with io.BytesIO() as wav_file:
			try:
				wav_writer = wave.open(wav_file, "wb")
				wav_writer.setframerate(self.sample_rate)
				wav_writer.setsampwidth(self.bit_width)
				wav_writer.setnchannels(self.channels)
				wav_writer.writeframes(self.byte_data)
			except ValueError as e:
				raise e
			finally:
				wav_writer.close()
			data = wav_file.getvalue()
		return data

	@raw_wav_data.setter
	def raw_wav_data(self, value):
		raise RuntimeError("It is not allowed to modify this attribute.")

	def play(self):
		audio = pyaudio.PyAudio()
		output_device_info = audio.get_default_output_device_info()
		output_stream = audio.open(
						output_device_index = output_device_info["index"],
						output = True,
						format = self.format,
						rate = self.sample_rate,
						channels = self.channels)
		output_stream.write(self.raw_wav_data)
		output_stream.stop_stream()
		output_stream.close()
		audio.terminate()

	def save(self, fname, path = None):
		assert fname.endswith("wav"), "The file extension must be wav."
		if path is None:
			path = os.getcwd()

		file_path = os.path.abspath(os.path.join(path, fname))

		with open(file_path, "wb") as wav_file:
			wav_file.write(self.raw_wav_data)
