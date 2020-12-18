#!/usr/bin/python

# Implementation of the PDR algorithm by Peter Den Hartog. Apr 28, 2016
# reference: http://z3prover.github.io/api/html/namespacez3py.html;
# http://theory.stanford.edu/~nikolaj/programmingz3.html#sec-cores

from z3 import *
import sys
import os
import pprint
from copy import deepcopy
from random import choice
import heapq
# class Cube:
#     def __init__(self, model, lMap):
#         #filter out primed variables when creating cube
#         # self.cubeLiterals = [lMap[str(l)] == model[l] for l in model if '\'' not in str(l)]
#         self.no_primes = [l for l in model if '\'' not in str(l)]
#         self.cubes = [lMap[str(l)] if model[l]==True else Not(lMap[str(l)]) for l in self.no_primes]
#     # return the conjection of all literals in this cube
#     def cube(self):
#         return And(*self.cubes)
#     def __repr__(self):
#         return str(sorted(self.cubes, key=str))


class Cube:
	def __init__(self):
		self.literals = []

	# return the conjection of all literals in this cube
	def from_model(self, model, lMap):
		no_primes = [l for l in model if '\'' not in str(l)]
		self.literals = [lMap[str(l)] if model[l] == True else Not(lMap[str(l)]) for l in no_primes]
		return self

	def from_list(self, lits):
		self.literals = lits
		return self

	def cube(self):
		if not (self.literals):
			return And(True)
		return And(*self.literals)

	def get_literals(self):
		return self.literals

	def __repr__(self):
		return str(sorted(self.literals, key=str))


