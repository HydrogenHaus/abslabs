#! /usr/bin/env python

import os
import sys
import string
import curses
import curses.panel
from showAny   import *
from lightUtil import *
from runSine   import runSine

global HOME, EXTS, PNCT
HOME = "/home/honus/music/"
EXTS = ('flac', 'mp3', 'wav')
PNCT = ('.', '_', '#')


##
##   Error Handling
##
#########################

class HostError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

class QuitError(Exception):
    def __init__(self, msg):
	self.msg = msg
    def __str__(self):
        return repr(self.msg)

class PaneError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)


##
##   Panels Class
##
#########################

class panels():
    def __init__(self,
		 ypos= 5,
		 xpos= 5,
		 rows= 10,
		 cols= 20,
                 padLines= 100,
		 title="Your Title"):

	self.xpos = int(xpos)
	self.ypos = int(ypos)
	self.rows = int(rows)
	self.cols = int(cols)
        self.padLines = padLines
	self.title = title
        if rows < 1:
            raise PaneError("Pane must have at least one row.")
        if len(title) > (cols-5):
            raise PaneError("Title will not fit.")
        self.pad = curses.newpad(self.padLines, self.cols)
	self.fields = None
        self.outside = curses.newwin(self.rows+4,self.cols+4,self.ypos+1,self.xpos+2)
        self.outside.border()
        self.body = curses.newwin(self.rows+2,self.cols+4,self.ypos+2,self.xpos)
	self.body.border(0,0,' ',0,0,0,0,0)
	self.head = curses.newwin(3,self.cols+4,self.ypos,self.xpos)
	self.head.box()
	self.head.addnstr(1,(self.cols+2-len(self.title)),self.title,self.cols-5)
        self.ready()

    def ready(self):
        self.outside.refresh()
	self.body.refresh()
	self.head.refresh()
        stdscr.move(scrmaxy-1, 0)
        stdscr.clrtoeol()


    ##
    ##   Free Methods
    ##
    #########################

def printErr( msg ):
    stdscr.addstr(scrmaxy-1,0, str(msg) )
    stdscr.clrtoeol()
    stdscr.refresh()
    sleep(1)


    ##
    ##   Music Management
    ##
    #########################

class music():
    def __init__( self ):
        self.cursor = 1
        self.startLine = 1
        self.padLength = None
        self.wave = None
        self.show = None

    def loadLbry( self, pane=None ):
        artistList = os.listdir(HOME)
        artistList.sort()
        if pane is not None:
            self.panel = pane
        else:
            self.artistPane = panels( 0,1, 30,40, len(artistList), title="Artists" )
            self.artistPane.fields = artistList[:]
            self.panel = self.artistPane
        printErr("artists sux.")
        self.artists()
        """
        albumList = os.listdir(self.currDir)
        # later: strip the none ablum files here
        albumList.sort()
        self.albumPane = panels( 8,50, 5,39, len(albumList), title="Albums" )
        self.albumPane.fields = albumList[:]
        self.panel = self.albumPane
        self.currDir = self.albums()
        songList = os.listdir(self.currDir)
        for line in songList:
            if line[0] not in PNCT:
                songList.append(line)
        songList.sort()
        self.songPane = panels( 18,50, 12,39, len(songList), title="Songs" )
        self.songPane.fields = songList[:]
        self.panel = self.songPane
        self.songs()
        """

    def artists(self):
        count = 1
        for artist in self.panel.fields:
            line = artist + (self.panel.cols - len(artist)) * ' '
            if count == self.cursor:
                self.panel.pad.addnstr(count,0, line, self.panel.cols, curses.A_STANDOUT)
            else:
                if count in [67, 68]:
                    pass
                else:
                    self.panel.pad.addnstr(count,0, line, self.panel.cols)
            count += 1
        #printErr("end of FOR loop.")
        self.refresh()
        self.currDir = "/home/honus/music/Books\,\ The/"
        #printErr("totally working")

    def albums(self):
        self.currDir = "/home/honus/music/Books\,\ The/"
        "\(2003\)\ The\ Lemon\ of\ Pink\ \{Tomlab\ -\ FLAC\}/"
        """
    Albums = []
    for line in os.listdir(currentDir):
        if not line[0] in PNCT:
            Albums.append(line)
    Albums.sort()
    count = 1
    for album in Albums:
        print "%2d. %s" %(count, album)
        count+=1
    entryAlbum  = raw_input("   --- CHOOSE THE ALBUM NUMBER:    ")
    if entryAlbum == "":
        currentDir = currentDir + '/' + Albums[0]
    else:
        currentDir = currentDir + '/' + Albums[formatNumber(entryAlbum)-1]
        """

    def songs(self):        
        count = 1
        for song in self.songList:
            if song.split(".")[-1] in EXTS:
                line = "%2d. %s" %(count, song)
                line += (self.songPane.cols - len(line)) * ' '
                if count == self.cursor:
                    self.songPane.pad.addnstr(count,0,
                                              line, self.songPane.cols,
                                              curses.A_STANDOUT)
                else:
                    self.songPane.pad.addnstr(count,0, line, self.songPane.cols)
            count += 1
        self.refresh()

    #currentDir  = HOME + Artists[formatNumber(entryArtist)]
        
    def scroll(self, direction):
        if self.cursor == self.startLine and direction < 0:
            self.startLine -= 1
            self.cursor -= 1
            if self.cursor == 0:
                self.cursor = self.padLength
                self.startLine = self.padLength-self.panel.rows+1
            else:
                pass
        elif self.cursor == self.startLine+self.panel.rows-1 and direction > 0:
            self.startLine += 1
            self.cursor += 1
            if self.cursor == self.padLength+1:
                self.cursor = 1
                self.startLine = 1
            else:
                pass
        else:
            if direction > 0:
                self.cursor += 1
            elif direction < 0:
                self.cursor -= 1
            else:
                printErr("scrolling trouble")
        self.artists()

    def refresh(self):
        self.panel.ready()
        self.panel.pad.refresh(self.startLine, 0, 
                               self.panel.ypos+3, self.panel.xpos+2, 
                               self.panel.rows+2, self.panel.cols+2)
    def cleanUp( self ):
        if self.wave is None:
            pass
        else:
            cleanUp = 'rm' + self.wave
            os.system( cleanUp)

    def playTrac( self, wave=None, showType=None ):
        if wave is None:
            self.show = lightShow(self.wave)
        else:
            self.show = lightShow(wave)
        #path = self.oldPick()
        path = "/home/honus/music/Books\,\ The/\(2003\)\ The\ Lemon\ of\ Pink\ \{Tomlab\ -\ FLAC\}/03\ -\ Tokyo.flac"
        self.decodeTrac(path)
        msg = "   >>>>>>   Song Playing   <<<<<<  "
        stdscr.addstr(scrmaxy-1,0, string.join((msg,msg)) )
        #self.show.play()

    def decodeFile( self, path ):
        decodeCmd = ''
        file = self.formatPath(path)
        if False:
            stdscr.addstr(scrmaxy-1,0, "--Filename: ", file)
        if file.endswith('flac'):
            decodeCmd = string.join( ("flac -f -d", file) )
            self.wave = file.rstrip('flac') + 'wav'
        elif file.endswith('mp3'):
            self.wave = file.rstrip('mp3') + 'wav'
            decodeCmd = string.join( ("lame --decode", file, self.wave) )
        elif file.endswith('wav'):
            decodeCmd = None
            self.wave = None
        else:
            raise Exception
        if False:
            if decodeCmd is not None:
                os.system(decodeCmd)
                stdscr.addstr(scrmaxy-1,0,"Decoded: " + file )
                #"ERROR: output file /home/honus/music/Menomena/Menomena - Friend and Foe/02 - The Pelican.wav already exists, use -f to override" deal with this here
            else:
                stdscr.addstr(scrmaxy-1,0,"Can't Decode: " + file )
        else:
            stdscr.addstr(scrmaxy-1,0,"Did Nothing to: " + file )

    def formatPath( self, path ):
        setx  = ( ' ', '[', ']', '{', '}', '(', ')', '\'' )
        result = ''
        for index in range( len(path) ):
            temp = ''
            char = path[index]
            for bad in setx:
                if( bad == char ):
                    result = string.join((result,'\\',char),'')
                else:
                    temp += bad
            if( len(temp) == len(setx) ):
                result = string.join((result,char),'')
            else:
                pass
        return result

    def formatNumber( self, entry ):
        result = ''
        for char in entry:
            for num in range(0,10):
                if( int(char) == num ):
                    result += char
                else:
                    pass
        return int(result)


    ##
    ##   Terminate screen
    ##
    #########################

