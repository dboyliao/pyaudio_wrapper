#!/usr/bin/env python

import wave, audioop, pyaudio
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-n", type = int, default = 20, dest = 'n')
parser.add_argument("-s", type = int, default = 10, dest = "s")
parser.add_argument("-r", action = "store_true", dest = 'r')

CHUNK_SIZE = 8092
RATE = 44100
BIT_WIDTH = 2
CHANNELS = 1

def record_sound(s):
	audio = pyaudio.PyAudio()
	stream = audio.open(input = True,
						output = True,
						frames_per_buffer = CHUNK_SIZE,
						channels = CHANNELS,
						rate = RATE,
						format = pyaudio.get_format_from_width(BIT_WIDTH))
	frames = []
	for _ in range(s):
		data_buffer = stream.read(CHUNK_SIZE)
		stream.write(data_buffer)
		frames.append(data_buffer)

	data = b''.join(frames)
	stream.stop_stream()
	stream.close()
	return data

def main(args):
	n = args.n
	s = args.s
	r = args.r
	energys = []
	for i in range(n):
		data = record_sound(s)
		energy = audioop.rms(data, BIT_WIDTH)
		energys.append(energy)
		print "Energy of {}th sample:".format(i+1), energy

		if r:
			wav_writer = wave.open("nose_{}_{}.wav".format(i + 1, energy), "wb")
			wav_writer.setsampwidth(BIT_WIDTH)
			wav_writer.setnchannels(CHANNELS)
			wav_writer.setframerate(RATE)
			wav_writer.writeframes(data)
			wav_writer.close()

	print "Mean:", np.mean(energys)
	print "Std.:", np.std(energys)


if __name__ == "__main__":
	args = parser.parse_args()
	main(args)