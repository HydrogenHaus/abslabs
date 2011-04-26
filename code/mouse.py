#!/usr/bin/env python

import struct
import curses
import lightUtil
import numpy
import time

def main(scr):
    room = lightUtil.lights(50)
    all = lightUtil.group(room,range(50))
    mstream = open('/Users/blakerego/Desktop/vlc-output.raw', 'rb')
    
    clr = numpy.array([127,127,127])
    
    while True:
        scr.erase()
        a,b,c = numpy.array(struct.unpack('bbb',mstream.read(3)))
        #a=int( a%255 )
        #b=int( b%255 )
        #c=int( c%255 )
        a=int( a )
        b=int(b)
        c=int(c)
        
        scr.addstr(1,1,str((a,b,c)))
        pos = numpy.array((a, b, c))
        nclr = clr+pos
        scr.addstr(2,1,str(nclr))
        all.setColor(tuple(nclr))
        room.update()
        scr.refresh()
 

    """
    scr.erase()
    a,b,c = numpy.array(struct.unpack('bbb',mstream.read(3)))
    a,b,c = numpy.array(struct.unpack('bbb',mstream.read(3)))

    a,b,c = numpy.array(struct.unpack('bbb',mstream.read(3)))
    a,b,c = numpy.array(struct.unpack('bbb',mstream.read(3)))

    #a=a%130                                                                              
    #b=b%130                                                                              
    #c=c%130                                                                              

    scr.addstr(1,1,str((a,b,c)))
    pos = numpy.array((a, b, c))
    nclr = clr+pos
    scr.addstr(2,1,str(nclr))
    all.setColor(tuple(nclr))                                                            
    room.update()
    scr.refresh()
    """

if __name__=='__main__':
    curses.wrapper(main)
