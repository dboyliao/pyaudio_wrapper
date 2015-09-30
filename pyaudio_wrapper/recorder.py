__all__ = ["Recorder"]

# standard libraries.
from io import BytesIO
import wave, os, audioop

# third party packages
import pyaudio
import matplotlib.pylab as plt
from scipy.io import wavfile

# submodules
from .audio_data import AudioData, WavAudioData
from ._source_abc import AudioSource
from ._recorder_abc import AbstractRecorder

class Recorder(AbstractRecorder):

	def __init__(self):
		self.__wav_data = None

	## Reimplement required methods ##
	def record(self, source, offset = 0, max_pause_time = 3, adjust_ambient_noise = False, wav = True, verbose = False):
		"""
		Return the recorded audio data.

		source: An AudioSource instance.
		offset: offset of time in second.
		"""

		self.set_source(source)
		seconds_per_chunk = float(self.source.CHUNK_SIZE)/ self.source.SAMPLE_RATE # seconds per chunk.

		if adjust_ambient_noise:
			energy_threshold = self.get_ambient_noice_energy(sample_time = max_pause_time)
		else:
			energy_threshold = 50

		start_phase = False
		offset_reached = False
		pause_time = 0
		elapsed_time = 0
		frames = []

		while True:
			data = self.source.read()
			elapsed_time += seconds_per_chunk
			
			if elapsed_time > offset:
				offset_reached = True

			## Start phase till detecting sound.
			energy = audioop.rms(data, self.source.BIT_WIDTH)
			if energy > energy_threshold:
				frames.append(data)
				print energy
				start_phase = True

			if start_phase and offset_reached:
				if verbose:
						print "Sound detected. Start recording."
				while True:
					data = self.source.read()
					if audioop.rms(data, self.source.BIT_WIDTH) < energy_threshold:
						pause_time += seconds_per_chunk
					else:
						frames.append(data)
						pause_time = 0
					if pause_time >= max_pause_time:
						break
				
				byte_data = b''.join(frames)
		if wav:
			return WavAudioData(byte_data, source.SAMPLE_RATE, source.BIT_WIDTH, source.CHANNELS)
		
		return AudioData(byte_data, source.SAMPLE_RATE, source.BIT_WIDTH, source.CHANNELS)

	def get_ambient_noice_energy(self, sample_time = 3):

		assert isinstance(sample_time, int), "`sample_time` must be integer."

		print "Detecting ambient noice level."
		print "Please keep silent for {} second(s).".format(sample_time)
		frames = []
		elapsed_time = 0
		seconds_per_chunk = float(self.source.CHUNK_SIZE) / self.source.SAMPLE_RATE 
		
		while elapsed_time < sample_time:
			frames.append(self.source.read())
			elapsed_time += seconds_per_chunk
		
		data = b''.join(frames)
		energy = audioop.rms(data, self.source.BIT_WIDTH)
		return energy


	def set_source(self, source):
		if not isinstance(source, AudioSource):
			raise ValueError("`source` must be of type {}".format(AudioSource))
		self.__source = source

	@property
	def source(self):
		return self.__source

	@source.setter
	def source(self, value):
		raise RuntimeError("Not allowed to directly modify `source` attribute. Use set_resource method instead.")

