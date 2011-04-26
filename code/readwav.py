#!/usr/bin/python

import wave, audioop, struct, sys, os

def progress(iteration, n):
    sys.stdout.write(os.popen('clear').read())
    print str(iteration)+' of '+str(n)


def read_wav(songname, mark_1=0, mark_2=0):
    file   = wave.open(songname, 'r')
    chanl  = file.getnchannels()
    smwid  = file.getsampwidth()
    smfreq = file.getframerate()
    global tframe
    tframe = file.getnframes()
    if mark_2 == 0:
	mark_2 = tframe
    #print "Channels:      "+str(chanl)
    #print "Sample Width:  "+str(smwid)
    #print "Sample Freq:   "+str(smfreq)
    #print "Total Frames:  "+str(tframe)

    frames = []
    songdata = file.readframes(mark_2)
    mark_toread = mark_2-mark_1
    for mark in range(0, mark_toread):
	pcm = audioop.adpcm2lin(songdata[mark+mark_1],2,None)
	value = struct.unpack('l', pcm[0])
	frames.append(value[0])
	#progress(mark+1, mark_toread)
    file.close()
    return frames


if __name__=="__main__":
    if len(sys.argv) == 2:
        read_wav(sys.argv[1])
        print "Done."
	# print frames[5000000]
    elif len(sys.argv) == 3:
        read_wav(sys.argv[1], 0, int(sys.argv[2]))
        print "Done."
        print str(sys.argv[2])+" of "+str(tframe)
    elif len(sys.argv) == 4:
        read_wav(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
        print "Done."
        print "From frame "+str(sys.argv[2])+" to "+str(sys.argv[3])+"."
    else:
        print "Error: invalid syntax."
        exit()
