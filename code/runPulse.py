#!/usr/bin/python


from lightUtil import lights, group
from random import randint
from time import sleep
import sys

def runPulse(inst, time=3):
    odd  = group(inst, range(1, inst.number, 2))
    even = group(inst, range(0, inst.number, 2))
    
    while True:
        odd.setColor( (randint(0,255), randint(0,255), randint(0,255)) )
        even.setColor( (randint(0,255), randint(0,255), randint(0,255)) )
        sleep(time)

if __name__=="__main__":
    try:
	test = lights(50)
	runPulse(test,float(sys.argv[1]))
    except:
        print 'error'
