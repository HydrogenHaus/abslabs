"""
***********************************************************************************************
Kyle Arthur Rego
fadeOut.py
This function uses the lightUtil library to fade continuously between the red, green and blue. 
***********************************************************************************************
"""

#!/usr/bin/python

from lightUtil import lights
from time import sleep
import sys

def fadeOut(inst,speed=100., n=1):
    """fadeOut(   inst,   speed(as-a-percent|default=100)   )"""
    if speed <= 0.:
	speed = 100.
    if n >= 100.:
	n = 100

    try:
        color_R = n*int(255/n)
        color_G = 0
        color_B = 0
        while True: 
	    for j in range(0, 6, 1):
	    	for i in range(0, int(255/n), 1):
		    if j == 0:
	                color_G = color_G + n
		    elif j == 1:
	                color_R = color_R - n
		    elif j == 2:
	                color_B = color_B + n
		    elif j == 3:
	                color_G = color_G - n
	            elif j == 4:
			color_R = color_R + n
		    elif j == 5:
	                color_B = color_B - n
	            for light in inst.state:
			inst.setLight(light,(color_R, color_G, color_B))
	            inst.update()
		    #print color_R, color_G, color_B
	            sleep(100./speed/255.)
		j = j + 1
		j = j%6

    except:
        inst.reset()

if __name__=="__main__":
    test = lights(24)
    if len(sys.argv) == 2:
	fadeOut(test,float(sys.argv[1]))
    elif len(sys.argv) == 3:
        fadeOut(test,float(sys.argv[1]),int(sys.argv[2]))
    else:
	fadeOut(test)
