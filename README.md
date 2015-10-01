# A Simple Audio Wrapper of PyAudio

[`PyAudio`](https://people.csail.mit.edu/hubert/pyaudio/) is a python bindings for [`PortAudio`](http://www.portaudio.com/). However, the api, to my humble opinion, is not so friendly to the programmer who has no deep or comprehensive knowledge about audio data. This package is yet again another wrapper build upon `PyAudio` in order to provide a friendly api.

# Basic Usage

## Working with WAV Audio Data

```{python}
from pyaudio_wrapper.audio_data import WavFileAudioData

wav_file = WavFileAudioData("path/to/your/wavfile")

wav_file.raw_wav_data # Get the raw wav data in bytes.
wav_file.duration     # duration of the audio file in seconds.
wav_file.data         # A numpy array of the wav audio data.
wav_file.play()       # Play out the audio.
wav_file.play(start = 3, stop = 10) # Play the audio from 3 sec to 10 sec.
```

## Recording Audio Data From Microphone

```{python}
from pyaudio_wrapper import Recorder
from pyaudio_wrapper.source import Microphone

recorder = Recorder() # Recording the sound from default microphone.
with Microphone() as source:
    wav_audio = recorder.record(source)

wav_audio.play()             # play out the audio.
wav_audio.data               # an numpy array of this audio data
wav_audio.save('record.wav') # save the audio as a wav file.
```

## Analyse Audio Data

```{python}
from pyaudio_wrapper.analyse import Analysor

analysor = Analysor(wav_audio)
analysor.plot() # plot the audio data.
analysor.fft() # fast fourier transform.
```

# Installation

```
git clone https://github.com/dboyliao/pyaudio_wrapper.git
cd pyaudio_wrapper
make install      # Run `make uninstall` if you want to uninstall this package. 
```

# Reference

- This package is inspired by the `speech_recognition` module by `Uberi`. [GitHub](https://github.com/Uberi/speech_recognition)
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/docs/index.html#)
- [24-bits Scipy](https://github.com/scipy/scipy/issues/1930)
- [24-bits wave](http://stackoverflow.com/questions/16767248/how-do-i-write-a-24-bit-wav-file-in-python)
- [IOError](http://stackoverflow.com/questions/28174540/ioerror-errno-input-overflowed-9981)