__all__ = ["MicrophoneRecorder", "Recorder"]

# standard libraries.
from io import BytesIO
import wave, os, audioop, math, collections

# third party packages
import pyaudio
import matplotlib.pylab as plt
from scipy.io import wavfile

# submodules
from .source import Microphone
from .audio_data import AudioData, WavAudioData
from ._source_abc import AudioSource
from ._recorder_abc import AbstractRecorder

class Recorder(AbstractRecorder):

	def __init__(self, pause_threshold = 0.8, phrase_threshold = 0.3, non_speaking_duration = 0.5, energy_threshold = 300, dynamic_energy_adjustment_damping = 0.15, dynamic_energy_ratio = 1.5, dynamic_energy_threshold = True):

		assert pause_threshold >= non_speaking_duration >= 0
		self.energy_threshold = energy_threshold # minimum audio energy to consider for recording
		self.dynamic_energy_threshold = dynamic_energy_threshold
		self.dynamic_energy_adjustment_damping = dynamic_energy_adjustment_damping
		self.dynamic_energy_ratio = dynamic_energy_ratio
		self.pause_threshold = pause_threshold # seconds of non-speaking audio before a phrase is considered complete
		self.phrase_threshold = phrase_threshold # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
		self.non_speaking_duration = non_speaking_duration # seconds of non-speaking audio to keep on both sides of the recording

		self.__wav_data = None
		self.current_source = None

	## Reimplement required methods ##
	def listen(self, source, timeout = None, wav = True):
		if not isinstance(source, AudioSource):
			raise ValueError("`source` must be of type {}".format(AudioSource))
		
		seconds_per_buffer = (source.CHUNK_SIZE + 0.0) / source.SAMPLE_RATE
		pause_buffer_count = int(math.ceil(self.pause_threshold / seconds_per_buffer)) # number of buffers of non-speaking audio before the phrase is complete
		phrase_buffer_count = int(math.ceil(self.phrase_threshold / seconds_per_buffer)) # minimum number of buffers of speaking audio before we consider the speaking audio a phrase
		non_speaking_buffer_count = int(math.ceil(self.non_speaking_duration / seconds_per_buffer)) # maximum number of buffers of non-speaking audio to retain before and after

		# read audio input for phrases until there is a phrase that is long enough
		elapsed_time = 0 # number of seconds of audio read
		while True:
			frames = collections.deque()

			# store audio input until the phrase starts
			while True:
				elapsed_time += seconds_per_buffer
				if timeout and elapsed_time > timeout: # handle timeout if specified
					raise WaitTimeoutError("listening timed out")

				buffer = source.read()
				if len(buffer) == 0: break # reached end of the stream
				frames.append(buffer)
				if len(frames) > non_speaking_buffer_count: # ensure we only keep the needed amount of non-speaking buffers
					frames.popleft()

				# detect whether speaking has started on audio input
				energy = audioop.rms(buffer, source.BIT_WIDTH) # energy of the audio signal
				if energy > self.energy_threshold: break

				# dynamically adjust the energy threshold using assymmetric weighted average
				if self.dynamic_energy_threshold:
					damping = self.dynamic_energy_adjustment_damping ** seconds_per_buffer # account for different chunk sizes and rates
					target_energy = energy * self.dynamic_energy_ratio
					self.energy_threshold = self.energy_threshold * damping + target_energy * (1 - damping)

			# read audio input until the phrase ends
			pause_count, phrase_count = 0, 0
			while True:
				elapsed_time += seconds_per_buffer

				buffer = source.read()
				if len(buffer) == 0: break # reached end of the stream
				frames.append(buffer)
				phrase_count += 1

				# check if speaking has stopped for longer than the pause threshold on the audio input
				energy = audioop.rms(buffer, source.BIT_WIDTH) # energy of the audio signal
				if energy > self.energy_threshold:
					pause_count = 0
				else:
					pause_count += 1
				if pause_count > pause_buffer_count: # end of the phrase
					break

			# check how long the detected phrase is, and retry listening if the phrase is too short
			phrase_count -= pause_count
			if phrase_count >= phrase_buffer_count: break # phrase is long enough, stop listening

		# obtain frame data
		for i in range(pause_count - non_speaking_buffer_count): frames.pop() # remove extra non-speaking frames at the end
		byte_data = b"".join(list(frames))

		if wav:
			return WavAudioData(byte_data, source.SAMPLE_RATE, source.BIT_WIDTH, source.CHANNELS)

		return AudioData(byte_data, source.SAMPLE_RATE, source.BIT_WIDTH, source.CHANNELS)

	def record(self, source, duration = 10, offset = 0, wav = True):
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
			byte_data = frames.getvalue()
		
		if wav:
			return WavAudioData(byte_data, source.SAMPLE_RATE, source.BIT_WIDTH, source.CHANNELS)
		
		return AudioData(byte_data, source.SAMPLE_RATE, source.BIT_WIDTH, source.CHANNELS)

class MicrophoneRecorder(Recorder):

	def record(self, duration = None, offset = None):
		with Microphone() as source:
			super(MicrophoneRecorder, self).record(source = source,
												   duration = duration,
												   offset = offset)