#!/usr/bin/python

# Implementation of the PDR algorithm by Peter Den Hartog. Apr 28, 2016

from z3 import *

class Cube:
    def __init__(self, model, lMap):
        #filter out primed variables when creating cube
        self.cubeLiterals = [lMap[str(l)] == model[l] for l in model if '\'' not in str(l)]
    # return the conjection of all literals in this cube
    def cube(self):
        return And(*self.cubeLiterals)
    def __repr__(self):
        return str(sorted(self.cubeLiterals, key=str)) 


class PDR(object):
    def __init__(self, literals, primes, init, trans, post):
        self.init = init
        self.trans = trans
        self.literals = literals
        self.lMap = {str(l):l for l in self.literals}
        self.post = post
        self.F = []
        self.primeMap = zip(literals, primes)

    def Fs(self, k):
        return And(self.F[k])

    def run(self):
        if self.violateInit():
            print "violation in the initial state:   " + str(self.init)
            return False
        self.F = list()
        self.F.append([self.init])
        self.F.append([True])
        self.k = 1

        while True :
            # blocking phase
            while True:
                # if F[k]/\!P is sat, then assign c to the cube extracted from the model
                # else c is None and break the while loop
                c = self.is_sat(And(self.Fs(self.k), Not(self.post)))
                if c!=None :
                    if not self.recBlock(c, self.k):
                        print "Didn't find inductive invariants"
                        return False
                else:
                    break

            #propagation phase
            self.k += 1
            self.F.append([True])
            for i in range(1, self.k):  # from 1 to k-1
                for clause in self.F[i]:
                    # if F[i]/\c/\T/\!c' is not sat( equally F/\c/\T => c' is sat )
                    # then c is inductive relative to the F[i]
                    # then propagate c to the F[i+1]
                    if None==self.is_sat(And(self.Fs(i), And(clause), self.trans, Not(substitute(And(clause), self.primeMap)))):
                        self.F[i+1].append(clause)
                if is_eq(self.Fs(i)==self.Fs(i+1)):
                    print "the inductive invariant is:  ", simplify((self.Fs(i)))
                    return True

    def recBlock(self, s, i):
        if i == 0:
            return False
        while True:
            # if F[i-1]/\!s/\T/\s' is sat( equally F[i-1]/\!s/\T => !s' is not sat)
            # then extract a cube c from the model
            # else c is None, then break the while loop
            c = self.is_sat(And(self.Fs(i-1), Not(s.cube()), self.trans, substitute(s.cube(),self.primeMap)))
            # print "at " + str(i) + " c is None ?  " + str(c==None)
            if c!=None:
                if not recBlock(c, i-1):
                    return False
            else:
                break
        # g = self.generalize(Not(s.cube()), i)
        for j in range(1, i+1):  # from 1 to i
            self.F[j].append(Not(s.cube()))
        return True
   
    def violateInit(self):
        if None==self.is_sat(And(self.init, Not(self.post))):
            return False
        else:
            return True


    def is_sat(self, formula):
        s = Solver()
        s.add(formula)
        if s.check() == sat:
            return Cube(s.model(), self.lMap)
        else:
            return None

