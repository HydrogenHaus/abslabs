from lightUtil import lights
from random import randint
from time import sleep
import sys

def oneColor(inst, color):
    print str(color[0]) + " " + str(color[1]) + " " + str(color[2])
    inst.reset(color)

if __name__=="__main__":
    try: 
        test = lights(24)
        if len(sys.argv) == 4:
            oneColor(test, (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])) )
        else:
            oneColor(test, (randint(0,255), randint(0,255), randint(0,255)) )
        while True:
            sleep(1000)
    except:
        test.reset()
