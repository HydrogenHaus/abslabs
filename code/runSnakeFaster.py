#!/usr/bin/python

from lightUtil import *  
from random import randint 
from time import sleep 

def runSnake(inst, time=3):

    while True:
        for i in range(0,12):
            inst.setLight( i, (randint(0,255), randint(0,255), randint(0,255)) )
            multiplier = ( 1/ (1+i) )
            sleep(time * multiplier )
            inst.update()
            inst.setLight( i, (0, 0, 0))
            

if __name__=="__main__":
    if len(sys.argv) == 2: 
        runSnake(lights(13), float(sys.argv[1]))
    else:
        runSnake(lights(13))
