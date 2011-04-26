#!/usr/bin/python

from lightUtil import *  
from random import randint 
from time import sleep 
import sys

import pygame

VOLUME = 100
FIRE_FILE = "soundlib/fire.wav"


def getFireColor( boundRed, boundOrange): 
    choice = randint(0,100)
    if  ( choice >= 0 and choice <= boundRed): 
        return (255,  0, 0) # red
    elif( choice > boundRed and choice <= boundOrange):
        return (255, 55, 0) # orange
    elif( choice > boundOrange and choice <=100): 
        return (255, 60, 0) # yellow

    
def runFire( inst, perRed=20, perOrange=50, perYellow=30, time=.01): # yellow is intentionally over-defined
    if (perRed + perOrange + perYellow != 100):
        print "Your percentages for red, orange and yellow don't add up."
        raise Exception
    else:
        boundRed    = perRed
        boundOrange = perRed + perOrange
        
    while True:     
        for i in range(0,inst.number):
            if( randint(0,inst.number) == i):
                inst.setLight( i, getFireColor(boundRed, boundOrange) )
        sleep( time )
        inst.update()


if __name__=="__main__":
    import sys
    if len(sys.argv)==2: 
        VOLUME = int(sys.argv[1])
    pygame.mixer.init()
    fire = pygame.mixer.Sound( FIRE_FILE )
    fire.set_volume(VOLUME/100.0)
    fire.play(-1)
    try:
        test = lights(7)
        if len(sys.argv) == 4:
            runFire( test, int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) )
        else:
            runFire( test)
    except:
        test.reset()
