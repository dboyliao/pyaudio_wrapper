__all__ = ["_abstractmethod", "_abstract_property", "_under_audio_context"]
__doc__ = """Utilities Module. All helper functions are defined here.
"""

from abc import abstractmethod
from functools import wraps

def _abstractmethod(fun):
    """
    This decorator will make `fun` be an abstract method which
    will raise NotImplementedError with a proper message.
    """
    
    @abstractmethod
    def wrapped(*args, **kwargs):
        """
        This method is an abstract method.
        """
        message = "You should not call this superclass' method. Please reimplement it: {}".format(fun.__name__)
        raise NotImplementedError(message)

    return wrapped

def _abstract_property(fun):
    """
    This decorator will make `fun` be an abstract propery
    and raise NotImplementedError with proper message.
    """

    @property
    @abstractmethod
    def wrapped(*args, **kwargs):
        """
        This property is an abstract property.
        """
        message = "You must reimplement this abstract property: {}".format(fun.__name__)
        raise NotImplementedError(message)

    return wrapped

def _under_audio_context(method):
    """
    A decorator which makes the instance method can only work
    under audio context.

    ex:
        with AudioSource() as source: .....

    Raise:
        RunTimeError
    """

    @wraps(method)
    def wrapped(self, *args, **kwargs):
        if self.audio is None:
            raise RuntimeError("Working outside of source context")
        return method(self, *args, **kwargs)

    return wrapped