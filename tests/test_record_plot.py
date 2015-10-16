#!/usr/bin/env python

from pyaudio_wrapper import Microphone, Recorder
from pyaudio_wrapper.analyse import AudioAnalysor
from pyaudio_wrapper.exceptions import PauseTimeout

r = Recorder()

while True:
    try:
        with Microphone(channels = 2) as source:
            print "Start recording"
            audio_data = r.record(source, verbose = True)

        a = AudioAnalysor(audio_data)
        a.plot(by_sec = False)
        a.show()
    except PauseTimeout:
        to_break = raw_input("Break process? ([y]/n): ")
        if to_break.lower().startswith("y"):
            break

    name = raw_input("Do you want to save the file?\nEnter the file name (leave it blank if not): ")
    if name is not "":
        audio_data.save("%s.wav" % name)
