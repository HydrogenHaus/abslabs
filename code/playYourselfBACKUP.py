#!/usr/bin/env python


from time import time
from random import uniform
from threading import Thread


if __name__ == "__main__":

    import sys

    cmd = raw_input("")
    m.quit = True
    while m.isAlive():
        pass

    true_time = m.count * m.step
    actual_time = m.tlast - m.tfirst
    error = actual_time - true_time
    print "Total error was %.4f ms" %(error*1000.0)
    print "  percent error was %.6f%%" %((error/true_time)*100)
    print "  for a total time of %.2f s" %actual_time
