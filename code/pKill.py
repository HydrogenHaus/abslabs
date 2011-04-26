#!/usr/bin/python

from lightUtil  import *
from runSine    import runSine

class pKill():
    def __init__(self):
        import os
        self.me = os.getpid()
    def killAll(self):
        s = os.popen("kill -9 `ps ax | grep python | cut -d ' ' -f 2` ").read()
        print s
    def getPIDs(self):
        import string
        import subprocess
        PIPE = subprocess.PIPE
        result = []
        a = subprocess.Popen(["pgrep", "python"], stdout=PIPE).communicate()[0]
        all = string.split(a, '\n')
        #print "ME:", self.me
        for pid in all:
            if pid is '':
                pass
            elif int(pid) == self.me:
                pass
            else:
                result.append(int(pid) )
        #print "RESULT:", result
        return result
    def killSet(self, toKill=[] ):
        if toKill == None:
            pass
        else:
            for pid in toKill:
                cmd = "kill -9 " + str(pid)
                os.system(cmd)

if __name__=="__main__":
    try:
        test = lights(24)
        pk = pKill()
        pk.killSet(pk.getPIDs() )
        test.reset((255,128,0) )
        while True:
            pass
    except KeyboardInterrupt:
        test.reset()
