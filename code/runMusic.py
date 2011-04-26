#!/usr/bin/python2.5

from lightUtil import *
import wave, audioop, struct, sys, os
from readwav import read_wav
from numpy import *
from numpy.fft import *

def runMusic(songname):
    # Build room with simple groupings
    room = lights(6)
    all = group(room, range(0, room.number))
    window = group(room, [1])
    l_wall = group(room, [2])
    r_wall = group(room, [3])
    b_wall = group(room, [4])

    # read data from file and try to process it
    data = read_wav(songname, 5000000, 5005000)
    try:
        signal = array(data)
        fourier = fft(signal)
        print fourier
        freq = fftfreq(len(signal), .1)
        print freq
        print len(signal)
    except:
	room.reset()


if __name__=="__main__":
    if len(sys.argv) == 2:
	print "Running..."
        runMusic(sys.argv[1])
        print "Done."
    else:
        print "Error: invalid syntax."
        exit() 
