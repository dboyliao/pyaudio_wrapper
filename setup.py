#!/usr/bin/env python

import os, sys
from setuptools import setup, find_packages
from pyaudio_wrapper import __authors__, __version__, __license__

if sys.platform == "win32":
    print "Sorry, I don't know how to install this package on windows."
    print "Though pyaudio and portaudio are cross-platform."
    print "Aborting install."

    sys.exit(1)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), "r").read()


setup(
    name = "pyaudio_wrapper",
    version = ".".join(__version__),
    author = ", ".join(__authors__),
    author_email = "qmalliao@gmail.com",
    description = ("A simple wrapper of PyAudio."),
    long_description = read("README.md"),
    license = __license__,
    keywords = "pyaudio wrapper",
    url = "https://github.com/dboyliao/Python_Audio_Utilities/tree/micro_phone",
    packages = find_packages(exclude = ['tests']),
    install_requires = ["pyaudio", 
                        "numpy", 
                        "scipy",
                        "matplotlib"]
)
