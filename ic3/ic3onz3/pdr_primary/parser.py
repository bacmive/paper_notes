import sys
import os
import re

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: python parser.py <input-filename>\n"
		os._exit(1)

	file = sys.argv[1]
	result = '''#!/usr/bin/python
from z3 import *
from pdr import PDR

def %s():'''%('Test_'+sys.argv[1].split('.')[0])

	len_inp = 0
	len_var = 0
	inp = list()
	var = list()
	prefix = ""
	init_map = dict()
	trans_map = dict()
	prop = ""

	with open(file) as f:
		line = f.readline()
		while line:
			# print line.strip()
			if line.find('--inputs') != -1:
				prefix = 'i'
			elif line.find('--latches') != -1:
				result += '''\n    primary_inputs=[ ''' + ','.join(inp) + ''' ]'''
				prefix = 'l'
			elif line.find('ASSIGN') !=-1 :
				tmp = map(lambda s: s+'p', var)
				result += '''\n    variables=[ ''' + ','.join(var) + ''' ]'''
				result += '''\n    primes=[ ''' + ','.join(tmp) + ''' ]'''
				prefix = 'A'
			elif line.find('--ands') != -1:
				prefix = 'a'
			elif line.find('--outputs') != -1:
				prefix = 'o'
			else:
				m_input = re.match( r'(.+)\s:\s(.+);', line.strip() )
				if prefix == 'i' and m_input:
					inp.append(m_input.group(1))
					result += '''\n    %s = Bool('%s')'''%(m_input.group(1), m_input.group(1))

				m_latch = re.match( r'(.+)\s:\s(.+);', line.strip() )
				if prefix == 'l' and m_latch:
					var.append(m_latch.group(1))
					result += '''\n    %s = Bool('%s')'''%(m_latch.group(1), m_latch.group(1))
					result += '''\n    %s = Bool(str(%s) + '\\\'')'''%(m_latch.group(1)+'p', m_latch.group(1))

				m_assign = re.match( r'(.+)\((.+)\)\s:=\s(.+);', line.strip() )
				if prefix == 'A' and m_assign:
					if m_assign.group(1) == "init":
						init_map[m_assign.group(2)] = m_assign.group(3)
					else:
						if '!' in m_assign.group(3):
							trans_map[m_assign.group(2)] = 'Not(%s)'%m_assign.group(3).replace('!', '', 1)
						elif m_assign.group(3) == 'TRUE':
							 trans_map[m_assign.group(2)] = 'True'
						elif m_assign.group(3) == 'FALSE':
							 trans_map[m_assign.group(2)] = 'False'
						else:
							trans_map[m_assign.group(2)] = m_assign.group(3)

				m_ands = re.match( r'(.+)\s:=\s(.+)\s&\s(.+);', line.strip() )
				if prefix == 'a' and m_ands:
					result += '''\n    %s = And(%s, %s)'''%(m_ands.group(1), 
															'Not(%s)'%m_ands.group(2).replace('!', "", 1) if '!' in m_ands.group(2) else m_ands.group(2),
															'Not(%s)'%m_ands.group(3).replace('!', "", 1) if '!' in m_ands.group(3) else m_ands.group(3)
															)
				m_outputs = re.match( r'(.+)\s:=\s(.+);', line.strip())
				if prefix == 'o' and m_outputs:
					if '!' in m_outputs.group(2):
						prop = '%s'%m_outputs.group(2).replace('!', '', 1)
					else:
						prop = 'Not(%s)'%m_outputs.group(2).replace('!', '', 1)

			line = f.readline()

	# initial condition
	init_list = list()
	for k in init_map.keys():
		if init_map[k] == 'FALSE':
			init_list.append( 'Not(%s)'%k )
		else:
			init_list.append( k )
	result += '''\n    init = And(*[ %s ])'''%(','.join(init_list))

	# transiton relations
	trans_list = list()

	for k in trans_map.keys():
		# print trans_map[k]
		if '!' in trans_map[k]:
			trans_list.append( '%s == Not(%s)'%(k+'p', trans_map[k].replace('!', '', 1)) )
		elif trans_map[k] == 'True':
			trans_list.append( '%s == And(True)'%(k+'p') )
		elif trans_map[k] == 'False':
			trans_list.append( '%s == And(False)'%(k+'p') )
		else:
			trans_list.append( '%s == %s'%(k+'p', trans_map[k]))
	result += '''\n    trans = And(*[ %s ])'''%( ','.join(trans_list))
	
	# postulate
	result += '''\n    post = %s'''%prop

	# return
	result += '''\n    return (primary_inputs, variables, primes, init, trans, post)'''
	# main
	result +='''

tests = {'%s':%s}

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
			solver.run()'''%('Test_'+sys.argv[1].split('.')[0],'Test_'+sys.argv[1].split('.')[0])
	print result






			
