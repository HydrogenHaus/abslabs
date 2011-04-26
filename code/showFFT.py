#!/usr/bin/env python

import sys
from time      import time
from pyplayer  import track
from lightUtil import *

MAX_POWER = 10000000000000.
THRESHOLD = MAX_POWER / 3.

def powerToColor(p):

    """ 
    takes a number and returns a color (tuple)
    This function works by picking a color temperature between
    green and red. The lower bound is completely off and the 
    upper bound is completely red. Everything in between is a 
    combination between green and red using a linear a few 
    linear functions. Green goes from 0 to 255 as the power
    goes from 0 to half. It then goes from full to 0 as the 
    power goes from half to full. Red goes from 0 to 255 as 
    the power goes from half to full. Blue is not used.
    We will use blue later in a simple attempt at beat 
    detection. 
    """
 
    lowerBound = 0 
    upperBound = MAX_POWER 
    N = MAX_POWER / 2.          #Piece-wise function switch point

    if p > MAX_POWER:
        E = 1.
    else:
        E = p / MAX_POWER       #Non-dimensionalized power

    if( p <= N):
        red   = 0
        blue  = 0
        green = int( 255*2*E )
    elif( p > N and p <= MAX_POWER ):
        red   = int( 255*(2*E-1) )
        blue  = 0
        green = int( 255*(2-2*E) )
    else:               
        red   = 0               # Error case. Should not get here 
        green = 0               # if MAX_POWER is set correctly. 
        blue  = 0               # Also checks to see if input p is negative.

    return (red, green, blue)

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
            t = track( "../wav/ParanoidAndroid.wav" )
        
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
                color = powerToColor( t.power[light] )
                if (average >= THRESHOLD ):
                    color = ( color[0], color[1], 255)

                inst.setLight( light, color )                
#                print light, color, t.power[light]
            inst.update()
            sleep(.125)
            #updates once a millisecond 
        t.stop
        for light in range(0, inst.number):
            inst.setLight( light, black )
        sys.exit()
    except KeyboardInterrupt:
        t.stop()
        sys.exit()
