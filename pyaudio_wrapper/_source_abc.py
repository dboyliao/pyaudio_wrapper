__all__ = ["AudioSourceABC"]

from abc import ABCMeta
from ._utils import _abstractmethod, _abstract_property

class AudioSourceABC(object):
    """
    AudioSource Abstract Base Class.

    This class is for definding the spec of AudioSource class.
    """

    __metaclass__ = ABCMeta

    @_abstractmethod
    def __init__(self):
        pass

    @_abstractmethod
    def __enter__(self):
        pass

    @_abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @_abstractmethod
    def read(self):
        pass

    @_abstract_property
    def CHUNK_SIZE(self):
        pass

    @_abstract_property
    def BIT_WIDTH(self):
        pass

    @_abstract_property
    def BYTE_WIDTH(self):
        pass

    @_abstract_property
    def CHANNELS(self):
        pass

    @_abstract_property
    def SAMPLE_RATE(self):
        pass

    @_abstract_property
    def FORMAT(self):
        pass
