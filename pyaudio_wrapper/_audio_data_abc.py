__all__ = ["AudioDataABC"]

from abc import ABCMeta
from ._utils import _abstract_property

class AudioDataABC(object):
    """
    AudioData Abstract Base Class.

    This class is for definding the spec of AudioData class.
    """
    
    __metaclass__ = ABCMeta

    @_abstract_property
    def CHANNELS(self):
        pass

    @_abstract_property
    def SAMPLE_RATE(self):
        pass

    @_abstract_property
    def BIT_WIDTH(self):
        pass

    @_abstract_property
    def BYTE_DATA(self):
        pass