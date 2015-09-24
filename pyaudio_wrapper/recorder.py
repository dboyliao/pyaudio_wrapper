__all__ = ["MicrophoneRecorder", "Recorder"]

# standard libraries.
from io import BytesIO
import wave, os

# third party packages
import pyaudio
import matplotlib.pylab as plt
from scipy.io import wavfile

# submodules
from .source import Microphone
from .audio_data import AudioData
from ._source_abc import AudioSource
from ._recorder_abc import AbstractRecorder

class Recorder(AbstractRecorder):

	def __init__(self):

		self.__wav_data = None
		self.current_source = None

	## Reimplement required methods ##
	def listen(self, source, timeout = None):
		if not isinstance(source, AudioSource):
			raise ValueError("`source` must be of type {}".format(AudioSource))
		pass

	def record(self, source, duration = 10, offset = 0):
		"""
		Record the audio data for a duration of time with offset. By default,
		the duration will be 10 seconds and offset will be 0.

		source: An AudioSource instance.
		duration: duration of time in second.
		offset: offset of time in second.
		"""

		if not isinstance(source, AudioSource):
			raise ValueError("`source` must be of type {}".format(AudioSource))
		assert isinstance(duration, int), "`duration` must be integer."
		assert isinstance(offset, int) and offset > 0, "`offset` must be non-negative integer."

		self.current_source = source
		seconds_per_buffer = float(source.CHUNK_SIZE) / source.SAMPLE_RATE
		elapsed_time = 0
		offseted_time = 0
		offset_reached = False
		
		with BytesIO() as frames:
			while True:

				if not offset_reached:
					offset_time += seconds_per_buffer
					if offseted_time > offset:
						offset_reached = True

				audio_buffer = source.read()
				if len(audio_buffer) == 0: break

				if offset_reached:
					elapsed_time += seconds_per_buffer
					if elapsed_time > duration: break

					frames.write(audio_buffer)
			self.__wav_data = frames.getvalue()

	## Helper properties ##
	@property
	def wav_data(self):
		if self.__wav_data is None:
			raise RuntimeError("You have to record audio firsrt.")

		with BytesIO() as wav_file:
			wav_writer = wave.open(wav_file, "wb")
			try:
				wav_writer.setframerate(self.current_source.SAMPLE_RATE)
				wav_writer.setsampwidth(self.current_source.BIT_WIDTH)
				wav_writer.setnchannels(self.current_source.CHANNELS)
				wav_writer.writeframes(self.__wav_data)
			finally:
				wav_writer.close()
			wav_data = wav_file.getvalue()

		return wav_data

	@wav_data.setter
	def wav_data(self, value):
		if value is not None:
			raise RuntimeError("Direct modification is not allowed.")
		self.__wav_data = value

	def save_wav(self, filename, path = None):
		assert filename.endswith("wav"), "The file extension must be wav."
		if path is None:
			path = os.getcwd()

		file_path = os.path.abspath(os.path.join(path, filename))

		with open(file_path, "wb") as wav_file:
			wav_file.write(self.wav_data)

	def plot(self, source):
		# use wavfile.read to get the data and frames_per_second
		pass

	def play(self, offset, duration):
		pass

class MicrophoneRecorder(Recorder):

	def record(self, duration = None, offset = None):
		with Microphone() as source:
			super(MicrophoneRecorder, self).record(source = source,
												   duration = duration,
												   offset = offset)