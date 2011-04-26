#!/usr/bin/python

from lightUtil import lights, powerSine
from time import sleep
import sys, math

def runPSine(inst,freq=100):
    """runPSine(   inst, freq(as-a-percent| default=100),   )"""
    time = 0
    speed = 100.
    if freq <= 0:
	freq = 100

    try:
        while True:
	    for light in range(0,48,6):
		phase_A = powerSine(time, 0, freq)
		phase_B = powerSine(time, math.pi, freq)
		inst.setLight(light+0,(phase_A, phase_B, 0))
		inst.setLight(light+1,(phase_B, phase_A, 0))
		inst.setLight(light+2,(0, phase_A, phase_B))
                inst.setLight(light+3,(0, phase_B, phase_A))
                inst.setLight(light+4,(phase_A, 0, phase_B))
                inst.setLight(light+5,(phase_B, 0, phase_A))
	    inst.update()
	    #print time, phase_A, phase_B
            sleep(1./speed)
            time += 1
    except:
        inst.reset()

if __name__=="__main__":
    if len(sys.argv) == 2:
	runPSine( lights(12), float(sys.argv[1]) )
    else:
	runPSine( lights(12))
