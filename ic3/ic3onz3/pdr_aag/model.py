import getopt
import sys
import re
import os
from z3 import *
from pprint import pprint

class Header():
	def __init__(self, max_idx, nin, nlatch, nout, nand, 
		nbad):
		self.max_var_index = max_idx
		self.inputs = nin
		self.latches = nlatch
		self.outputs = nout
		self.ands = nand
		self.bads = nbad


class Latch():
	def __init__(self, _var, _next, _init):
		self.var = _var
		self.next = _next
		self.init = _init

	def __repr__(self):
		return str(self.var) + ', ' \
			+ str(self.next) + ', ' \
			+ str(self.init)

class AND():
	def __init__(self, _lhs, _rhs0, _rhs1):
		self.lhs = _lhs
		self.rhs0 = _rhs0
		self.rhs1 = _rhs1

	def __repr__(self):
		return str(self.lhs) + ', ' \
			+ str(self.rhs0) + ', ' \
			+ str(self.rhs1)


def read_in(filename):
	inputs = list()
	outputs = list()
	bads = list()
	latches = list()
	ands = list()
	
	HEADER_PATTERN = re.compile(ur"aag (\d+) (\d+) (\d+) (\d+) (\d+)(?: (\d+))?\n")
	IO_PATTERN = re.compile(ur"(\d+)\n")
	LATCH_PATTERN = re.compile(ur"(\d+) (\d+)(?: (\d+))?\n")
	AND_PATTERN = re.compile(ur"(\d+) (\d+) (\d+)\n")

	with open(filename, 'r') as f:
		first_line = f.readline()
		cont = re.match(HEADER_PATTERN, first_line)
		if cont == None:
			print "Don't support constraint, fairness, justice property yet"
			os._exit(1)
		
		header = Header(
				int(cont.group(1)),
				int(cont.group(2)),
				int(cont.group(3)),
				int(cont.group(4)),
				int(cont.group(5)),
				int(cont.group(6)) if cont.group(6) != None else 0
			)
		
		input_num = header.inputs
		output_num = header.outputs
		bad_num = header.bads
		latch_num = header.latches
		and_num = header.ands

		for line in f.readlines():
			if input_num>0 :
				h = re.match(IO_PATTERN, line)
				if h:
					# print "input nodes"
					inputs.append(h.group(1))
					input_num -= 1
			elif latch_num > 0:
				h = re.match(LATCH_PATTERN, line)
				if h:
					if h.group(3) == None:
						# print h.groups()
						latches.append(Latch(h.group(1), h.group(2), "0"))
					else:
						# print "I ain't getting in"
						latches.append(Latch(h.group(1), h.group(2), h.group(3)))
					# print line.strip()
					# print "latches"
					latch_num -= 1
			elif output_num	> 0:
				h = re.match(IO_PATTERN, line)
				if h:
					# print "output nodes"
					outputs.append(h.group(1))
					output_num -= 1
			elif bad_num > 0:
				h = re.match(IO_PATTERN, line)
				if h:
					# print "bad nodes"
					bads.append(h.group(1))
					bad_num -= 1
			elif and_num > 0:
				h = re.match(AND_PATTERN, line)
				if h:
					ands.append(AND(h.group(1), h.group(2), h.group(3)))
					# print line.strip()
					# print h.group(1), h.group(2), h.group(3)
					and_num -= 1

			# exit()
		return (inputs, outputs, bads, latches, ands)
			

