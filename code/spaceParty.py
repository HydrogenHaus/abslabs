#!/usr/bin/python

import os
from pyplayer import track
import sys
from pKill import pKill
import threading
from random import randint

MUSIC_DIR = "/home/honus/svn/abslabs/music/"

def handleStrangeCharacters( s ):
    SETX  = ( ' ', '[', ']', '{', '}', '(', ')', '\'' )
    result = ''
    for index in range( len(s) ):
        temp = ''
        CHAR = s[index]
        for BAD in SETX:
            if( BAD == CHAR ):
                result = result+'\\'+CHAR
            else:
                temp = temp+BAD
        if( len(temp) == len(SETX) ):
            result = result+CHAR
        else:
            pass
    return result

def keepWav( myList ):
    for element in myList:
        if not element.endswith( '.wav' ):
            print element
            myList.remove( element )
        else:
            pass

class partyPlayer():
    def __init__(self):
        self.iterator = 0
        self.initializeFiles()
        self.pk = pKill()
        self.random = False


    def initializeFiles(self):
        self.songList = os.listdir(MUSIC_DIR)  
        keepWav( self.songList )
        self.songList.sort()        

    def runAll(self):
        threading.Thread( target=self.keyboardEvent ).start()

        if( self.random == True ):
            
            

        while self.iterator <= len(self.songList):
            songPath = MUSIC_DIR + handleStrangeCharacters( self.songList[self.iterator] )
            playCommand = 'python /home/honus/svn/abslabs/showFFT.py ' + songPath
            os.system( 'clear' )
            self.listSomeSongs()
            self.printUsage()
            os.system( playCommand )
            self.iterator = self.iterator + 1

    def printUsage(self):
        print """
*************************************************************************************
        Key:    Function: 
        n       next song
        p       previous song
        l       list available songs
        s       skip to letter
        q       quit
       
        Press a key followed by <enter>.
        """
        aestheticFlare = '*******************************'
        song = self.songList[self.iterator].split('.')[0]
        song += (10 -len(song) )*' ' 
        print aestheticFlare, ' Playing: ', song, aestheticFlare

    def killFFT(self):
        self.pk.killSet( self.pk.getPIDs() )

    def nextSong(self):
        self.killFFT()

    def quit(self):
        print 'Goodbye!' 
        os.system( 'kill -9 `pgrep python`' )

    def prevSong(self):
        self.iterator -= 2
        self.killFFT()

    def listAllSongs(self):
        os.system( 'clear' )
        for song in self.songList:
            if song == self.songList[self.iterator]:
                print '****** CURRENT SONG: ', song.split('.')[0], '*************'
            else:
                print song.strip( '.wav' )
        
        self.printUsage()

    def listSomeSongs(self, numSongs=10):

        if self.iterator < numSongs:
            min = 0
        else: 
            min = self.iterator - numSongs
        if self.iterator+5 > len( self.songList )-1:
            max = len( self.songList ) -1
        else:
            max = self.iterator + numSongs

        for something in range( min, max):
            song = self.songList[ something ] 
            if self.songList[ self.iterator ] == self.songList[ something ]:
                print '****** CURRENT SONG: ', song.split('.')[0], '*************'
            else:
                print song.split('.')[0]

    def skipToLetter(self):
        letter = raw_input("Select a leter to skip to: ")
        for song in self.songList:
            if song.lower().startswith( letter.lower() ):
                self.iterator = self.songList.index( song )-1
                self.killFFT()
                os.system( 'clear' )
                break
            else:
                print 'Nothing starts with your string!'
                self.printUsage()

    def keyboardEvent(self):
        while True: 
            cmd = raw_input("")
            if cmd == 'n':
                self.nextSong()
            elif cmd == 'q':
                self.quit()
            elif cmd == 'p':
                self.prevSong()
            elif cmd == 'l':
                self.listAllSongs()
            elif cmd == 's':
                self.skipToLetter()




if __name__=="__main__":
    partyTime = partyPlayer()
    partyTime.runAll()
