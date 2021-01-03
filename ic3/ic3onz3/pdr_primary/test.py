#!/usr/bin/python
from z3 import *
from pdr import PDR



def MutualExclusive():
	len_inp = 7
	len_var = 9

	i2 = Bool('i2')
	i4 = Bool('i4')
	i6 = Bool('i6')
	i8 = Bool('i8')
	i10 = Bool('i10')
	i12 = Bool('i12')
	i14 = Bool('i14')
	primary_inputs = [i2, i4, i6, i8, i10, i12, i14]

	l16 = Bool('l16')
	l18 = Bool('l18')
	l20 = Bool('l20')
	l22 = Bool('l22')
	l24 = Bool('l24')
	l26 = Bool('l26')
	l28 = Bool('l28')
	l30 = Bool('l30')
	l32 = Bool('l32')

	l16p = Bool(str(l16) + '\'')
	l18p = Bool(str(l18) + '\'')
	l20p = Bool(str(l20) + '\'')
	l22p = Bool(str(l22) + '\'')
	l24p = Bool(str(l24) + '\'')
	l26p = Bool(str(l26) + '\'')
	l28p = Bool(str(l28) + '\'')
	l30p = Bool(str(l30) + '\'')
	l32p = Bool(str(l32) + '\'')

	variables = [l16, l18, l20, l22, l24, l26, l28, l30, l32]
	primes = [l16p, l18p, l20p, l22p, l24p, l26p, l28p, l30p, l32p]

	a34 = And(Not(i4), i2)
	a36 = And(a34, Not(i6))
	a38 = And(Not(i10), Not(i8))
	a40 = And(a38, a36)
	a42 = And(Not(i14), Not(i12))
	a44 = And(a42 , a40)
	a46 = And(a44 , Not(l16))
	a48 = And(Not(l20) , l18)
	a50 = And(a48 , l22)
	a52 = And(Not(l26) , l24)
	a54 = And(a52 , l28)
	a56 = And(a54 , l30)
	a58 = And(Not(a56) , Not(a50))
	a60 = And(l20 , l18)
	a62 = And(a60 , l22)
	a64 = And(l26 , l24)
	a66 = And(a64 , l28)
	a68 = And(Not(a66) , Not(a62))
	a70 = And(a68 , Not(l30))
	a72 = And(Not(a70) , a58)
	a74 = And(Not(a72) , i2)
	a76 = And(a72 , Not(i2))
	a78 = And(Not(a76) , Not(a74))
	a80 = And(Not(l20) , Not(l18))
	a82 = And(a80 , l22)
	a84 = And(a82 , Not(i10))
	a86 = And(a48 , l30)
	a88 = And(a86 , l22)
	a90 = And(i10 , Not(i8))
	a92 = And(a90 , a88)
	a94 = And(l20 , Not(l18))
	a96 = And(a94 , l22)
	a98 = And(a96 , i10)
	a100 = And(a62 , a38)
	a102 = And(l20 , i10)
	a104 = And(Not(l20) , Not(i10))
	a106 = And(Not(a104) , Not(a102))
	a108 = And(Not(a106) , i8)
	a110 = And(a108 , l18)
	a112 = And(Not(a106) , Not(i8))
	a114 = And(a112 , Not(l18))
	a116 = And(Not(a114) , Not(a110))
	a118 = And(Not(a116) , Not(a62))
	a120 = And(Not(a118) , Not(a100))
	a122 = And(Not(a120) , Not(a96))
	a124 = And(Not(a122) , Not(a98))
	a126 = And(Not(a124) , Not(a88))
	a128 = And(Not(a126) , Not(a92))
	a130 = And(Not(a128) , Not(a82))
	a132 = And(Not(a130) , Not(a84))
	a134 = And(Not(a132) , a78)
	a136 = And(Not(l26) , Not(l24))
	a138 = And(a136 , l28)
	a140 = And(a138 , Not(i14))
	a142 = And(a52 , l30)
	a144 = And(a142 , l28)
	a146 = And(i14 , Not(i12))
	a148 = And(a146 , a144)
	a150 = And(l26 , Not(l24))
	a152 = And(a150 , l28)
	a154 = And(a152 , i14)
	a156 = And(a66 , a42)
	a158 = And(l26 , i14)
	a160 = And(Not(l26) , Not(i14))
	a162 = And(Not(a160) , Not(a158))
	a164 = And(Not(a162) , i12)
	a166 = And(a164 , l24)
	a168 = And(Not(a162) , Not(i12))
	a170 = And(a168 , Not(l24))
	a172 = And(Not(a170) , Not(a166))
	a174 = And(Not(a172) , Not(a66))
	a176 = And(Not(a174) , Not(a156))
	a178 = And(Not(a176) , Not(a152))
	a180 = And(Not(a178) , Not(a154))
	a182 = And(Not(a180) , Not(a144))
	a184 = And(Not(a182) , Not(a148))
	a186 = And(Not(a184) , Not(a138))
	a188 = And(Not(a186) , Not(a140))
	a190 = And(Not(a188) , a134)
	a192 = And(a190 , a78)
	a194 = And(i6 , i4)
	a196 = And(Not(i6) , Not(i4))
	a198 = And(Not(a196) , Not(a194))
	a200 = And(a198 , a192)
	a202 = And(a200 , a198)
	a204 = And(a202 , Not(a132))
	a206 = And(a204 , Not(a188))
	a208 = And(a206 , l32)
	a210 = And(a208 , l16)
	a212 = And(Not(a210) , Not(a46))
	a214 = And(a150 , a94)
	a216 = And(a214 , l32)
 
	init = And(*[Not(variables[i]) for i in range(len_var-1)] + [(Not(variables[-1]))])
	trans = And(*[l16p == And(True),
				l18p == i8,
				l20p == i10,
				l22p == i4,
				l24p == i12,
				l26p == i14,
				l28p == i6,
				l30p == i2,
				l32p == Not(a212)
			])
	post = Not(a216)

	# print init
	# print trans
	# print post

	return (primary_inputs, variables, primes, init, trans, post)

tests = {'MutualExclusive':MutualExclusive,}

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