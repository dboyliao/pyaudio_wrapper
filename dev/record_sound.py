#!/usr/bin/env python

import argparse
import pyaudio, wave

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--out", dest = "out")
parser.add_argument("-n", type = int, default = 100, dest = "n")


if __name__ == "__main__":
	args = parser.parse_args()
	output_file =  args.out
	n = args.n

	CHUNK_SIZE = 8092
	RATE = 44100
	BIT_WIDTH = 2
	CHANNELS = 1

	audio = pyaudio.PyAudio()

	input_stream = audio.open(input = True,
							  frames_per_buffer = CHUNK_SIZE,
							  channels = CHANNELS,
							  rate = RATE,
							  format = pyaudio.get_format_from_width(BIT_WIDTH))
	frames = []
	for _ in range(n):
		data_buffer = input_stream.read(CHUNK_SIZE)
		frames.append(data_buffer)

	input_stream.stop_stream()
	input_stream.close()
	data = b''.join(frames)
	wav_writer = wave.open(output_file, "wb")
	wav_writer.setframerate(RATE)
	wav_writer.setsampwidth(BIT_WIDTH)
	wav_writer.setnchannels(CHANNELS)
	wav_writer.writeframes(data)
	wav_writer.close()
	audio.terminate()
