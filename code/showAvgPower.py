#!/usr/bin/env python

import sys
from time      import time
from pyplayer  import track
from lightUtil import *

MAX_POWER = 10000000000000.
THRESHOLD = MAX_POWER / 3.

if __name__ == "__main__":
    try:
        inst = lights(24)
        if len(sys.argv) == 2:
            t = track( str(sys.argv[1]) )
        elif len(sys.argv) == 3:
            t = track( str(sys.argv[1]) )
            MAX_POWER = MAX_POWER * ( float(sys.argv[2])/100. )
        else:
            #Default track must be Radiohead.
            t = track( "/home/honus/svn/abslabs/music/ParanoidAndroid.wav" )
        t.start()
        while not t.done:
            """
            The following few lines attempt to detect the beat. Here we 
            average all the bands from the FFT spectrum. If this value
            is above the threshold, we switch the blue to 255. If not, 
            blue is zero. 
            """
            sum = 0
            for band in range(0, inst.number): 
                sum = sum+ t.power[band]
            average = sum / inst.number
            for light in range(0, inst.number):
                if ( average >= light * MAX_POWER / inst.number ):
                    if ( average >= THRESHOLD ):
                        if( average >= MAX_POWER):
                            color = red
                        else: 
                            color = (255, 0, 255) 
                    else: 
                        color = ( 255, 255, 0)
                    inst.setLight( light, color )
                else: 
                    inst.setLight( light, black ) 
#                print light, color, t.power[light]
            inst.update()
            sleep(.001)
            #updates once a millisecond 
        t.stop
        for light in range(0, inst.number):
            inst.setLight( light, black )
        sys.exit()
    except KeyboardInterrupt:
        t.stop()
        sys.exit()
