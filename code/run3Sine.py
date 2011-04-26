#!/usr/bin/python

from lightUtil import lights, powerSine
from time import sleep
import sys, math

def run3Sine(inst, freq=100, color_a=(255,0,0), color_b=(0,255,0), color_c=(0,0,255)):
    """run3Sine(   inst, freq, color1, color2, color3   )"""
    time = 0
    speed = 100.
    if freq <= 0:
	freq = 100

    while True:
	cycle = 1
	while cycle:
	    scale = powerSine(time, 0, freq)/255.
            color_A = (int(scale*color_a[0]), int(scale*color_a[1]), int(scale*color_a[2]))
            color_B = (int(scale*color_b[0]), int(scale*color_b[1]), int(scale*color_b[2]))
            color_C = (int(scale*color_c[0]), int(scale*color_c[1]), int(scale*color_c[2]))
	    for light in range(0,inst.number,3):
		inst.setLight(light+0,color_A)
		inst.setLight(light+1,color_B)
	        inst.setLight(light+2,color_C)
	    inst.update()
	    #print time, color_A, color_B, color_C
	    sleep(1./speed)
	    cycle = scale
	    time += 1

if __name__=="__main__":
    try:
	test = lights(13)
	if len(sys.argv) == 2:
	    run3Sine(test,float(sys.argv[1]))
#       elif len(sys.argv) == 5:
#           run3Sine(test,float(sys.argv[1]),color1,color2,color3)
	else:
	    run3Sine(test)
