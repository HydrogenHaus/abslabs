from lightUtil import lights
from runSine import runSine
from random import randint
from time import sleep
import sys

if __name__=="__main__":
    try:
	test = lights(7,ip="76.24.23.162",port=51413)
	if len(sys.argv) == 2:
            while True:
                runSine( test, float(sys.argv[1]), (randint(0,255), randint(0,255), randint(0,255)) )
                sleep(1)
	else:
            while True:
                runSine( test, 25, (randint(0,255), randint(0,255), randint(0,255)) )
                sleep(1)
    except:
	test.reset()
