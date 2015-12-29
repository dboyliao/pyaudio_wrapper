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
from .exceptions import PauseTimeout
from ._source_abc import AudioSourceABC
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

        ## Wait for offset to be reached.
        ## All data read from the source during offset time will be disgard.

        self.set_source(source)
        seconds_per_chunk = float(self.source.CHUNK_SIZE)/ self.source.SAMPLE_RATE # seconds per chunk.

        if adjust_ambient_noise:
            energy_threshold = self.get_ambient_noice_energy(sample_time = max_pause_time)
        else:
            energy_threshold = 50

        if verbose:
            print("The energy threshold has been set as {}. (default: 50)".format(energy_threshold))
        
        offset_reached = False
        elapsed_time = 0

        while not offset_reached:
            
            self.source.read() # The data read during this time is disgarded.
            elapsed_time += seconds_per_chunk
            
            if elapsed_time > offset:
                offset_reached = True

        ## Detecting sound.
        frames = []
        start_phase = False
        while not start_phase:
            data = self.source.read()
            elapsed_time += seconds_per_chunk

            energy = audioop.rms(data, self.source.BIT_WIDTH)
            if energy > energy_threshold:
                frames.append(data)
                start_phase = True
            elif elapsed_time - offset > max_pause_time:
                raise PauseTimeout("Pause time too long. Timeout the recording process.")

        if verbose:
            print("Sound detected. Start recording.")

        pause_time = 0

        while True:

            data = self.source.read()
            if audioop.rms(data, self.source.BIT_WIDTH) < energy_threshold:
                pause_time += seconds_per_chunk
            else:
                pause_time = 0
            
            frames.append(data)

            if pause_time >= max_pause_time:
                if verbose:
                    print('Pause time reached. Stopping recording process.')
                break
                
        byte_data = b''.join(frames)
        if wav:
            return WavAudioData(byte_data, source.SAMPLE_RATE, source.BIT_WIDTH, source.CHANNELS)
        
        return AudioData(byte_data, source.SAMPLE_RATE, source.BIT_WIDTH, source.CHANNELS)

    def get_ambient_noice_energy(self, sample_time = 3):

        assert isinstance(sample_time, int), "`sample_time` must be integer."

        print("Detecting ambient noice level.")
        print("Please keep silent for {} second(s).".format(sample_time))
        
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
        if not isinstance(source, AudioSourceABC):
            raise ValueError("`source` must be of type {}".format(AudioSource))
        self.__source = source

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        raise RuntimeError("Not allowed to directly modify `source` attribute. Use set_resource method instead.")

