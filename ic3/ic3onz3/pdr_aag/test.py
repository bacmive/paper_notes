#!/usr/bin/python
from z3 import *
from pdr import PDR
from model import Model
from multiprocessing import Process
from time import sleep
import os


test_file_path = "./aag"


def test_a_file(solver):	
	solver.run()

def run_with_limited_time(func, args, kwargs,time):
	"""Runs a function with time limit

	:param func: The function to run
	:param args: The functions args, given as tuple
	:param kwargs: The functions keywords, given as dict
	:param time: The time limit in seconds
	:return: True if the function ended successfully. False if it was terminated.
	"""
	p = Process(target=func, args=args, kwargs=kwargs)
	p.start()
	p.join(time)
	if p.is_alive():
		p.terminate()
		return False
	return True




if __name__ == "__main__":
	help_info = "Usage: python test.py <file-name>.aag"
	import argparse
	parser = argparse.ArgumentParser(description="Run tests examples on the PDR algorithm")
	parser.add_argument('filename', type=str, help='The name of the test to run', default=None, nargs='?')
	parser.add_argument('-m', type=int, help='the time limitation of one test to run')
	args = parser.parse_args()
	if(args.filename!=None):
		file = args.filename
		m = Model()
		print "=========== Running test ==========="
		solver = PDR(*(m.parse(file)))
		solver.run()
	else:
		print "=======Test the ./aag directory===="
		for root, dirs, files in os.walk(test_file_path):
			for name in files:
				
				print "==============Testing " + str(name) + " ======================="
				
				m = Model()
				solver = PDR(*(m.parse(os.path.join(root, name))))
				
				if not run_with_limited_time(test_a_file, 
									  (solver, ),
									  {},
									  args.m
									  ):
					print "Time Out"
				else:
					print "Done in time"
		# print args.m





