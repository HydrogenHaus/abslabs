#!/usr/bin/env python

from time import time
from random import uniform
from threading import Thread

class metronome(Thread):

    def __init__(self, bpm, note=16, debug=False):
        self.bpm   = bpm
        self.note  = note
        self.step  = ((60*4)/float(self.bpm))/self.note
        self.debug = debug
        self.count = 0
        self.func  = lambda: None
        self.quit  = False
        Thread.__init__(self)

    def run(self):
        self.actual_time = self.true_time = 0
        self.error  = 0
        self.tfirst = self.tlast = tstart = told = time()
        tend        = tstart + self.step
        while not self.quit:
            self.func()
            if self.debug:
                s  = int(tend-told)
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
    bpm   = 87.5
    phase = 200
    song = '/home/honus/svn/abslabs/music/SuchGreatHeights.wav'

    import pygame
    pygame.mixer.init()
    s = pygame.mixer.Sound(song)

    from lightUtil import *
    from runFade import fade, fade_wrapper
    room = lights(12)
    all = group(room, range(room.number))

    introClrs =  [(255,255,0), (255,0,125), (125,0,255), (255,0,125), 
                  (0,0,255)  , (125,255,0), (125,255,0) ]

    verse1clrs = [(255,0,255), (255,125,0), (255,255,0), (255,255,0),
                  (0,255,0)  , (255,0,0),   (255,255,0), (255,255,0) ]

            
    one  = group( room, [1] )
    five = group( room, [5] )
    six  = group( room, [6] )
    seven = group(room, [7] )
    eight = group(room, [8] )
    nine  = group(room, [9] ) 
    ten   = group(room, [10])
    eleven= group(room, [11])


#    introSecondPart = 

    mid  = group( room, [2,3,4] )
    bricks = [ one, five, six, five, six, five, six, five ]
    
    mid.setColor( black )


    chorusClrs = [ red, yellow, green, blue, 
                   (255,255,0), (255,0,255), (0,255,255), 
                   (255,125,0), (255,125,0), #such
                   (0,255,255), (0,255,255), #great
                   (125,0,255), (125,0,255), #heights
                   (255,125,0), (255,125,0), #come
                   (0,125,255), (0,125,255), #down
                   (125,255,0), (125,255,0), (125,255,0), (125,255,0), #now
                   (125,255,0), (125,255,0),                           #(now)
                   (125,255,125), (125,255,125), #they'll
                   (0,125,255), (0,125,255), (0,125,255), (0,125,255), #say
                   (0,125,255), (0,125,255)                            #(say)
                   ]

    backWall = group( room, range(7, room.number) )
    backWall.setColor( black )


    #In the introduction, this is the melody
    #This is intended to be played on the back wall; if played on 
    #adjacent walls, it might be confusing to some. 
    oneBack    = (0,2,4,6, 16,18,20,22,
                  48,50,52,54, 64,66,68,70,
                  96,98,100,102, 112,114,116,118,
                  144,146,148,150, 160,162,164,166,
                  192,194,196,198, 208,210,212,214
                  )
    twoBack    = (32,34,36,38,40,42,44,46,
                  80,82,84,86,88,90,92,94,
                  128,130,132,134,136,138,140,142,
                  176,178,180,182,184,186,188,190,
                  224,226,228,230,232,234,236,238
                  )
    threeBack  = ()
    fourBack   = ( 450, 490 )
    fiveBack   = (  8,10,12,14, 24,26,28,30,
                    56,58,60,62, 72,74,76,78, 
                    104,106,108,110, 120,122,124,126,
                    152,154,156,158, 168,170,172,174,
                    200,202,204,206, 216,218,220,222
                  )
    sixBack    = (47,95,143,192)


    """
    They will see us co-ming from such great heights. Come down now, they'll say  
    1    1    1  1  1   1    1    2    2     2        2    2    6    2 
    """


    def intro():
        one.setColor( black )
        five.setColor( black )
        six.setColor( black )
        seven.setColor( black )
        eight.setColor( black )
        ten.setColor( black )
        eleven.setColor( black )
        bricks[ m.count%len(bricks) ].setColor( (0,255,255) )

        noteColor = (125,255,0)
        if( m.count in oneBack ):
            seven.setColor( noteColor )
        if( m.count in twoBack ):
            eight.setColor( noteColor )
        if( m.count in fourBack ):
            nine.setColor(  noteColor )
        if( m.count in fiveBack ):
            ten.setColor(   noteColor )
        if( m.count in sixBack ):
            eleven.setColor(noteColor ) 


        if( m.count ==  240 ):
            m.func = verse1
        if( m.count >= 128 ):
            if( m.count%16 == 0):
                Thread( target=playFade ).start()




    def verse1():
        all.setColor( verse1clrs[ m.count%len(verse1clrs) ])
        if( m.count == 494 ):
            m.func = chorus

    def chorus():
        one.setColor( black )
        five.setColor( black )
        six.setColor( black )
        bricks[ m.count%len(bricks) ].setColor( (0,255,255) )
        if( m.count%2 == 0 ):
            Thread( target=playFade2 ).start()
        if( m.count == 900 ):
            m.func = verse


    def flashGroup( grp, color, time ):
        grp.setColor( color )
        sleep(time)
        grp.setColor( black )

    def playFade():
        fade_wrapper( mid, introClrs[ (m.count-128)/16 ]%len(introClrs), .1, 50 )

    def playFade2():
        n =(m.count-494)/2
        if( n >= len(chorusClrs) ):
            n = n%len(chorusClrs)
        else:
            pass
        print str(m.count) + ' : ' + str( n ) + ' : ' 
        fade_wrapper( mid, chorusClrs[ n ], .1, 50  )



    m = metronome(bpm, note=16, debug=False)
    m.func = intro
    s.play()
    sleep(phase/1000.0)
    m.start()

    cmd = raw_input("")
    m.quit = True
    while m.isAlive():
        pass

    true_time = m.count * m.step
    actual_time = m.tlast - m.tfirst
    error = actual_time - true_time
    print "Total error was %.4f ms" %(error*1000.0)
    print "  percent error was %.6f%%" %((error/true_time)*100)
    print "  for a total time of %.2f s" %actual_time
    
    all.setColor( black )
    s.stop()
    sleep(1)
    fade_wrapper( all, (170,170,170), 3, 100 )
    while(1):
        sleep(99)

        

