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
from ._source_abc import AudioSource

class Recorder(object):

	def __init__(self):

		self.__wav_data = None
		self.current_source = None

	def listen(self, source, duration = None, offset = None):
		pass

	def record(self, source, duration = None, offset = None):
		"""
		source: An AudioSource instance.
		"""
		if not isinstance(source, AudioSource):
			raise ValueError("`source` must be of type {}".format(AudioSource))
		self.current_source = source
		wav_bytes = BytesIO()
		seconds_per_buffer = float(source.CHUNK_SIZE) / source.SAMPLE_RATE
		elapsed_time = 0
		offseted_time = 0
		offset_reached = False
		
		with BytesIO() as wav_bytes:
			while True:

				if offset and not offset_reached:
					offset_time += seconds_per_buffer
					if offseted_time > offset:
						offset_reached = True

				audio_buffer = source.read()
				if len(audio_buffer) == 0: break

				if offset_reached or offset is None:
					elapsed_time += seconds_per_buffer
					if duration and elapsed_time > duration: break

					wav_bytes.write(audio_buffer)
			self.__wav_data = wav_bytes.getvalue()

	@property
	def wav_data(self):
		if self.__wav_data is None:
			raise RuntimeError("You have to record audio firsrt.")

		with BytesIO() as wav_file:
			wav_writer = wave.open(wav_file, "wb")
			try:
				wav_writer.setframerate(self.current_source.SAMPLE_RATE)
				wav_writer.setsamplewidth(self.current_source.BIT_WIDTH)
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
		assert filename.endswith("wav"), "Only save as wav format."
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

	def __init__(self):
		super(MicrophoneRecorder, self).__init__()
		self.source = Microphone()

	def listen(self, duration = None, offset = None):
		super(MicrophoneRecorder, self).listen(source = self.source,
											   duration = duration,
											   offset = offset)