__all__ = ["AbstractRecorder"]

from abc import ABCMeta
from ._utils import _abstractmethod

class AbstractRecorder(object):
	__metaclass__ = ABCMeta

	@_abstractmethod
	def record(self):
		pass

	@_abstractmethod
	def listen(self):
		pass
