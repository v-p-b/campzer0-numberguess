#!/usr/bin/python

import random, math

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
                print "N is", start
            else:
                print "N is", end
            found = True
            break

    if not found:
        # linear search
        for i in xrange(start, end+1):
            if game.equals(i):
                break

    return game.getcost()


def naive(game):
    for i in xrange(0, game.N+1):
        if game.equals(i):
            return game.getcost()
    raise Exception("naive failed :(")


def cj(game,start,end):
    chunksize = game.goodcost / game.badcost
    newend=start+(end-start)/chunksize
    if newend==start:
        for i in xrange(start,end+1):
            if game.equals(i):
                return game.getcost()
        raise Exception("cj failed :(")

    if game.ininterval(start,newend):
        return cj(game,start,newend)
    else:
        return cj(game,newend,end)

MAX = 10000
BOUND = 200

s = 0
for i in xrange(0, MAX):
    s += naive(guess(BOUND))
print "naive average of", MAX, "runs:", float(s)/MAX

s=0
for i in xrange(0, MAX):
    s += synalgo(guess(BOUND))
print "synapse average of", MAX, "runs:", float(s)/MAX


s=0
for i in xrange(0,MAX):
    s+= cj(guess(BOUND),0,BOUND)
print "cj average of", MAX, "runs:", float(s)/MAX
