#!/usr/bin/env python


from time import time
from random import uniform
from threading import Thread


class metronome(Thread):

    def __init__(self, bpm, note=16, debug=False):
        self.bpm = bpm
        self.note = note
        self.step = ((60*4)/float(self.bpm))/self.note
        self.debug = debug
        self.count = 0
        self.func = lambda: None
        self.quit = False
	self.pause = False
        Thread.__init__(self)

    def run(self):
        self.actual_time = self.true_time = 0
        self.error = 0
        self.tfirst = self.tlast = tstart = told = time()
        tend = tstart + self.step
        while not self.quit:
		while not self.pause:
            	self.func()
            	if self.debug:
                	s = int(tend-told)
                	ms = int( ((tend-told)-s)*1000.0 )
                	us = (tend-told-s-ms/1000.0)*1000000.0
                	print "%5i/%5i: %3i sec, %3i ms, %.2f microsec with last error %.2f us"\
                    		%(self.count%16,self.count,s,ms,us,self.error*1000000.0)
            	if self.count:
                	self.actual_time = self.tlast - self.tfirst
                	self.true_time = self.count * self.step
                	self.error = self.actual_time - self.true_time
            	self.count += 1
            	while time()-tstart <= self.step-self.error:
                	tend = time()
            	told = tstart
            	self.tlast = tend
            	tstart = time()


if __name__ == "__main__":

    import sys
    bpm = float(sys.argv[1])
    phase = float(sys.argv[2])
    song = sys.argv[3]

    import pygame
    pygame.mixer.init()
    s = pygame.mixer.Sound(song)

    from lightUtil import *
    l = lights(7)
    all = group(l,range(7))

    clrs = [red,orange,black,black,red,orange,black,black]
    def alternate():
        all.setColor(clrs[m.count%len(clrs)])

    m = metronome(bpm, note=16, debug=False)
    m.func = alternate
    s.play(-1)
    sleep(phase/1000.0)
    m.start()

    raw_input("<enter> to pause")
    m.pause = True
    
    raw_input("<enter> to restart")
    m.pause = False

    raw_input("<enter> to quit")
    m.quit = True
    while m.isAlive():
        pass

    true_time = m.count * m.step
    actual_time = m.tlast - m.tfirst
    error = actual_time - true_time
    print "Total error was %.4f ms" %(error*1000.0)
    print "  percent error was %.6f%%" %((error/true_time)*100)
    print "  for a total time of %.2f s" %actual_time
