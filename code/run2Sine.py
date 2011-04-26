#!/usr/bin/python

from lightUtil import lights, powerSine
from time import sleep
import sys, math

def run2Sine(inst,freq=100,color_a=(255,0,0),color_b=(0,255,0)):
    """run2Sine(   inst, freq(as-a-percent| default=100), color1, color2   )"""
    time = 0
    speed = 100.
    if freq <= 0:
	freq = 100

    while True:
	for index in range(0,2):
	    cycle = 1
	    while cycle:
		scale_a = float(powerSine(time, 0, freq)/255.)
		scale_b = 1. - scale_b
                color_A = (int(scale_a*color_a[0]),int(scale_a*color_a[1]),int(scale_a*color_a[2]))
		color_B = (int(scale_b*color_b[0]),int(scale_b*color_b[1]),int(scale_b*color_b[2]))
                for light in range(0,inst.number,2):
		    inst.setLight(light+index+0,color_A)
		    inst.setLight(light+index+1,color_B)
		inst.update()
		#print time, color_A, color_B
		sleep(1./speed)
		cycle = color_A
		time += 1

if __name__=="__main__":
    try:
	test = lights(13)
	if len(sys.argv) == 2:
	    run2Sine(test,float(sys.argv[1]) )
	elif len(sys.argv) == 4:
	    run2Sine(test,sys.argv[1],sys.argv[2],sys.argv[3])
	else:
	    run2Sine(test)
    except:
	test.reset()
