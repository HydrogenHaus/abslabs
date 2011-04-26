#!/usr/bin/python

import os
import sys
import string
from pKill import pKill
#from pyplayer import track


HOME = "/home/honus/music/"
EXTS = ('flac', 'mp3', 'wav')
PNCT = ('.', '_', '#')

def decodeFile( path ):
    decodeCmd = ''
    file = formatPath(path)
    #print "--Filename: ", file
    if file.endswith('flac'):
        decodeCmd = string.join( ("flac -d", file) )
        wave = file.rstrip('flac') + 'wav'
    elif file.endswith('mp3'):
        wave = file.rstrip('mp3') + 'wav'
        decodeCmd = string.join( ("lame --decode", file, wave) )
    elif file.endswith('wav'):
        decodeCmd = "None"
        wave = "None"
    else:
        print "File Type Error: must be wav, flac, or mp3"
        raise Exception
    os.system( decodeCmd )
    #print "--decodeCommand: ", decodeCmd
    #print "--Wave File: ", wave
    return wave


def playTrac( wave=None ):
    print "1 showFFT.py"
    print "2 showAvgPower.py"
    entryScript = raw_input("--- CHOOSE A SCRIPT TO RUN:     ")
    playCommand = ''
    if( entryScript == '2' ):
        playCmd = string.join( ("python /home/honus/svn/abslabs/showAvgPower.py", wave) )
    else:
        playCmd = string.join( ("python /home/honus/svn/abslabs/showFFT.py", wave) )
    msg = "   >>>>>>   Song Playing   <<<<<<   "
    print "\n", string.join( (msg, msg) ), "\n"
    #print "--playCommand: ", playCmd
    os.system( playCmd )


def cleanUp( wave=None ):
    if( wave is "None" ):
        pass
    else:
        cleanUp = "rm " + wave
        #print "--cleanUp: ", cleanUp
        os.system( cleanUp)
    print "   --- SONG FINISHED, CLEAN-UP DONE.   "


def formatPath( path ):
    setx  = ( ' ', '[', ']', '{', '}', '(', ')', '\'' )
    result = ''
    for index in range( len(path) ):
        temp = ''
        char = path[index]
        for bad in setx:
            if( bad == char ):
                #join((result,'\\',char),'')
                result += '\\'+char
            else:
                temp += bad
        if( len(temp) == len(setx) ):
            #result.join((result,char),'')
            result += char
        else:
            pass
    return result


def formatNumber( entry ):
    result = ''
    for char in entry:
        for intg in range(0,10):
            if( int(char) == intg ):
                result += char
            else:
                pass
    return int(result)


def loadLibrary():
    #for element in os.listdir(HOME)
    count = 0
    Artists = os.listdir(HOME)
    Artists.sort()
    for artist in Artists:
        print "%2d. %s" %(count, artist)
        count+=1

    entryArtist = raw_input("   --- CHOOSE THE ARTIST NUMBER:   ")
    currentDir  = HOME + Artists[formatNumber(entryArtist)]

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
            
    Songs = []
    for line in os.listdir(currentDir):
        if not line[0] in PNCT:
            Songs.append(line)
    Songs.sort()
    count = 1
    for song in Songs:
        if song.split(".")[-1] in EXTS and not song[0] in PNCT:
            print "%2d. %s" %(count, song)
            count += 1
    entrySong   = raw_input("   --- CHOOSE THE SONG NUMBER:     ")
    if entrySong == "":
        file = currentDir + '/' + Songs[0]
    else:
        file = currentDir + '/' + Songs[formatNumber(entrySong)-1]
    return file


if __name__=="__main__":
    pk = pKill()
    file = loadLibrary()
    trac = decodeFile(file)
    pk.killSet(pk.getPIDs() )
    playTrac(trac)
    cleanUp(trac)
