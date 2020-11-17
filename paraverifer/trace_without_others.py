import os 
import sys
import commands
import re

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: trace_without_others filename"
		os._exit(1)
	command = "python -m trace --trace " + sys.argv[1] + "mutualEx.m > | grep -n 'modulename'"
	ret = commands.getoutput(command)
	pattern = re.compile(r'---\smodulename[:]\s(\w+)[,]')
	module_set = set()
	input_module = [(sys.argv[1]).split('.')[0]]
	if len(sys.argv) > 2:
		for md in sys.argv[2:]:
			input_module.append(md)
	other_modules = ""
	for m in pattern.finditer(ret):
		module = m.group(1)
		if module not in module_set:
			module_set.add(module)
			if module not in input_module:
				other_modules += module+','
	cmd = "python -m trace --ignore-module=" + other_modules + " --trace " + sys.argv[1]
	rets = commands.getoutput(cmd)
	print rets 
