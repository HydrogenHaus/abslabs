#!/usr/bin/python

##
##     A Diagnostics Module for
##      ColorKinetics Lights
##
#####################################

from lightUtil import setState, lights
from time import sleep

def whiteTest(inst,time=3):
    for light in inst.state:
        inst.setLight(light, (64,64,64))
    inst.update()
    if time:
        sleep(time)
        inst.reset()

def scanTest(inst,time=0.1):
    init_state = inst.state
    for light in inst.state:
        setState({light:(64,0,0)},inst.ip,inst.port)
	sleep(time)
	setState({light:(0,64,0)},inst.ip,inst.port)
	sleep(time)
	setState({light:(0,0,64)},inst.ip,inst.port)
	sleep(time)
    setState(init_state,inst.ip,inst.port)

if __name__=="__main__":
    test = lights(50)
    whiteTest(test)
