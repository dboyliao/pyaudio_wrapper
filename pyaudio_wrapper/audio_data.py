__all__ = ["AudioData"]

import io, wave
import pyaudio

class AudioData(object):

	def __init__(self, data, sample_rate, sample_width, channels):
		assert sample_rate > 0, "`sample_rate` must be positive."
		assert isinstance(sample_width, int) and sample_width > 0, "`sample_width` must be positive integer."
		assert channels in (1, 2), "`channels` can be either 1(mono) or 2(stereo) only."

		self.data = data # a byte string
		self.sample_rate = sample_rate
		self.sample_width = sample_width
		self.format = pyaudio.get_format_from_width(self.sample_width)
		self.channels = channels

	@property
	def wav_data(self):
		"""
		Convert original byte string into wav formated data.
		"""

		with io.BytesIO() as wav_file:
			try:
				wav_writer = wave.open(wav_file, "wb")
				wav_writer.setframerate(self.sample_rate)
				wav_writer.setsampwidth(self.sample_width)
				wav_writer.setnchannels(self.channels)
				wav_writer.writeframes(self.data)
			except ValueError as e:
				raise e
			finally:
				wav_writer.close()
			data = wav_file.getvalue()
		return data

	@wav_data.setter
	def wav_data(self, value):
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
		output_stream.write(self.wav_data)
		output_stream.stop_stream()
		output_stream.close()
		audio.terminate()
