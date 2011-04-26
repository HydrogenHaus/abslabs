#!/usr/bin/env python

import curses
import curses.panel
from lightUtil import *


#if __name__=="__main__":
def main(scr): 
    room = lights(12)
    g1 = group( room, [7,8,9] )
    g2 = group( room, [10,11,0] )
    g3 = group( room, [1,2,3] )
    g4 = group( room, [4,5,6] )
    all = group( room, range( room.number ) )
    stdscr = curses.initscr()

    colorRange = (red, green, blue)
    while True:
        all.setColor( black )
        scr=curses.initscr()

        c = scr.getkey()
        #c = stdscr.getch()

        if c == 'z':
           g1.setColor( colorRange[0] )
           sleep(.1)
        if c == 'a':
            g1.setColor( colorRange[1] )
            sleep(.1)

        if c == 'q':
            g1.setColor( colorRange[2] )
            sleep(.1)
        if c == 'x':
            g2.setColor( colorRange[0] )
            sleep(.1)
       
        if c == 's':
            g2.setColor( colorRange[1] )
            sleep(.1)

        if c =='w':
            g2.setColor( colorRange[2] )
            sleep(.1)

        if c =='c':
            g3.setColor( colorRange[0] )
            sleep(.1)
        if c =='d':
            g3.setColor( colorRange[1] )
            sleep(.1)

        if c =='e':
            g3.setColor( colorRange[2] )
            sleep(.1)

        if c=='v': 
            g4.setColor( colorRange[0] )
            sleep(.1)

        if c=='f':
            g4.setColor( colorRange[1] )
            sleep(.1)

        if c=='r': 
            g4.setColor( colorRange[2] ) 
            sleep(.1)


if __name__=="__main__":
    curses.wrapper(main)
