#!/usr/bin/python

from lightUtil import *  
from random import randint 
from time import sleep 

def runBars(inst, speed=.2):

    while True:
        roomColor = ( randint(0,255), randint(0,255), randint(0,255) )
        for i in range(0,6,2):
            j = i + 6
            currentColor = (randint(0,255), randint(0,255), randint(0,255))
            inst.setLight( i, currentColor )
            inst.setLight( j, currentColor )
            inst.setLight( i+1, currentColor )
            inst.setLight( j+1, currentColor )


            sleep(speed)
            inst.update()
            inst.setLight( i, roomColor )
            inst.setLight( i+1, roomColor )
            inst.setLight( j, roomColor )
            inst.setLight( j+1, roomColor) 

if __name__=="__main__":
    if len(sys.argv) == 2:
        runBars(lights(12), float(sys.argv[1]))
    else:
        runBars(lights(12), .2)
