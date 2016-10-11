#!/usr/bin/python

import random, math
import scipy.optimize as opt
import argparse

class guess:
    def __init__(self, N, costgood=10, costbad=1):
        self.N = N
        self.goodcost = costgood
        self.badcost = costbad
        self.__number = random.randint(0,N)
        self.__counter = 0

    def countgood(self):        self.__counter += self.goodcost; return True
    def countbad(self):         self.__counter += self.badcost; return False
    def check(self, condition): return self.countgood() if condition else self.countbad()       

    def smaller(self, N):       return self.check(N < self.__number)
    def larger(self, N):        return self.check(N > self.__number)
    def ininterval(self, N, M): return self.check(N <= self.__number < M)
    def equals(self, N):        return self.check(N == self.__number)
    def getcost(self):          return self.__counter


def synalgo(game):
    start, end = 0, game.N
    found = False

    # binary search
    while True:
        linearcost = ((end-start)/2.0) * game.badcost + game.goodcost
        binarycost = math.log((end-start), 2) * game.goodcost * 0.5
        if linearcost < binarycost:
            break
        guess = start + (end-start)/2
        ret = game.larger(guess)
        if ret:
            end = guess
        else:
            start = guess
        if end-start == 1:
            if game.equals(start):
                #print "N is", start
                pass
            else:
                #print "N is", end
                pass
            found = True
            break

    if not found:
        # linear search
        for i in xrange(start, end+1):
            if game.equals(i):
                found=True
                break
    if not found: raise Exception("synalgo failed :(")
    return game.getcost()

def naive(game):
    for i in xrange(0, game.N+1):
        if game.equals(i):
            return game.getcost()
    raise Exception("naive failed :(")


def cj(game,start,end):
    chunksize = float(game.goodcost) / float(game.badcost)
    newend=start+int((end-start)/chunksize)
    if newend==start:
        for i in xrange(start,end+1):
            if game.equals(i):
                return game.getcost()
        raise Exception("cj failed :(")

    if game.ininterval(start,newend):
        return cj(game,start,newend)
    else:
        return cj(game,newend,end)

def ew(game,ew_opt,start,end):
    newend=start+int((end-start)*ew_opt)
    if newend==start:
        for i in xrange(start,end+1):
            if game.equals(i):
                return game.getcost()
        raise Exception("ew failed :(")

    if game.ininterval(start,newend):
        return ew(game,ew_opt,start,newend)
    else:
        return ew(game,ew_opt,newend,end)

parser = argparse.ArgumentParser(description='Number guessing game simulator')
parser.add_argument("--bound",default=10000,type=int,help="Upper bound of the guess")
parser.add_argument("--good",default=10,type=float,help="Cost of positive answers (should be higher than --bad)")
parser.add_argument("--bad",default=1,type=float,help="Cost of negative answers (should be lower than --good)")

args = parser.parse_args()

MAX = 1000
BOUND = args.bound
COSTGOOD = args.good
COSTBAD = args.bad
PENALTY = COSTGOOD-COSTBAD


def ew_f(e):
    return e-(1.0/(1.0+math.pow(math.e,(-PENALTY*math.log(1.0-e)))))

ew_opt=opt.fsolve(ew_f,0.5)[0]

# Execute

print "Iterations\tUpper bound\tPenalty"
print "%d\t\t%d\t\t%f" % (MAX,BOUND,PENALTY)
print "\nEW calculated: %f\n" % ew_opt
s = 0
for i in xrange(0, MAX):
    s += naive(guess(BOUND, COSTGOOD, COSTBAD))
print "naive average of", MAX, "runs:", float(s)/MAX

s=0
for i in xrange(0,MAX):
    s+= ew(guess(BOUND,COSTGOOD,COSTBAD),0.5,0,BOUND)
print "binary average of", MAX, "runs:", float(s)/MAX

s=0
for i in xrange(0, MAX):
    s += synalgo(guess(BOUND,COSTGOOD,COSTBAD))
print "synapse average of", MAX, "runs:", float(s)/MAX

s=0
for i in xrange(0,MAX):
    s+= cj(guess(BOUND,COSTGOOD,COSTBAD),0,BOUND)
print "cj average of", MAX, "runs:", float(s)/MAX

s=0
for i in xrange(0,MAX):
    s+= ew(guess(BOUND,COSTGOOD,COSTBAD),ew_opt,0,BOUND)
print "ew average of", MAX, "runs:", float(s)/MAX

