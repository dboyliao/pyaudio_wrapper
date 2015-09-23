#!/usr/bin/env python

import os
from setuptools import setup
from pyaudio_wrapper import __authors__, __version__, __license__

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname), "r").read()

setup(
	name = "pyaudio_wrapper",
	version = ".".join(__version__),
	author = ", ".join(__authors__),
	author_email = "qmalliao@gmail.com",
	description = ("A simple wrapper of PyAudio."),
	license = __license__,
	keywords = "pyaudio wrapper",
	url = "https://github.com/dboyliao/Python_Audio_Utilities/tree/micro_phone",
	packages = ["pyaudio_wrapper"],
	install_requires = ["pyaudio", "numpy", "scipy"]
)
