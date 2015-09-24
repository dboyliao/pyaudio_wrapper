from functools import wraps

def _under_audio_context(fun):

	@wraps(fun)
	def wrapped(self, *args, **kwargs):
		if self.audio is None:
			raise RuntimeError("Working outside of source context")

		return fun(self, *args, **kwargs)

	return wrapped


class A(object):

	def __init__(self):
		self.audio = None

	@_under_audio_context
	def fun(self, a):
		return a

	def __enter__(self):
		self.audio = "audio"
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.audio = None