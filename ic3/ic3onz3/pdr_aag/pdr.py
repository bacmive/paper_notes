from z3 import *
import sys
import os
import pprint
from random import choice
import heapq
from pprint import pprint


class Cube:
	def __init__(self):
		self.literals = []

	def from_model(self, model, lMap, primary_inputs):
		no_primes = [l for l in model if '\'' not in str(l)]
		no_inputs = [l for l in no_primes if 'i' not in str(l)]
		self.literals = [lMap[str(lit)] if model[lit] == True else Not(
			lMap[str(lit)]) for lit in no_inputs]
		return self

	def from_list(self, lits):
		self.literals = lits[:]
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
	def __init__(self, primary_inputs, literals, primes, init, trans, post):
		self.primary_inputs = primary_inputs
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
		self.F.append(set([self.init]))
		self.F.append(set([]))
		self.k = 1
		while True:
			s1 = Solver()
			while True:
				s1.add(And(And(list(self.F[self.k])), Not(self.post)))
				if s1.check() == sat:
					c = Cube().from_model(s1.model(), self.lMap, self.primary_inputs)
					s1.reset()
					if not self.recBlock(c, self.k):
						print "Din't find invariants\n"
						return False
				else:
					s1.reset()
					break
			self.k += 1
			self.F.append(set([]))
			s2 = Solver()
			for i in range(1, self.k):
				for clause in self.F[i]:
					# s2.add(And(And(list(self.F[i])), clause, self.trans, Not(substitute(clause, self.primeMap))))
					s2.add(And(And(list(self.F[i])), self.trans, Not(substitute(clause, self.primeMap))))
					if s2.check() == unsat and clause not in self.F[i+1]:
						self.F[i + 1].add(clause)
					s2.reset()
				inv = self.checkFixedpoint(i, i+1)
				if inv != None:
					print "the inductive invariant is:  ", simplify(inv)
					self.checkForInvariant(simplify(inv))
					return True
	
	def recBlock(self, s, i):
		obligations = []
		obligations.append((i, s))
		heapq.heapify(obligations)
		s3 = Solver()
		while len(obligations) > 0:
			j, sp = heapq.heappop(obligations)
			if j == 0:
				return False
			s3.add(And(And(list(self.F[j-1])), Not(sp.cube()), self.trans, substitute(sp.cube(), self.primeMap)))
			if s3.check() == sat:
				c = Cube().from_model(s3.model(), self.lMap, self.primary_inputs)
				heapq.heappush(obligations, (j, sp))
				heapq.heappush(obligations, (j-1, c))   
			else:
				g = self.generalize(sp, j)
				for t in range(1, j+1):
					self.F[t].add(Not(g.cube()))
			s3.reset()
		return True
	
	def checkFixedpoint(self, i, j):
		if not (self.F[i] - self.F[j]):
			return And(list(self.F[i]))
		return None
	
	def checkForInvariant(self, inv):
		c1 =Solver()
		c1.add(And(self.init, Not(inv)))
		c2 = Solver()
		c2.add(And(inv, self.trans, Not(substitute(inv, self.primeMap))))
		c3 = Solver()
		c3.add(And(inv, Not(self.post)))
		if not c1.check()==sat and not c2.check()==sat and not c3.check()==sat:
			print "find the reliable invariant"
		else:
			print "sorry, try again"
	
	def generalize(self, s, i):
		c = s.get_literals()
		for lit in s.get_literals():
			tryc = c[:]
			tryc.remove(lit)
			s1 = Solver()
			s2 = Solver()
			s1.add(And(self.init, And(tryc)))
			s2.add(And(And(list(self.F[i-1])), self.trans, Not(And(tryc)), substitute(And(tryc), self.primeMap)))
			if not s1.check() == sat and not s2.check() == sat:
				c = tryc[:]
		return Cube().from_list(c)
	
	def violateInit(self):
		s = Solver()
		s.add(And(self.init, Not(self.post)))
		if s.check() == sat:
			return True
		else:
			return False