class Model(object):
	"""transition model"""
	def __init__(self):
		self.inputs = []
		self.vars = []
		self.primed_vars = []
		self.trans = True
		self.init = True
		self.post = True

	def parse(self, filename):
		i, o, b, l, a = read_in(filename)
		# pprint(i)
		# pprint(l)
		# pprint(a)
		# pprint(b)

		inp = dict()  # string of primary input ==> primary input boolean variables
		self.inputs = list()
		for it in i:
			inp[it] = Bool("i" + it)
			self.inputs.append(inp[it])
		# pprint(self.inputs) 

		vs = dict()  # string of state variables ==> state boolean variables
		self.vars = list()
		for it in l:
			vs[it.var] = Bool("v" + it.var)
			self.vars.append(vs[it.var])
		# pprint(self.vars)

		pvs = dict()  # string of state variables ==> primed state boolean variables
		self.primed_vars = list()
		for it in l:
			pvs[it.var] = Bool("v" + it.var + '\'')
			self.primed_vars.append(pvs[it.var])
		# pprint(self.primed_vars)

		ands = dict()  # string of AND definition ==> AND boolean expression
		for it in a:
			# flag = 1
			rs0 = True
			rs1 = True
			if it.rhs0 == "1":
				rs0 = True
			elif it.rhs0 == "0":
				rs0 = False
			elif int(it.rhs0) & 1 != 0:  # odd number
				# print it.rhs0
				v = str( int(it.rhs0) - 1 )
				if v in inp.keys():
					rs0 = Not(inp[v])
				elif v in vs.keys():
					rs0 = Not(vs[v])
				elif v in ands.keys():
					rs0 = Not(ands[v])
				else:
					print "Error in AND definition"
					os._exit(1)
			else: 
				# print it.rhs0 
				v = it.rhs0
				if v in inp.keys():
					rs0 = inp[v]
				elif v in vs.keys():
					rs0 = vs[v]
				elif v in ands.keys():
					rs0 = ands[v]
				else:
					print "Error in AND definition"
					os._exit(1)

			if it.rhs1 == "1":
				rs1 = True
			elif it.rhs1 == "0":
				rs1 = False
			elif int(it.rhs1) & 1 != 0:  # odd number
				v = str(int(it.rhs1) - 1)
				if v in inp.keys():
					rs1 = Not(inp[v])
				elif v in vs.keys():
					rs1 = Not(vs[v])
				elif v in ands.keys():
					rs1 = Not(ands[v])
				else:
					print "Error in AND definition"
					os._exit(1)
			else: 
				v = it.rhs1
				if v in inp.keys():
					rs1 = inp[v]
				elif v in vs.keys():
					rs1 = vs[v]
				elif v in ands.keys():
					rs1 = ands[v]
				else:
					print "Error in AND definition"
					os._exit(1)

			ands[it.lhs] = And(rs0, rs1)
			# print ands[it.lhs]
		# pprint(ands.keys())
		# pprint(len(ands.keys()))

		# initial condition
		inits_var = list()
		for it in l:
			if it.init == "0":
				inits_var.append(Not(vs[it.var]))
			elif it.init == "1":
				inits_var.append(vs[it.var])
		self.init = And(inits_var)
		# print self.init

		# transition relation
		trans_items = list()
		for it in l:
			if it.next == "1":
				trans_items.append(pvs[it.var] == And(True) )
			elif it.next == "0":
				trans_items.append(pvs[it.var] == And(False))
			elif int(it.next) & 1 == 0:  # even number
				v = it.next
				if v in inp.keys():
					trans_items.append(pvs[it.var] == inp[v])
				elif v in vs.keys():
					trans_items.append(pvs[it.var] == vs[v])
				elif v in ands.keys():
					trans_items.append(pvs[it.var] == ands[v])
				else:
					print "Error in transition relation"
					os._exit(1)
			else:
				v = str( int(it.next) - 1)
				if v in inp.keys():
					trans_items.append(pvs[it.var] == Not(inp[v]))
				elif v in vs.keys():
					trans_items.append(pvs[it.var] == Not(vs[v]))
				elif v in ands.keys():
					trans_items.append(pvs[it.var] == Not(ands[v]))
				else:
					print "Error in transition relation"
					os._exit(1)
		self.trans = simplify(And(trans_items))
		# self.trans = And(trans_items)
		# print self.trans

		# postualte
		bad_var = None
		if len(o) < 1:
			if len(b) == 0:
				print "Din't specify a property"
				os._exit(1)
			elif len(b)>1:
				print "Sorry, only handle one property"
				os._exit(1)
			else:
				bad_var = b[0]
		else:
			print "Consider the output as bad property"
			bad_var = o[0]
		# print bad_var
		if bad_var != None:
			tmp = int(bad_var)
			if  tmp & 1 == 0:  # even number
				if bad_var in inp.keys():
					self.post = Not(inp[bad_var])
				elif bad_var in vs.keys():
					self.post = Not(vs[bad_var])
				elif bad_var in ands.keys():
					self.post = Not(ands[bad_var])
				else:
					print "Error in property definition"
					os._exit(1)
			else:
				bad_var = str(tmp -1)
				if bad_var in inp.keys():
					self.post = inp[bad_var]
				elif bad_var in vs.keys():
					self.post = vs[bad_var]
				elif bad_var in ands.keys():
					self.post = ands[bad_var]
				else:
					print "Error in property definition"
					os._exit(1)
			# print self.post

		return (self.inputs, self.vars, self.primed_vars, self.init, self.trans, self.post)		



								




if __name__ == '__main__':
	help_info = "Usage: python model.py [-i <input-file>|-h|-v]" 
	try:
		opts, arg = getopt.getopt(sys.argv[1:], '-h-i:-v', ['help', 'inputfile=', 'version'])
	except getopt.GetoptError:
		print help_info
		sys.exit(2)
	# print opts
	# print arg ['inputfile=counter.aag']
	for opt_name, opt_value in opts:
		if opt_name in ('-h', '--help'):
			print help_info
		elif opt_name in ('-v', '--version'):
			print "version 0.00.1"
			exit()
		elif opt_name in ('-i', '--ifile'):
			input_file = opt_value
			# parse(input_file)
			m = Model()
			m.parse(input_file)
			exit()
		else:
			print help_info




