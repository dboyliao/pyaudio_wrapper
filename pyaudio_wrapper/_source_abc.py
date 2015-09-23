__all__ = ["AudioSource"]

from abc import ABCMeta, abstractmethod

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


class AudioSource(object):

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

	@_abstractmethod
	def write(self):
		pass

	@_abstractmethod
	def close(self):
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

