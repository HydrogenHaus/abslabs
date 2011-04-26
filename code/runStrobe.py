#!/usr/bin/python


from lightUtil import *
from random import randint
from time import sleep
import sys

def runStrobe(inst, slp_time=4, blk_time=2):
    all = group(inst, range(0, inst.number))
    
    while True:
	strobe(all, white, slp_time, blk_time)

def strobe(grp, color, slp_time, blk_time):
	grp.setColor(color)
	sleep(slp_time)
	grp.setColor(black)
	sleep(blk_time)

if __name__=="__main__":
    try:
	test = lights(50)
	if len(sys.argv) == 3:
            runStrobe(test,float(sys.argv[1]),float(sys.argv[2]))
	elif len(sys.argv) == 2:
	    runStrobe(test,float(sys.argv[1]),float(sys.argv[1]))
	else:
	    runStrobe(test)
    except:
	test.reset()
