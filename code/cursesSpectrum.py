#!/usr/bin/env python


import sys
import curses
import threading
from numpy import log10, inf
from time import sleep
from pyplayer import track


class SpectrumTracker(threading.Thread):
    
    def __init__(self, track, mainwin, wins):
        self.track = track
        self.mainwin = mainwin
        self.wins = wins
        self.quit = False
        threading.Thread.__init__(self)

    def run(self):
        while not self.quit:
            for f in range(len(self.wins)):
                self.wins[f].erase()
                #temp = log10(self.track.power[f])
                #if temp == inf:
                #    temp = MAXX
                #elif temp == -inf:
                #    temp = 0
                #bar = '#'*int(10*temp)
                bar = '#' * int(self.track.power[f]/float(5 * 10**10))
                if len(bar) > MAXX-30:
                    bar = '#'*(MAXX-20)
                self.wins[f].addstr(0,0,'%3i '%f + bar + '-'*(MAXX-len(bar)-10))
                self.wins[f].refresh()
            #self.mainwin.refresh()
            sleep(.001)

    def stop(self):
        self.quit = True
        while self.isAlive():
            pass
        


def main(stdscr):

    t = track(sys.argv[1])
    t.start()

    global MAXY, MAXX
    mainwin = curses.newwin(0,0)
    MAXY, MAXX = mainwin.getmaxyx()

    spec_wins = []
    for f in range(len(t.power)):
        spec_wins.append(mainwin.subwin(1,MAXX,f+5,0))

    s = SpectrumTracker(t,mainwin,spec_wins)
    s.start()

    while True:
        cmd = mainwin.getkey()
        if cmd == 'q':
            t.stop()
            s.stop()
            return
        elif cmd == 'p':
            if t.paus:
                t.unpause()
            else:
                t.pause()
        elif cmd == 'r':
            t.skip(0.0)


curses.wrapper(main)
