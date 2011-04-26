#!/usr/bin/python

from lightUtil import lights, powerSine
from time import sleep
import sys, math

def run3Snake(inst,freq=100):
    """run3Snake(   inst, freq(as-a-percent|default=100),   )"""
    time = 0
    speed = 100.
    if freq <= 0:
	freq = 100

    while True:
	for index in range(0,3):
	    cycle = 1
	    while cycle:
		scale   = powerSine(time, 0, freq)
		color_A = (scale, 0, 0)
                color_B = (0, scale, 0)
                color_C = (0, 0, scale)
                color   = (color_A, color_B , color_C)
		for light in range(0,inst.number,3):
		    inst.setLight(light+0,color[(index+0)%3])
		    inst.setLight(light+1,color[(index+1)%3])
	            inst.setLight(light+2,color[(index+2)%3])
		inst.update()
		ind0 = (index+0)%3
		ind1 = (index+1)%3
		ind2 = (index+2)%3
		#print time, scale
		sleep(1./speed)
		cycle = scale
		time += 1
	    time += 2

if __name__=="__main__":
    try:
	test = lights(13)
	if len(sys.argv) == 2:
	    run3Snake(test,float(sys.argv[1]) )
	else:
	    run3Snake(test)
    except:
	test.reset()
