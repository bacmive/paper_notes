#!/usr/bin/python
from z3 import *
from pdr import PDR

def ExampleOne():
	x = Bool('x')
	y = Bool('y')
	z = Bool('z')
	xp = Bool('xp')
	yp = Bool('yp')
	zp = Bool('zp')

	variables = [x,y,z]
	primes = [xp, yp, zp]
	init = And(x, y, Not(z))
	trans = And(
				Or(Not(x), zp),
				Or(x, Not(zp)),
				Or(y, Not(yp)),
				Or(Not(x), Not(y), Not(xp)),
				Or(Not(z), xp, x),
				Or(Not(z), xp, y)
			)
	post = Or(Not(x), Not(y), Not(z))
	return (variables, primes, init, trans, post)


if __name__ == "__main__":
	solver = PDR(*ExampleOne())
	solver.run()