def termscr():
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(0)
    #curses.curs_set(2)
    curses.endwin()
    os.system('clear')
    sys.exit()

if __name__=="__main__":
    try:
    
        ##
        ##   Build screen
        ##
        #########################

	global stdscr, scrmaxx, scrmaxy, panelist
	stdscr = curses.initscr()
        scrmaxy, scrmaxx = stdscr.getmaxyx()
	curses.start_color()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)
        stdscr.refresh()
        #curses.curs_set(0)
	if curses.has_colors():
            curses.init_pair(1, curses.COLOR_RED,   curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_BLUE,  curses.COLOR_BLACK)
        """
        pane_L = panels(  0, 74,  3, 15, title="setColor" )
	pane_D = panels(  0, 50,  3, 15,  title="runSine" )
        pane_C = panels(  8, 50,  5, 39,   title="Albums" )
        pane_B = panels( 18, 50, 12, 39,    title="Songs" )
        pane_A = panels(  0,  1, 30, 40,  title="Artists" )
	panelist = { 1: pane_A, 2: pane_B, 3: pane_C, 4: pane_D, 5: pane_L }
        """


        ##
        ##   Music Interface
        ##
        #########################

        Lbry = music()
        Lbry.loadLbry()


        ##
        ##   Keyboard Interface
        ##
        #########################

	while True:
	    c = stdscr.getch()
	    if c == curses.KEY_UP:
                Lbry.scroll(-1)
	    elif c == curses.KEY_DOWN:
                Lbry.scroll(1)
	    elif c == curses.KEY_RIGHT:
                pass
	    elif c == curses.KEY_LEFT:
                pass
	    elif c == curses.KEY_ENTER:
                pass
	    elif c == curses.KEY_RESIZE:
                pass
            elif c == ord('q'):
                for ms in (0, 100, 100):
                    curses.napms(ms)
                    curses.beep()
        	raise QuitError("User quit.")
            else:
                curses.beep()


    ##
    ##   Exception Defs   
    ##
    #########################

    except HostError:
	termscr()
	print "HostError: Couldn't find host IP."
    except QuitError, (quitErr):
        termscr()
        print "QuitError: ", quitErr.msg
    except PaneError, (paneErr):
        termscr()
        print "PaneError: ", paneErr.msg
    except KeyboardInterrupt:
        Lbry.cleanUp()
    finally:
        termscr()
