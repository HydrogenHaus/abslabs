#!/usr/bin/env python


from time import sleep
from numpy import array as narray
from threading import Thread
from lightUtil import *


def fade( from_color, to_color, steps ):
    from_color = narray(from_color)
    to_color = narray(to_color)
    diff = (to_color-from_color)/float(steps)
    for n in range(steps):
        color = from_color + n*diff
        yield color.round().astype(int).tolist()


def fade_wrapper( grp, to_color, time, steps=100 ):
    from_color = grp.color
    for c in fade(from_color, to_color, steps):
        grp.setColor(c)
        sleep(float(time)/steps)


if __name__ == "__main__":
    
    from time import sleep
    import sys
    
    if len(sys.argv)==3:
        time = float(sys.argv[1])
        steps = int(sys.argv[2])
    else:
        time = 10.0
        steps = 1000

    room = lights(7)
    all = group(room,range(7))
    
    for c in fade(cyan,orange,steps):
        all.setColor(c)
        room.update()
        sleep(time/steps)
