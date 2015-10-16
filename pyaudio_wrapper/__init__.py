__authors__ = ("Dboy Liao")
__version__ = ("1", "0", "0")
__license__ = "BSD"
__doc__     = "A wrapper build on pyaudio, scipy and numpy in order to provide a friendly api for audio data analysis."
__all__ = ["Recorder", "Microphone"]

from .recorder import Recorder
from .source import Microphone
