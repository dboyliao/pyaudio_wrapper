#!/usr/bin/env python

import subprocess
import sys

if __name__ == "__main__":
	n = int(sys.argv[1])
	for i in range(n):
		subprocess.call("./record_sound.py -o noise_{}.wav".format(i), shell = True)
