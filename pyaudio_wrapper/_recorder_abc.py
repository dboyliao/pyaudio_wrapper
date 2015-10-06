__all__ = ["AbstractRecorder"]

from abc import ABCMeta
from ._utils import _abstractmethod

class AbstractRecorder(object):
    """
    Recorder Abstract Base Class.

    This class is for definding the spec of Recorder class.
    """

    __metaclass__ = ABCMeta

    @_abstractmethod
    def record(self):
        pass
