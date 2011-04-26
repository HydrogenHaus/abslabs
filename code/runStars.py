#!/usr/bin/python

from lightUtil import lights, powerSine
from random import randint
from time import sleep
import sys

def runStars( inst, freq=100, color=(255,0,0), speed=100. ):
    """runSine(inst, freq, color)"""
    time = 0
    trigger1 = -1
    trigger2 = -1
    if freq <= 0:
	freq = 100

    while True:
	scale = powerSine(time, 0, freq)
        scale2 = powerSine(time, 360, freq)
        currentColor = ( int(scale*color[0]), int(scale*color[1]), int(scale*color[2]) )
        currentColor2 = ( int(scale2*color[0]), int(scale2*color[1]), int(scale2*color[2]) )
        for light in inst.state:
            if light%2 == 0:
                inst.setLight(light, currentColor)
            else:
                inst.setLight(light, currentColor2)
        inst.update()
        sleep(1./speed)
	if( scale == 1 and trigger2 == 1):
	    trigger1 = 1
	    trigger2 = 0
	elif( scale == 0):
	    trigger2 = 1
        if( trigger1 == 1 and trigger2 == 1):
            break
	time +=1


if __name__=="__main__":
    try:
	test = lights(4)
	if( len(sys.argv) == 2):
	    while True:
		runStars( test, float(sys.argv[1]), (randint(0,255), randint(0,255), randint(0,255)) )
	elif( len(sys.argv) == 4):
	    while True:
		runStars( test, 100., (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])) )
	elif( len(sys.argv) == 5):
	    while True:
		runStars( test, float(sys.argv[1]), (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])) )
	else:
	    while True:
		runStars( test, 25, (80,80,100) )
    except:
	test.reset()
