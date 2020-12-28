#!/usr/bin/python
from z3 import *
from pdr import PDR

def Test_test2():
    i8 = Bool('i8')
    i10 = Bool('i10')
    primary_inputs=[ i8,i10 ]
    l2 = Bool('l2')
    l2p = Bool(str(l2) + '\'')
    l24 = Bool('l24')
    l24p = Bool(str(l24) + '\'')
    l26 = Bool('l26')
    l26p = Bool(str(l26) + '\'')
    l4 = Bool('l4')
    l4p = Bool(str(l4) + '\'')
    variables=[ l2,l24,l26,l4 ]
    primes=[ l2p,l24p,l26p,l4p ]
    a6 = And(Not(i8), Not(i10))
    a22 = And(Not(l24), Not(l26))
    a20 = And(Not(a22), l24)
    a28 = And(i8, Not(a20))
    a30 = And(a20, Not(i8))
    a32 = And(Not(a28), Not(a30))
    a34 = And(Not(l24), l26)
    a36 = And(i10, Not(l26))
    a38 = And(l26, Not(i10))
    a40 = And(Not(a36), Not(a38))
    a42 = And(Not(l26), Not(i10))
    a44 = And(l26, a40)
    a46 = And(Not(a42), Not(a44))
    a48 = And(Not(l24), a46)
    a50 = And(a34, i10)
    a52 = And(Not(a34), Not(a48))
    a54 = And(Not(a50), Not(a52))
    a18 = And(a32, Not(a54))
    a16 = And(a18, a32)
    a14 = And(a16, Not(a54))
    a12 = And(l4, a14)
    a56 = And(Not(l2), a6)
    a58 = And(l2, a12)
    a60 = And(Not(a56), Not(a58))
    a62 = And(l24, Not(l26))
    a64 = And(l4, a62)
    init = And(*[ Not(l4),Not(l2),Not(l24),Not(l26) ])
    trans = And(*[ l4p == Not(a60),l2p == And(True),l24p == i8,l26p == i10 ])
    post = Not(a64)
    return (primary_inputs, variables, primes, init, trans, post)

tests = {'Test_test2':Test_test2}

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
