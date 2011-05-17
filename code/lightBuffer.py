#!/usr/bin/env python  

from showFFT import powerToColor, updateRoom
from lightUtil import * 


class lightBuffer:

    def __init__(self, bufferSize = 7):
        self.trackList = []
        self.bufferSize = bufferSize

    def update(self, track, lightInst):
        newTrackSnippet = trackSnippet( track )
        self.trackList.append(newTrackSnippet)
        if len(self.trackList) >= self.bufferSize:
            updateRoom(self.trackList[0], lightInst)
            self.trackList.remove(self.trackList[0])
        #else:
        #    print len(self.trackList)

class trackSnippet: 
    def __init__(self, track):
        self.power = track.power
