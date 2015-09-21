# A Simple Audio Wrapper of PyAudio

[`PyAudio`](https://people.csail.mit.edu/hubert/pyaudio/) is a python bindings for [`PortAudio`](http://www.portaudio.com/). However, the api, to my humble opinion, is not so friendly to the programmer who has no deep or comprehensive knowledge about audio data. This package is yet again another wrapper build upon `PyAudio` in order to provide a friendly api.

# Basic Usage (Probably the ONLY Usage. XD)

```{python}
from pyaudio_wrapper.recorder import Recorder

rr = Recorder() # Recording the sound from default microphone.
rr.plot() # Plot out the wav file.
rr.play() # play out the wav file.
```