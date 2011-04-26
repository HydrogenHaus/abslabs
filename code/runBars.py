#!/usr/bin/python

from lightUtil import *  
from random import randint 
from time import sleep 

####################################################################
##
## This function will create bars around the room. It is similar to 
## snake, except the previous color remains, rather than returning to 
## black. 
##
##
## param1: speed for bars going around room
##         range of values  { x : 0 < x <= 100 } where 0 is slow
##
## param2: number of lights in the system. 
####################################################################
def runBars(inst, speed=.2, numLights=4):
    while True:
	barColor  = ( randint(0,255), randint(0,255), randint(0,255) )
        roomColor = ( randint(0,255), randint(0,255), randint(0,255) )
        #roomColor = barColor
        for i in range(0,numLights):
            j = i + numLights+1

            inst.setLight( i, barColor )
            inst.setLight( j, barColor )
            sleep(speed)

            inst.update()
            inst.setLight( i, roomColor )
            inst.setLight( j, roomColor )

if __name__=="__main__":
    try:
	test = lights(4)
	if len(sys.argv) == 2:
            runBars(test, float(sys.argv[1])/100)
	else:
            runBars(test)
    except:
        print "error running script"
    
