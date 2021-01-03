#!/usr/bin/python
from z3 import *
from pdr import PDR

def Test_mutual():
    i14 = Bool('i14')
    i16 = Bool('i16')
    i18 = Bool('i18')
    i22 = Bool('i22')
    i24 = Bool('i24')
    i28 = Bool('i28')
    i30 = Bool('i30')
    primary_inputs=[ i14,i16,i18,i22,i24,i28,i30 ]
    l2 = Bool('l2')
    l2p = Bool(str(l2) + '\'')
    l54 = Bool('l54')
    l54p = Bool(str(l54) + '\'')
    l56 = Bool('l56')
    l56p = Bool(str(l56) + '\'')
    l58 = Bool('l58')
    l58p = Bool(str(l58) + '\'')
    l66 = Bool('l66')
    l66p = Bool(str(l66) + '\'')
    l68 = Bool('l68')
    l68p = Bool(str(l68) + '\'')
    l70 = Bool('l70')
    l70p = Bool(str(l70) + '\'')
    l72 = Bool('l72')
    l72p = Bool(str(l72) + '\'')
    l4 = Bool('l4')
    l4p = Bool(str(l4) + '\'')
    variables=[ l2,l54,l56,l58,l66,l68,l70,l72,l4 ]
    primes=[ l2p,l54p,l56p,l58p,l66p,l68p,l70p,l72p,l4p ]
    a12 = And(i14, Not(i16))
    a10 = And(a12, Not(i18))
    a20 = And(Not(i22), Not(i24))
    a8 = And(a10, a20)
    a26 = And(Not(i28), Not(i30))
    a6 = And(a8, a26)
    a52 = And(l54, Not(l56))
    a50 = And(a52, l58)
    a64 = And(l66, Not(l68))
    a62 = And(a64, l70)
    a60 = And(a62, l72)
    a74 = And(Not(a50), Not(a60))
    a78 = And(l54, l56)
    a76 = And(a78, l58)
    a82 = And(l66, l68)
    a80 = And(a82, l70)
    a84 = And(Not(a76), Not(a80))
    a86 = And(a84, Not(l72))
    a48 = And(a74, Not(a86))
    a88 = And(i14, Not(a48))
    a90 = And(a48, Not(i14))
    a92 = And(Not(a88), Not(a90))
    a96 = And(Not(l54), Not(l56))
    a94 = And(a96, l58)
    a100 = And(a52, l72)
    a98 = And(a100, l58)
    a102 = And(Not(i22), i24)
    a106 = And(Not(l54), l56)
    a104 = And(a106, l58)
    a110 = And(l56, i24)
    a112 = And(Not(l56), Not(i24))
    a114 = And(Not(a110), Not(a112))
    a108 = And(i22, Not(a114))
    a116 = And(Not(i22), Not(a114))
    a118 = And(l54, a108)
    a120 = And(Not(l54), a116)
    a122 = And(Not(a118), Not(a120))
    a124 = And(a76, a20)
    a126 = And(Not(a76), Not(a122))
    a128 = And(Not(a124), Not(a126))
    a130 = And(a104, i24)
    a132 = And(Not(a104), Not(a128))
    a134 = And(Not(a130), Not(a132))
    a136 = And(a98, a102)
    a138 = And(Not(a98), Not(a134))
    a140 = And(Not(a136), Not(a138))
    a142 = And(a94, Not(i24))
    a144 = And(Not(a94), Not(a140))
    a146 = And(Not(a142), Not(a144))
    a46 = And(a92, Not(a146))
    a150 = And(Not(l66), Not(l68))
    a148 = And(a150, l70)
    a154 = And(a64, l72)
    a152 = And(a154, l70)
    a156 = And(Not(i28), i30)
    a160 = And(Not(l66), l68)
    a158 = And(a160, l70)
    a164 = And(l68, i30)
    a166 = And(Not(l68), Not(i30))
    a168 = And(Not(a164), Not(a166))
    a162 = And(i28, Not(a168))
    a170 = And(Not(i28), Not(a168))
    a172 = And(l66, a162)
    a174 = And(Not(l66), a170)
    a176 = And(Not(a172), Not(a174))
    a178 = And(a80, a26)
    a180 = And(Not(a80), Not(a176))
    a182 = And(Not(a178), Not(a180))
    a184 = And(a158, i30)
    a186 = And(Not(a158), Not(a182))
    a188 = And(Not(a184), Not(a186))
    a190 = And(a152, a156)
    a192 = And(Not(a152), Not(a188))
    a194 = And(Not(a190), Not(a192))
    a196 = And(a148, Not(i30))
    a198 = And(Not(a148), Not(a194))
    a200 = And(Not(a196), Not(a198))
    a44 = And(a46, Not(a200))
    a42 = And(a44, a92)
    a202 = And(i18, i16)
    a204 = And(Not(i16), Not(i18))
    a206 = And(Not(a202), Not(a204))
    a40 = And(a42, a206)
    a38 = And(a40, a206)
    a36 = And(a38, Not(a146))
    a34 = And(a36, Not(a200))
    a32 = And(l4, a34)
    a208 = And(Not(l2), a6)
    a210 = And(l2, a32)
    a212 = And(Not(a208), Not(a210))
    a214 = And(a106, a160)
    a216 = And(l4, a214)
    init = And(*[ Not(l66),Not(l54),Not(l56),Not(l58),Not(l70),Not(l68),Not(l72),Not(l4),Not(l2) ])
    trans = And(*[ l66p == i28,l54p == i22,l56p == i24,l58p == i16,l70p == i18,l68p == i30,l72p == i14,l4p == Not(a212),l2p == And(True) ])
    post = Not(a216)
    return (primary_inputs, variables, primes, init, trans, post)

tests = {'Test_mutual':Test_mutual}

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
