#!/usr/bin/python

from lightUtil import *
from random import randint
from time import sleep

################################################################
## The lights move around the room in a snake fashion. 
## We choose a random color and we move it around the room. 
## 
## param1: speed of the snake around the room
##         range : { x : 0 < x <= 100 } where 0 is the slowest.
################################################################

def runSnake(inst, speed=100):

    snake = inst.number+3
    while True:
        R = randint(0,255)
        G = randint(0,255)
        B = randint(0,255)

        for light in range(0, snake):
            if (light-0 >= 0 and light-0 <= inst.number):
                inst.setLight( light, (R, G, B) )
            if (light-3 >= 0 and light-3 <= inst.number):
                inst.setLight( light-3, (0,0,0) )
            if (light-2 >= 0 and light-2 <= inst.number):
                inst.setLight( light-2, (int(.25*R), int(.25*G), int(.25*B)) )
            if (light-1 >= 0 and light-1 <= inst.number):
                inst.setLight( light-1, (int(.50*R), int(.50*G), int(.50*B)) )
            inst.update()
            sleep(10./speed)
            #print light


if __name__=="__main__":
    try:
        test = lights(4)
        if len(sys.argv) == 2:
            runSnake(test, float(sys.argv[1]))
        else:
            runSnake(test)
    except:
        test.reset()
