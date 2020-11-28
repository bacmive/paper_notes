from z3 import *
from pprint import pprint
len = 2
variables = [Bool(str(i)) for i in range(len)]
primes = [Bool(str(i) + '\'') for i in variables]
init = And(*[Not(variables[i]) for i in range(len-1)] + [Not(variables[-1])])
trans = And(*[
		Or(variables[0], Not(variables[1]), primes[1]),
		Or(variables[0], variables[1], Not(primes[0])),
		Or(Not(variables[0]), primes[1]),
		Or(Not(variables[0]), Not(primes[1])),
		Or(variables[1], Not(primes[1]))
		])
post = Not(And(*[variables[0], Not(variables[1])]))
# post1 = Or(*[Not(variables[0]),variables[1]])
# if is_eq(post1==post):
	# print "yes"
primeMap = zip(variables, primes)

lMap = {str(l):l for l in variables}

model = And(Not(post), True)
s = Solver()
s.add (model)
# print str(init)
if(s.check() == sat):
	# print s
	m = s.model()
	print m
	# for l in m:
		# print l
	cubeLiterals = [lMap[str(l)] == m[l] for l in m if '\'' not in str(l)]
	# pprint(cubeLiterals)
	# pprint(And(*cubeLiterals))





class Cube:
    def __init__(self, model, lMap):
        #filter out primed variables when creating cube
        self.cubeLiterals = [lMap[str(l)] == model[l] for l in model if '\'' not in str(l)]
    # return the conjection of all literals in this cube
    def cube(self):
        return And(*self.cubeLiterals)
    def __repr__(self):
        return str(sorted(self.cubeLiterals, key=str)) 


def is_sat(formula):
        s = Solver()
        s.add(formula)
        if s.check() == sat:
            return Cube(s.model(), lMap)
        else:
            return None

# print substitute(is_sat(model).cube(), primeMap)

s = is_sat(model).cube()
# print is_sat(And(init, Not(s), trans, substitute(s, primeMap))) # None
print is_sat(And(And(True, Not(s)), And(Not(s)), trans, Not(substitute(And(Not(s)), primeMap))))
print is_sat(And(And(True, Not(s)), And(True), trans, Not(substitute(And(True), primeMap))))


# F = list()
# F.append([init])
# F.append([True, True])
# m2 = And(And(F[0]), And(F[1]))
# pprint(simplify(m2))
# pprint(simplify(And(True)))
# s.add(True)





# split clauses
# t = OrElse(Tactic('split-clause'), Tactic('skip'))
# res = t(post)
# pprint(res)




# class IC3:
# 	def run(self):
# 		self.k = 1
# 		self.k += 1

# ic3 = IC3()
# ic3.run()
# print ic3.k

# def ret():
# 	return 1+2

# while (res = ret()) != 4):
# 	print res
# 	break