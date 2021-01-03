#!/usr/bin/python
from z3 import *
from pdr import PDR

def Test_test1():
    i2 = Bool('i2')
    i4 = Bool('i4')
    primary_inputs=[ i2,i4 ]
    l12 = Bool('l12')
    l12p = Bool(str(l12) + '\'')
    l10 = Bool('l10')
    l10p = Bool(str(l10) + '\'')
    variables=[ l12,l10 ]
    primes=[ l12p,l10p ]
    a6 = And(i2, i4)
    a8 = And(i4, Not(a6))
    a14 = And(Not(l10), l12)
    init = And(*[ Not(l10),Not(l12) ])
    trans = And(*[ l10p == a8,l12p == a6 ])
    post = Not(a14)
    return (primary_inputs, variables, primes, init, trans, post)

tests = {'Test_test1':Test_test1}

def listTests():
	for name in tests:
		print name

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Run tests examples on the PDR algorithm")
	parser.add_argument('-ls', action='store_true')
	parser.add_argument('testname', type=str, help='The name of the test to run', default=None, nargs='?')
	args = parser.parse_args()
	if(args.ls):
		listTests()
	elif(args.testname!=None):
		name = args.testname
		print "=========== Running test", name,"==========="
		solver = PDR(*tests[name]())
		solver.run()
	else:
		for name in tests:
			print "=========== Running test", name,"==========="
			solver = PDR(*tests[name]())
			solver.run()
