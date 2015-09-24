__all__ = ["AbstractRecorder"]

from abc import ABCMeta, abstractmethod

class AbstractRecorder(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def record(self):
		raise NotImplementedError("Please reimplement this method.")

	@abstractmethod
	def listen(self):
		raise NotImplementedError("Please reimplement this method.")

