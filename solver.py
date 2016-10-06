import sys
import math
import scipy.optimize as opt

PENALTY=float(sys.argv[1])

def f(e):
    return e-(1.0/(1.0+math.pow(math.e,(-PENALTY*math.log(1.0-e)))))

print f(0.5)
print opt.fsolve(f,0.5)