class PDR(object):
	def __init__(self, literals, primes, init, trans, post):
		self.init = init
		self.trans = trans
		self.literals = literals
		self.lMap = {str(l): l for l in self.literals}
		self.post = post
		self.F = []
		self.primeMap = zip(literals, primes)
		self.toNoPrimes = zip(primes, literals)
		self.max_iter = 4

	def run(self):
		if self.violateInit():
			print "violation in the initial state:   " + str(self.init)
			return False
		self.F = list()
		self.F.append(self.init)
		self.F.append(True)
		# print self.F
		# os._exit(1)
		self.k = 1

		while True:
			# blocking phase
			s1 = Solver()
			while True:
				# if F[k]/\!P is sat, then assign c to the cube extracted from the model
				# else c is None and break the while loop
				# print "the formula is:   ",And(self.F[self.k], Not(self.post))
				# print "the formula in blocking to check: ", And(self.F[self.k],
				# Not(self.post))
				s1.add(And(self.F[self.k], Not(self.post)))
				if s1.check() == sat:
					c = Cube().from_model(s1.model(), self.lMap)
					s1.reset()
					if not self.recBlock(c, self.k):
						print "Didn't find inductive invariants"
						return False
				else:
					s1.reset()
					break

			# propagation phase
			self.k += 1
			self.F.append(True)
			s2 = Solver()
			for i in range(1, self.k):  # from 1 to k-1
				for clause in self.get_clauses(self.F[i]):
					# if F[i]/\c/\T/\!c' is not sat( equally F/\c/\T => c' is sat )
					# then c is inductive relative to the F[i]
					# then propagate c to the F[i+1]
					# print clause
					# print "the formula in propagation to check: ",
					# And(self.F[i], clause, self.trans, Not(substitute(clause,
					# self.primeMap)))
					s2.add(And(self.F[i], clause, self.trans,
						   Not(substitute(clause, self.primeMap))))
					if s2.check() == unsat:
						# print And(self.F[i], clause, self.trans, Not(substitute(clause, self.primeMap)))
						# print "Propogating"
						# print "add clause " + str(clause) + " to Frame " +
						# str(i+1)
						self.F[i + 1] = And(self.F[i + 1], clause)
					s2.reset()
				# print "-----Frames------"
				# for item in self.F:
				#     print item
				# print "-----------------"
				# if is_eq(self.F[i]==self.F[i+1]):
				#     print "the indcutive invariant is: ", simplify(self.F[i])
				#     return True

				inv = self.checkFixedpoint(self.F[i], self.F[i + 1])
				if inv != None:
					print "the inductive invariant is:  ", simplify(inv)
					return True

	# def recBlock(self, s, i):
	#     if i == 0:
	#         return False
	#     while True:
	#         # if F[i-1]/\!s/\T/\s' is sat( equally F[i-1]/\!s/\T => !s' is not sat)
	#         # then extract a cube c from the model
	#         # else c is None, then break the while loop
	#         # print "the formula tested in reckBlock: " + str(And(self.F[i-1], Not(s.cube())  , self.trans, substitute(s.cube(),self.primeMap)))
	#         # print "the formula in recblock    to check: ", And(self.F[i-1], Not(s.cube())  , self.trans, substitute(s.cube(),self.primeMap))
	#         c = self.is_sat(And(self.F[i-1], Not(s.cube())  , self.trans, substitute(s.cube(),self.primeMap)))
	#         # print "at " + str(i) + " c is None ?  " + str(c==None)
	#         if isinstance(c,Cube):
	#             # print "the cube to be blocked: " + str(c.cube())
	#             if not self.recBlock(c, i-1):
	#                 return False
	#         else:
	#             break
	#     g = self.generalize(s, i)
	#     # print "after generalize: ", g
	#     for j in range(1, i+1):  # from 1 to i
	#         # print "add cube " + str(Not(s.cube())) + " to Frame " + str(j)
	#         self.F[j] = And(self.F[j], Not(g.cube()))
	#     return True

	def recBlock(self, s, i):
		obligations = []
		obligations.append((i, s))
		heapq.heapify(obligations)

		s3 = Solver()
		while len(obligations) != 0:
			j, sp = heapq.heappop(obligations)
			if j == 0:
				return False

			s3.add(And(self.F[j - 1], Not(sp.cube()), self.trans,
				substitute(sp.cube(), self.primeMap)))

			if s3.check() == sat:
				new_cube = Cube().from_model(s3.model(), self.lMap)
				heapq.heappush(obligations, (j, sp))
				heapq.heappush(obligations, (j-1, new_cube))	
			else:
				# print "the obligations: ", obligations
				g = self.generalize(sp, j)
				for k in range(1, j+1):
					self.F[k] = And(self.F[k], Not(sp.cube()))
			s3.reset()
		return True


	def get_clauses(self, formula):
		# from https://stackoverflow.com/a/18003288/1911064
		# from https://stackoverflow.com/questions/65047040/how-to-get-every-clauses-of-a-cnf-formula-in-z3?noredirect=1&lq=1
		g = Goal()
		g.add(formula)
		# use describe_tactics() to get to know the tactics available
		t = Tactic('tseitin-cnf')
		clauses = t(g)
		return clauses[0]



	# Check all images in F to see if one is inductive  
	def checkFixedpoint(self, formula1, formula2):
		s = Solver()
		f1 = And(formula1)
		f2 = And(formula2)
		# print "check f1: " + str(f1) + " and f2: " + str(f2)
		s.add(self.trans)
		s.add(f1)
		s.add(Not(substitute(f2), self.primeMap))
		if s.check() == unsat and self.equiv(f1==f2):
			# print s.check() == unsat
			# print is_eq(f1==f2)
			return f1
		# for frame in self.F:
		#     s=Solver()
		#     s.add(self.trans)
		#     s.add(And(frame))
		#     s.add(Not(substitute(And(frame), self.primeMap)))
		#     if s.check() == unsat:
		#         return And(frame)
		return None
	

	# "Efficient implementation of property directed reachability"
	# Iterative inductive geralization algorithm(max_iter is configuration parameter)
	def generalize(self, c, i):
		c = c.get_literals()
		s4 = Solver()
		s5 = Solver()
		s6 = Solver()
		for r in range(1, self.max_iter):
			for l in c:
				g = deepcopy(c)
				g.remove(l)
				s4.add(And(self.init, And(*g)))
				s5.add(And(self.F[i],self.trans, Not(And(*g))))
				if s4.check() == unsat and s5.check([substitute(l, self.primeMap) for l in g]) == unsat:
					induc_check = s5.unsat_core()
					s4.reset()
					s5.reset()
					cc = [substitute(l, self.toNoPrimes) for l in list(induc_check)]

					while True:
						s6.add(And(And(*cc), self.init))
						if s6.check() == sat:
							diff = list(set(g).difference(set(cc)))
							if len(diff) != 0:
								lit = choice()
								if lit not in cc:
									cc.append(lit)
							s6.reset()
						else:
							s6.reset()
							break
					return Cube().from_list(cc)
		return Cube().from_list(c)

	
	# "Better Generalization in IC3"
	# IC3 generalization procedure
	# def generalize(self, q, i):
	# 	def down(qhat, i):
	# 		while 1==1:
	# 			init_check = self.is_sat(And(self.init, And(*qhat)))
	# 			if isinstance(init_check, Cube):
	# 				# print "to be False ~"
	# 				return False;

	# 			cons_check = self.is_sat(And(self.F[i],Not(And(*qhat)), self.trans, substitute(And(*qhat), self.primeMap)))
	# 			if not isinstance(cons_check, Cube):
	# 				# print "to be True!"
	# 				return True
	# 			else:
	# 				s = cons_check.get_literals()
	# 				qhat[:] = list(set(s) & set(qhat))
	# 				# print "update qhat in down: ", qhat

	# 	q = q.get_literals()
	# 	k = 0
	# 	# print "initial q: ", q
	# 	for l in q:
	# 		qhat = deepcopy(q)
	# 		if l in qhat:
	# 			qhat.remove(l)
	# 		else:
	# 			continue
	# 		# print "after deleting literal " + str(l) + ", the remaining is: " + str(qhat)
	# 		if down(qhat, i):
	# 			q = deepcopy(qhat)
	# 			k += 1
	# 			# print "after %d down: "%k +str(q)
	# 	return Cube().from_list(q)


	def violateInit(self):
		# print "the formula in violateInit to check: ", And(self.init, Not(self.post))
		s = Solver()
		s.add(And(self.init, Not(self.post)))
		if s.check() == sat:
			return True
		else:
			return False

	def equiv(self, claim):
		s = Solver()
		s.add(Not(claim))
		r = s.check()
		if r == unsat:
			return True
		else:
			return False
