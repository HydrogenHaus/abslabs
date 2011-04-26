#!/usr/bin/env python

from time      import sleep
from pyplayer  import track
from runFadeTo import fadeTo
from threading import Thread
from metronome import metronome

class songKnockEmOut():
    def __init__(self, inst): 
        self.all    = group( inst, range(0,inst.number) )
        self.inst   = inst
        self.file   = '/home/honus/svn/abslabs/music/KnockEmOut.wav'
        self.bpm    = 128.0 # was 102.4
        self.offset = 0
        self.beat   = 0
        self.count  = 0
        self.end    = 1456
        self.dict = {64: self.drums, 128: self.bridge, 256: self.verse1, 
                     386: self.verse2, 448: self.chorus, 576: self.red, 
                     640: self.verse3, 768: self.verse4, 832: self.chorus, 
                     960: self.verse5, 1088: self.chorus, 1216: self.chorus,
                     1344: self.outro }
    def red(self):
        self.all.setColor( (255,0,0) )
    def grn(self):
        self.all.setColor( (0,255,0) )
    def intro(self):
        self.all.setColor( (128,0,128) )
    def drums(self):
        every = 16
        print "Beat is:", self.beat
        if( self.beat == 0 ):
            for light in self.inst.state:
                self.inst.setLight(light, (128,0,0) )
        if( self.beat%every == 0 ):
            for light in [1]:
                self.inst.setLight(light, (128,0,128) )
        elif( self.beat%every == 2 ):
            for light in [2]:
                self.inst.setLight(light, (128,0,128) )
        elif( self.beat%every == 8 ):
            for light in [5,6]:
                self.inst.setLight(light, (128,0,128) )
        elif( self.beat%every == 12 ):
            for light in self.inst.state:
                self.inst.setLight(light, (128,0,0) )
        else:
            pass
        self.inst.update()
    def bridge(self):
        self.all.setColor( (128,128,0) )
    def verse1(self):
        self.all.setColor( (128,0,0) )
    def verse2(self):
        self.all.setColor( (0,128,0) )
    def verse3(self):
        self.all.setColor( (0,0,128) )
    def verse4(self):
        self.all.setColor( (0,128,0) )
    def verse5(self):
        self.all.setColor( (128,0,0) )
    def chorus(self):
        self.beat = (self.beat-self.count)%13
        self.all.setColor( (128,128,128) )
    def outro(self):
        pass

def lightShow(inst, song, metr, trac):
    metr.func = song.intro
    trac.start()
    sleep(song.offset/1000.)
    metr.start()
    while metr.quit is False:
        if( metr.count == song.end ):
            metr.quit = True
            inst.reset()
        else:
            for key, value in song.dict.iteritems():
                if( metr.count == int(key) ):
                    metr.func = value
                    song.count = int(key)
                    song.beat = metr.count - int(key)
                    sleep(.125)
                    break
                else:
                    pass
        song.beat = metr.count - song.count
    while metr.isAlive():
        pass
    trac.stop()


"""
Knock 'Em Out Lyrics
[Intro]   {Piano and Horns}
[Bridge]
   Alright so this is a song about, anyone, it could be anyone
   You're just doing your own thing and some one comes out the blue
   They're like
   Alright, what ya sayin
   Yeah can I take your digits?
   And you're like, no not in a million years, you're nasty
   please leave me alone
[Verse]
   Cut to the pub on a lads night out
   Man at the bar cos it was his shout
   Clocks this bird and she looks OK
   She caught him looking and walked his way
   Alright darling, you gonna buy us a drink then?
   Err no, but I was thinking about buying one for your friend
[Verse]
   She's got no taste hand on his waist, 
   Tries to pull away but her lips on his face
   If you insist I'll have a white wine spritzer
   Sorry love, but you ain't a pretty picture
[Chorus]
   Can't knock em out, can't walk away
   Try desperately to think of the politest way to say
   Just get out my face, just leave me alone
   And no you can't have my number
   Because I've lost my phone
[Bridge]
   Oh yeah, actually yeah I'm pregnant,
   having a baby in like 6 months 
   so no, yeah, yeah
[Verse]
   I recognise this guy's way of thinking
   As he walks over her face starts sinking
   She's like oh here we go
   It's a routine check that she already knows
   She's thinking they're all the same
   Yeah you alright baby? You look alright still, yeah what's your name?
[Verse]
   She looks in her bag, takes out a fag
   tries to get away from the guy on a blag
   can't find a light
   Here use mine
   You see the thing is I just don't have the time
[Chorus]
[Verse]
   Go away now, let me go
   Are you stupid? Or just a little slow?
   Go away now I've made myself clear
   Nah it's not gonna happen
   Not in a million years
[Chorus x2]
[Outro]
   Nah I've gotta go, my house is on fire
   I've got herpes, err no I've got syphilis
"""


if __name__ == "__main__":
    try:
        from lightUtil import *
        room = lights(12)
        song = songKnockEmOut(room)
        m = metronome(song.bpm, note=16, debug=False)
        t = track(song.file)
        lightShow(room, song, m, t)
    except KeyboardInterrupt:
        print m.count
        m.quit = True
        while m.isAlive():
            pass
        t.stop()
        sleep(.5)
        fadeTo(room, (32,32,32), 25 )
#        while True:
#            sleep(10)

