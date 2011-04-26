#!/usr/bin/python

import os
from pyplayer import track
import sys

MUSIC_DIR = "/home/honus/music/"


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

if __name__=="__main__":
    
    count = 0
    for artist in os.listdir(MUSIC_DIR):
        print count, artist
        count+=1
        
    cmd = raw_input("--- Chose the number corresponding to the artist you would like to hear:")
    currentDir = MUSIC_DIR + os.listdir(MUSIC_DIR)[int(cmd)]
        
    count = 0
    for album in os.listdir(currentDir):
        print count, album
        count+=1
            
    cmd = raw_input("--- Choose the number corresponding to the album you would like to hear:")
    currentDir = currentDir + '/' + os.listdir(currentDir)[int(cmd)]
            
    count = 0
    for song in os.listdir(currentDir):
        print count, song
        count += 1

    cmd   = raw_input("--- Choose the number corresponding to the song you would like to hear:")

    track = currentDir + '/' + os.listdir(currentDir)[int(cmd)]
    
    print track
    print len(track)


    track = handleStrangeCharacters( track )
    myCommand = "flac -d " + track
    #print myCommand
    os.system( myCommand )
    waveFile = ''
    for char in range( len(track)-4 ):
        waveFile += track[char]
    

    waveFile += 'wav'
    print waveFile

    print '1 - showFFT.py'
    print '2 - showAvgPower.py'
    cmd = raw_input("--- Choose a script to run \n")
    playCommand = ''
    if cmd== '1' : 
        playCommand = 'python /home/honus/svn/abslabs/showFFT.py ' + waveFile
        valid='true'
    elif cmd=='2' : 
        playCommand = 'python /home/honus/svn/abslabs/showAvgPower.py ' + waveFile
        valid='true'
    else: 
        print 'Invalid choice, please select 1 or 2.'

    print playCommand
    os.system( playCommand )
    
    rmCommand = 'rm ' + waveFile
    os.system( rmCommand ) 
