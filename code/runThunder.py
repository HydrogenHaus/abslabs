#!/usr/bin/python
from __future__ import with_statement
from lightUtil import *  
from random import randint 
from time import sleep 
import pygame
import os
import threading
import traceback


#THUNDER_FILE = "soundlib/lightning.wav"
#RAIN_FILE    = "soundlib/heavyrainloop.wav"
RAIN_FILE    = "soundlib/thunder.wav"
THUNDER_FILE = RAIN_FILE
#WIND_FILE    = "soundlib/wind2.wav"



def play_lightning():
    thunder.play()

def play_rain():
    rain.play(-1)

def getLightning(inst, lightNumber, thunderTime=.1): 
    choice = randint(1,100)
    if( choice > 0 and choice <= 1): 
        for int in range(0, randint(3, 7) ):
            inst.setLight(lightNumber, white)
            inst.update()
            sleep( thunderTime)
            inst.setLight(lightNumber, black) 
            inst.update()
            sleep( thunderTime)     
        return white
    elif (choice > 1 and choice <= 60): 
        return (50, 50, 255)
    elif (choice > 60 and choice <= 100):
        if choice == 75: 
            if randint(0,4) == 1:
                wind.play()
        return (80, 80, 255)
    
def runThunder( inst, rainTime=.1, thunderTime=.1, lightningTime=1):
    while True:
        ifLightning = getLightning(inst, randint(0,inst.number), thunderTime)
        for i in range(0,inst.number):
            inst.setLight( i, ifLightning )
        inst.update()
        sleep( rainTime )
        if( ifLightning == white ): 
            #threading.Thread(target=play_lightning).start()
            thunder.play()
            sleep( lightningTime )
            
if __name__=="__main__":
    pygame.mixer.init()
    #thunder = pygame.mixer.Sound( THUNDER_FILE )
    rain    = pygame.mixer.Sound( RAIN_FILE )
    #wind   = pygame.mixer.Sound( WIND_FILE )

    rain.set_volume(.2)
    #wind.set_volume(.3)

#        threading.Thread(target=play_rain).start()
    rain.play(-1)
    
    with lights(7) as test:
        if len(sys.argv) == 4:
            runThunder(test, float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
            pygame.mixer.fadeout
        else:
            runThunder(test)
    
