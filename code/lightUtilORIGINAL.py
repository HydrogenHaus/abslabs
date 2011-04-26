#!/usr/bin/python

###########################################
##                 _    _                ##
##    _           | |  | |        _      ##
##   | |          | |  | |       | |     ##
##   | |o    _   _| |  | |  _   o| |     ##
##   | |_ __| |_| |_|__| |_| |_ _| |     ##
##   | | |_o ||_   _|    /_   _| | |     ##
##   |_|_|__/_|_|_|\____/  |_| |_|_|     ##
##                                       ##
##                                       ##
##     low level utilities for           ##
##     interfacing with ColorKinetics    ##
##     lights                            ##
##                                       ##
##                                       ##
###########################################
##                                       ##
##    Authors: Rurik Primiani            ##
##             Blake Rego                ##
##             Brian Tovar               ##
##                                       ##
###########################################

from socket import socket, AF_INET, SOCK_DGRAM
from math import sin, pi, floor
from time import sleep
from array import array
from struct import pack
from random import randint
import os, sys


##
##  some color macros
##
###########################################

black      = (0,   0,   0  )
white      = (255, 255, 255)
red        = (255, 0,   0  )
dark_red   = (128, 0,   0  )
green      = (0,   255, 0  )
dark_grn   = (0,   128, 0  )
blue       = (0,   0,   255)
dark_blu   = (0,   0,   128)
dark_gry   = (64,  64,  64 )
gray       = (128, 128, 128)
cyan       = (0,   255, 255)
dark_cyn   = (0,   128, 128)
magenta    = (255, 0,   255)
dark_mag   = (128, 0,   128)
yellow     = (255, 255, 0  )
dark_yel   = (128, 128, 0  )
orange     = (255, 128, 0  )
brown      = (166, 42,  42 )


##
##  setState: packetizes and ships
##      the current state of the lights
##      over udp
##
##      state:
##          keys   -- light number
##              where number = 0,1,2,...
##          values -- lists of the form
##              (red, green, blue)
##          e.g. : {0:(128,128,255), 1:(255,255,128)}
##
###########################################

def setState(state, ip="192.168.1.244", port=6038):
    levels = [0]*3*(max(state)+1)
    for light in state:
        addr  = 3*light
        red   = state[light][0]
        green = state[light][1]
        blue  = state[light][2]

        levels[addr]   = red
        levels[addr+1] = green
        levels[addr+2] = blue

    arr = array('B', levels)
    fmt = "<LHHLBxHlB"+str(len(arr))+"s"
    hdr = 0x4adc0104, 0x0001, 0x0101, 0, 0, 0, -1, 0, arr.tostring()
    out = pack(fmt, *hdr)
    socket(AF_INET, SOCK_DGRAM).sendto(out, (ip, port))


##
##  lights: a class object for inter-
##      facing with an entire light
##      system
##
##      number:
##          the total number of lights
##          in the system
##
###########################################

class lights():
    def __init__(self, number, ip="192.168.1.244", port=6038):
        self.number = number
        self.ip = ip
        self.port = port
        self.state = {}
        self.reset()
    def __del__(self):
        self.reset()
    def __enter__(self):
	return self
    def __exit__(self):
	self.reset()
    def update(self):
        setState(self.state, self.ip, self.port)
    def reset(self, color=(0,0,0)):
        for light in range(self.number):
            self.state[light] = color
        self.update()
    def setLight(self, light, color):
        self.state[light] = color
        self.number = len(self.state)


##
##  group: a macro class for controlling
##      the color of groups of lights
##      simultaneously
##
##      lights_inst:
##          a lights class object
##      subset:
##          a subset of the lights
##          must be a list of integers
##          ex: [0,1,3] or even just [3]
##
###########################################


class group():
    def __init__(self, lights_inst, subset):
        if not set(subset).issubset(range(lights_inst.number)):
            raise Exception, "Not a subset of the total lights."
        self.lights_inst = lights_inst
        self.subset = subset
        self.number = len(subset)
        self.state = {}
        self.color = (-1,-1,-1)
        for light in subset:
            self.state[light] = lights_inst.state[light]
    def __call__(self, *args):
        if len(args)==1 and isinstance(args[0],tuple):
            self.setColor(args[0])
        elif len(args)==3:
            self.setColor((args[0],args[1],args[2]))
        else:
            raise Exception, "Only a list/tuple or three separate values accepted"
    def setColor(self, color):
        self.color = color
        for light in self.subset:
            self.lights_inst.setLight(light, color)
        self.lights_inst.update()


##
##  Some useful functions for dynamic
##      changes in light states
##
###########################################

def sineLight(time, phase=0, freq=100, amp=100, steps_per_cycle=100):
    if amp > 100:
        amp = 100
    bias = 127
    return int(127*amp/100.*sin(pi*freq/100.*time/steps_per_cycle+phase)+bias)

def powerSine(time, phase=0, freq=100, amp=100, steps_per_cycle=100):
    if amp > 100:
        amp = 100
    p = amp/100.*sin(pi*freq/100.*time/steps_per_cycle+phase)
    return round(p*p, 4)

def genRand():
    return (randint(0,255), randint(0,255), randint(0,255))

    

##
##  This runs if the module is executed
##      on the command line
##
###########################################

if __name__=="__main__":
    demo = lights(100)
    for i in demo.state:
        demo.setLight(i,white)
    demo.update()
    sleep(5)
    
