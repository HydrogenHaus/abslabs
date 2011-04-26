#!/usr/bin/python

from lightUtil import *  
from random    import randint 
from time      import *

import runFade
import pygame
import sys
import threading
import traceback
from runFadeTo import fadeTo

VOLUME = 100
MUSIC_FILE = "music/TimeToPretend.wav"


def getTime( timeZero ):
    return time() - timeZero

def printTime( timeZero ):
    print getTime( timeZero )

def showTimeToPretend( room, timeZero ):
    all = group(room, range(room.number) )
    waveColor = (0,255,255)
    sleep(1.2)

    for counter in range(6):
        runWaves(room, waveColor) 
    all.setColor( red )
    fadeTo( room, black,  60 )
    for counter in range(6):
        runWaves(room, waveColor)
    all.setColor( red )
    fadeTo( room, (0,0,0), 30)
    for counter in range(5):
        runWaves(room, waveColor)
    all.setColor( red )
    fadeTo( room, black, 35 )
    
    noteSpeed1 = .26
    sleep(.05)
    for guitar in range(5):
        flashColor( room, 1, green, noteSpeed1)
        flashColor( room, 6, green, noteSpeed1)
    flashColor( room, 1, green, noteSpeed1 )
    flashColor( room, 5, green, noteSpeed1 ) 
    flashColor( room, 1, green, noteSpeed1 ) 
    flashColor( room, 4, green, noteSpeed1 )
    flashColor( room, 1, green, noteSpeed1 )
    flashColor( room, 5, green, noteSpeed1 )
    for guitar in range(5):
        flashColor( room, 1, green, noteSpeed1 )
        flashColor( room, 6, green, noteSpeed1 )
    flashColor(room, 1, green,noteSpeed1 )
    flashColor( room, 5, green,noteSpeed1 )
    flashColor(room, 1, green,noteSpeed1 )
    flashColor(room, 4, green,noteSpeed1 )
    flashColor(room, 1, green,noteSpeed1 )
    flashColor( room, 5, green, noteSpeed1 )
    
    
def flashColor( room, lightNumber, color, time ):
    originalColor = room.state[lightNumber]
    room.setLight( lightNumber, color )
    room.update()
    sleep(time)
    room.setLight( lightNumber, originalColor )

def runWaves( inst, waveColor=(255,0,0), time=.05 ):
    startPos = inst.number/2
    forwardWave  = startPos
    backwardWave = startPos
    while ( backwardWave >= -2 ):
        if(backwardWave >= 0):
            inst.setLight( forwardWave,    waveColor )
            inst.setLight( backwardWave,   waveColor )
            if(backwardWave <= startPos-1):
                inst.setLight( forwardWave-1,  (waveColor[0]/2, waveColor[1]/2, waveColor[2]/2) )
                inst.setLight( backwardWave+1, (waveColor[0]/2, waveColor[1]/2, waveColor[2]/2) )
                if(backwardWave <= startPos-2):
                    inst.setLight( forwardWave-2,  (waveColor[0]/4, waveColor[1]/4, waveColor[2]/4) )
                    inst.setLight( backwardWave+2,  (waveColor[0]/4, waveColor[1]/4, waveColor[2]/4) )



        elif(backwardWave >= -1 and backwardWave < 0):
            inst.setLight( forwardWave-1, (waveColor[0]/2, waveColor[1]/2, waveColor[2]/2) )
            inst.setLight( backwardWave+1,(waveColor[0]/2, waveColor[1]/2, waveColor[2]/2) )
            inst.setLight( forwardWave-2, (waveColor[0]/4, waveColor[1]/4, waveColor[2]/4) )
            inst.setLight( backwardWave+2, (waveColor[0]/4, waveColor[1]/4, waveColor[2]/4) )


        elif( backwardWave ==-2 ):
            inst.setLight( forwardWave-2,  (waveColor[0]/4, waveColor[1]/4, waveColor[2]/4) )
            inst.setLight( backwardWave+2,  (waveColor[0]/4, waveColor[1]/4, waveColor[2]/4) )


        inst.update()
        forwardWave  += 1
        backwardWave -= 1
        sleep(time)




if __name__=="__main__": 
    if len(sys.argv)==2: 
        VOLUME = int(sys.argv[1])
    pygame.mixer.init()
    song = pygame.mixer.Sound( MUSIC_FILE )
    song.set_volume( VOLUME/100.0 )
    song.play()
    timeZero = time()

    
    try:
        test = lights(7)
        if len(sys.argv) == 4:
            showTimeToPretend( test, (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])), timeZero )

        else:
            showTimeToPretend( test, timeZero )
    except:
        test.reset()

