from z3 import *
from pprint import pprint
from copy import deepcopy
import heapq
import random
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
toLiterals = zip(primes, variables)
lMap = {str(l):l for l in variables}

model = And((post), True)
s = Solver()
s.add (model)
# print str(init)
if(s.check() == sat):
	# print s
	m = s.model()
	# print m
	# for l in m:
	# 	print l
	cubeLiterals = [lMap[str(l)] == m[l] for l in m if '\'' not in str(l)]
	no_primes = [l for l in m if '\'' not in str(l)]
	cubes = [lMap[str(l)] if m[l]==True else Not(lMap[str(l)]) for l in no_primes]

	# pprint(cubeLiterals)
	# pprint(cubes)
	# for lit in cubes:
		# print substitute(substitute(lit, primeMap), toLiterals)
	# pprint(And(*cubeLiterals))
	# pprint(And(*cubes))



# class Cube:
#     def __init__(self):
#         self.literals = []     
    
#     def from_model(self, model, lMap):
#         no_primes = [l for l in model if '\'' not in str(l)]
#         self.literals = [lMap[str(l)] if model[l]==True else Not(lMap[str(l)]) for l in no_primes]
#         return self

#     def from_list(self, lits):
#         self.literals = lits
#         return self
    
#     def cube(self):
#         if not (self.literals):
#             return And(True)
#         return And(*self.literals)
    
#     def get_literals(self):
#         return self.literals

#     def __repr__(self):
#         return str(sorted(self.literals, key=str)) 

# def is_sat(formula, assumption=[]):
#     s = Solver()
#     s.add(And(formula))
#     if s.check(assumption) == sat:
#         c = Cube().from_model(s.model(), lMap)
#         return c
#     else:
#         return s.unsat_core()

# def generalize(q):
# 	def down(qhat):
# 		while 1==1:
# 			init_check = is_sat(And(init, And(*qhat)))
# 			if not isinstance(init_check, Cube):
# 				return False;

# 			cons_check = is_sat(And(post,Not(And(*qhat)), trans, substitute(And(*qhat), primeMap)))
# 			if not isinstance(cons_check, Cube):
# 				return True
# 			else:
# 				s = cons_check.get_literals()
# 				qhat = list(set(s) & set(qhat))
# 				print "update qhat in down: ", qhat

# 	q = q.get_literals()
# 	print "initial q: ", q
# 	k = 0
# 	for l in q:
# 		qhat = deepcopy(q)
# 		qhat.remove(l)
# 		if down(qhat):
# 			q = deepcopy(qhat)
# 			k += 1
# 			print "after %d down: "%k +str(q)

# 	return Cube().from_list(q)

# print generalize(Cube().from_list([variables[0], Not(variables[1])]))





# heapq
mylist = zip(list(random.sample(range(100), 10)), [i for i in range(10)])
# k = 3
# largest = heapq.nlargest(k, mylist, key=lambda x:x[1])
# smallest = heapq.nsmallest(k, mylist,key=lambda x:x[1])
# print largest
# print smallest
pprint(mylist)
heapq.heapify(mylist)
heapq.heappop(mylist)
pprint(mylist)
print "the minimum is: ", min(mylist)
ob = [(1,"1212"), (2,"#423")]
print min(ob)









# def d(a,i):
# 	a[:] = [l for l in range(5,19)]
# 	return True
# def wrapper():
# 	c = [1,3,4,5,6,7,14]
# 	cp = deepcopy(c)
# 	cp.remove(1)
# 	if d(cp, 3):
# 		c = deepcopy(cp)
# 		print c
# wrapper()
# li = list(set(c)&set(cc))




# def recur(k):
# 	def inner(i):
# 		return i+1;
# 	res = 0
# 	for i in range(8):
# 		res += inner(i)
# 	return res
# print recur(7)






# s.check(variables)
# core = s.unsat_core()
# core = list(core)
# print core





# print prove(post == init)
# print prove(post == And(True))
# print is_eq(post == And(True))




# def clauses(formula):
#     #  from https://stackoverflow.com/a/18003288/1911064
#     g = Goal()
#     g.add(formula)
#     # use describe_tactics() to get to know the tactics available
#     t = Tactic('tseitin-cnf')
#     clauses = t(g)
#     return clauses[0]

# cls = clauses(And(True))
# print "the clauses in True( " + str(And(True))  + " )is: "
# for c in cls:
# 	print c






# class Cube:
#     def __init__(self, model, lMap):
#         #filter out primed variables when creating cube
#         self.cubeLiterals = [lMap[str(l)] == model[l] for l in model if '\'' not in str(l)]
#     # return the conjection of all literals in this cube
#     def cube(self):
#         return And(*self.cubeLiterals)
#     def __repr__(self):
#         return str(sorted(self.cubeLiterals, key=str)) 


# def is_sat(formula):
#         s = Solver()
#         s.add(formula)
#         if s.check() == sat:
#             return Cube(s.model(), lMap)
#         else:
#             return None

# # print substitute(is_sat(model).cube(), primeMap)

# s = is_sat(model).cube()
# print is_sat(And(init, Not(s), trans, substitute(s, primeMap))) # None
# print is_sat(And(And(True, Not(s)), And(Not(s)), trans, Not(substitute(And(Not(s)), primeMap))))
# print is_sat(And(And(True, Not(s)), And(True), trans, Not(substitute(And(True), primeMap))))


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