#!/usr/bin/python

from lightUtil import lights, powerSine
from random import randint
from time import sleep
import sys, math

def sineRand(inst,freq=100):
    """sineRand(   inst, freq   )"""
    time = 0
    speed = 100.
    if freq <= 0:
	freq = 100

    while True:
	cycle = 1
	color_R = randint(0,255)
	color_G = randint(0,255)
	color_B = randint(0,255)
	while cycle:
	    scale = powerSine(time, 0, freq)/255.
	    color = (int(color_R*scale), int(color_G*scale), int(color_B*scale))
	    for light in range(0,inst.number,3):
		inst.setLight(light+0,color)
		inst.setLight(light+1,color)
	        inst.setLight(light+2,color)
	    inst.update()
	    #print time, color_R, color_G, color_B
	    sleep(1./speed)
	    cycle = scale
	    time += 1

if __name__=="__main__":
    try:
	test = lights(36)
	if len(sys.argv) == 2:
	    sineRand(test,float(sys.argv[1]))
	else:
	    sineRand(test)
    except:
        test.reset()
