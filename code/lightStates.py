#!/usr/bin/env python2.5


from random import randint, uniform
from numpy import *
from lightUtil import setState


initial_state = { 0:(0,0,0),
                  1:(0,0,0),
                  2:(0,0,0),
                  3:(0,127,0),
                  4:(0,0,0),
                  5:(0,0,0),
                  6:(0,0,0),
                  }


cycle_left = matrix( [ [0,1,0,0,0,0,0],
                       [0,0,1,0,0,0,0],
                       [0,0,0,1,0,0,0],
                       [0,0,0,0,1,0,0],
                       [0,0,0,0,0,1,0],
                       [0,0,0,0,0,0,1],
                       [1,0,0,0,0,0,0] ] )


cycle_rght = matrix( [ [0,0,0,0,0,0,1],
                       [1,0,0,0,0,0,0],
                       [0,1,0,0,0,0,0],
                       [0,0,1,0,0,0,0],
                       [0,0,0,1,0,0,0],
                       [0,0,0,0,1,0,0],
                       [0,0,0,0,0,1,0] ] )


rand_state = {}
for i in range(7):
    rand_state[i] = (randint(0,255),randint(0,255),randint(0,255))


rand_square = zeros((7,7))
for a in range(7):
    for b in range(7):
        if b is randint(0,7) or randint(0,7):
            rand_square[a][b] = uniform(-1,2)


rand_matrix = matrix(rand_square)


fade = matrix( [ [0,0,1],
                 [1,0,0],
                 [0,1,0] ] )


def dict_to_matrix(dic):
    lis = []
    for a,b in dic.iteritems():
        lis.append(list(b))
    return matrix(lis)


def matrix_to_dict(mat):
    lis = mat.tolist()
    dic = {}
    for i in range(len(lis)):
        dic[i] = tuple(lis[i])
    return dic


class lights:
    def __init__(self, state):
        self.state = dict_to_matrix(state)
    def update(self):
        setState(matrix_to_dict(self.state))
    def setOper(self, left_op, right_op):
        self.left_op = left_op
        self.right_op = right_op
    def getNext(self):
        self.state = self.left_op * self.state * self.right_op


if __name__=="__main__":
    from time import sleep
    a = lights(initial_state)
    a.setOper(cycle_left,fade)
    a.update()
    while True:
        print a.state
        sleep(0.1)
        a.getNext()
        a.update()
