#!/usr/bin/python

from lightUtil import *
from time import sleep
from runStrobe import strobe
import sys


def runCYM(inst, slp_time=4, blk_time=2):
    all = group(inst, range(0, inst.number))
    inst.setDebug(0)    

    while True:
	strobe(all, cyan,    slp_time, blk_time)
	strobe(all, yellow,  slp_time, blk_time)
	strobe(all, magenta, slp_time, blk_time)

if __name__=="__main__":
    try:
	test = lights(4)
	if len(sys.argv) == 3:
            runCYM(test,float(sys.argv[1]),float(sys.argv[2]))
	elif len(sys.argv) == 2:
	    runCYM(test,float(sys.argv[1]),float(sys.argv[1]))
	else:
	    runCYM(test)
    except:
	test.reset()
