#!/usr/bin/python

# Implementation of the PDR algorithm by Peter Den Hartog. Apr 28, 2016
# reference: http://z3prover.github.io/api/html/namespacez3py.html; http://theory.stanford.edu/~nikolaj/programmingz3.html#sec-cores

from z3 import *
import sys
import pprint

class Cube:
    def __init__(self, model, lMap):
        #filter out primed variables when creating cube
        # self.cubeLiterals = [lMap[str(l)] == model[l] for l in model if '\'' not in str(l)]
        self.no_primes = [l for l in model if '\'' not in str(l)]
        self.cubes = [lMap[str(l)] if model[l]==True else Not(lMap[str(l)]) for l in self.no_primes]
    # return the conjection of all literals in this cube
    def cube(self):
        return And(*self.cubes)
    def __repr__(self):
        return str(sorted(self.cubes, key=str)) 


class PDR(object):
    def __init__(self, literals, primes, init, trans, post):
        self.init = init
        self.trans = trans
        self.literals = literals
        self.lMap = {str(l):l for l in self.literals}
        self.post = post
        self.F = []
        self.primeMap = zip(literals, primes)

    def run(self):
        if self.violateInit():
            print "violation in the initial state:   " + str(self.init)
            return False
        self.F = list()
        self.F.append(self.init)
        self.F.append(True)
        self.k = 1

        while True :
            # blocking phase
            while True:
                # if F[k]/\!P is sat, then assign c to the cube extracted from the model
                # else c is None and break the while loop
                # print "the formula is:   ",And(self.F[self.k], Not(self.post))
                # print "the formula in blocking    to check: ", And(self.F[self.k], Not(self.post))
                c = self.is_sat(And(self.F[self.k], Not(self.post)))
                if c!=None :
                    # print "ther return cube:    ",c.cube()
                    if not self.recBlock(c, self.k):
                        print "Didn't find inductive invariants"
                        return False
                else:
                    break

            #propagation phase
            self.k += 1
            self.F.append(True)
            for i in range(1, self.k):  # from 1 to k-1
                for clause in self.clauses(self.F[i]):
                    # if F[i]/\c/\T/\!c' is not sat( equally F/\c/\T => c' is sat )
                    # then c is inductive relative to the F[i]
                    # then propagate c to the F[i+1]
                    # print clause
                    # print "the formula in propagation to check: ", And(self.F[i], clause, self.trans, Not(substitute(clause, self.primeMap)))
                    if None==self.is_sat(And(self.F[i], clause, self.trans, Not(substitute(clause, self.primeMap)))):
                        # print And(self.F[i], clause, self.trans, Not(substitute(clause, self.primeMap)))
                        # print "Propogating"
                        # print "add clause " + str(clause) + " to Frame " + str(i+1)
                        self.F[i+1] = And(self.F[i+1], clause)
                # print "-----Frames------"
                # for item in self.F:
                #     print item
                # print "-----------------"
                # if is_eq(self.F[i]==self.F[i+1]):
                #     print "the indcutive invariant is: ", simplify(self.F[i])
                #     return True

                inv = self.checkFixedpoint(self.F[i], self.F[i+1])
                if inv!=None :
                    print "the inductive invariant is:  ", simplify(inv)
                    return True
    def recBlock(self, s, i):
        if i == 0:
            return False
        while True:
            # if F[i-1]/\!s/\T/\s' is sat( equally F[i-1]/\!s/\T => !s' is not sat)
            # then extract a cube c from the model
            # else c is None, then break the while loop
            # print "the formula tested in reckBlock: " + str(And(self.F[i-1], Not(s.cube())  , self.trans, substitute(s.cube(),self.primeMap)))
            # print "the formula in recblock    to check: ", And(self.F[i-1], Not(s.cube())  , self.trans, substitute(s.cube(),self.primeMap))
            c = self.is_sat(And(self.F[i-1], Not(s.cube())  , self.trans, substitute(s.cube(),self.primeMap)))
            # print "at " + str(i) + " c is None ?  " + str(c==None)
            if c!=None:
                # print "the cube to be blocked: " + str(c.cube())
                if not self.recBlock(c, i-1):
                    return False
            else:
                break
        # g = self.generalize(Not(s.cube()), i)
        for j in range(1, i+1):  # from 1 to i
            # print "add cube " + str(Not(s.cube())) + " to Frame " + str(j)
            self.F[j] = And(self.F[j], Not(s.cube()))
        return True

    def clauses(self, formula):
        #  from https://stackoverflow.com/a/18003288/1911064
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
   
    def violateInit(self):
        # print "the formula in violateInit to check: ", And(self.init, Not(self.post))
        if None==self.is_sat(And(self.init, Not(self.post))):
            return False
        else:
            return True


    def is_sat(self, formula):
        # print ("--- called by function      ", sys._getframe().f_back.f_code.co_name)
        # print ("--- called at line          ", sys._getframe().f_back.f_lineno)
        s = Solver()
        # print id(s)
        s.add(And(formula))
        # print s
        if s.check() == sat:
            c = Cube(s.model(), self.lMap)
            # print c
            # s.reset()
            return c
        else:
            # s.reset()
            return None

    def equiv(self, claim):
        s = Solver()
        s.add(Not(claim))
        r = s.check()
        if r == unsat:
            return True
        else:
            return False