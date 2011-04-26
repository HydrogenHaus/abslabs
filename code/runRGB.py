#!/usr/bin/python


from lightUtil import *
from time import sleep
from runStrobe import strobe
import sys

def runRGB(inst, slp_time=1, blk_time=1):
    all = group(inst, range(0, inst.number))

    while True:
	strobe(all, red, slp_time, blk_time)
	strobe(all, green, slp_time, blk_time)
	strobe(all, blue, slp_time, blk_time)

if __name__=="__main__":
    try:
	test = lights(13)
	if len(sys.argv) == 3:
            runRGB(test,float(sys.argv[1]),float(sys.argv[2]))
	elif len(sys.argv) == 2:
	    runRGB(test,float(sys.argv[1]),float(sys.argv[1]))
	else:
	    runRGB(test)
    except:
	test.reset()
