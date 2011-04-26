from lightUtil import *
from time import sleep


def fadeTo( inst, desiredColor, speed=100):
    inst.oldColor = inst.state.copy()
    for time in range(0,51):
	UP_scale = powerSine(time)
	DN_scale = 1. - UP_scale
	for light, color in inst.oldColor.iteritems():
	    newColor = ( int(desiredColor[0]*UP_scale+color[0]*DN_scale), int(desiredColor[1]*UP_scale+color[1]*DN_scale), int(desiredColor[2]*UP_scale+color[2]*DN_scale) )
	    inst.setLight(light, newColor)
	inst.update()
	sleep(1./speed)
	

if __name__=="__main__":
    try:
        test = lights(7)
	for light in test.state:
	    test.setLight(light,(255,0,0) )
	test.update()
        if( len(sys.argv) == 2):
	    while True:
                fadeTo( test, (randint(0,255), randint(0,255), randint(0,255)), float(sys.argv[1]) )
		sleep(1)
	else:
            while True:
		fadeTo( test, (randint(0,255), randint(0,255), randint(0,255)), 25 )
		sleep(1)
    except:
        test.reset()