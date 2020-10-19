import sys
import re

class tbl_handle(object):
	def __init__(self, file_name):
		self.file_name = file_name
	
	def stats(self):
		with open(self.file_name,'r') as f:
			for iter, line in enumerate(f.read().splitlines()):
				elems = re.split(';|-', line);
				if len(elems) > 1:
					rule = elems[0].split()[1]
					inv = elems[1].split(':')[1].strip()
					guard = elems[2].split()[1]
					relation = elems[3].split()[1]

					res = str()
					res += (str((iter+1)) + '.\ &')
					if inv == '((n[1] = C) & (n[2] = C))':
						res += 'mutualInv(1,2)\ & '
					elif inv == '((n[1] = C) & (x = TRUE))':
						res += 'invOnXC(1)\ & '
					elif inv =='((n[2] = C) & (n[1] = E))':
						res += 'aux_1(2,1)\ & '
					elif inv == '((n[1] = E) & (x = TRUE))':
						res += 'invOnXE(1)\ & '
					else:  # inv == '((n[2] = E) & (n[1] = E))'
						res += 'aux_2(2,1)\ & '

					if rule.startswith('n_T'):
						res += rule[2:]+'\ & '
					elif rule.startswith('n_C'):
						res += rule[2:]+'\ & '
					elif rule.startswith('n_E'):
						res += rule[2:]+'\ & '
					else: # rule.startswith('n_I')
						res += rule[2:]+'\ & '

					res += relation[0:len(relation)-1]+'_'+relation[len(relation)-1:]+'\ &'

					if len(elems) > 4:
						new_inv = elems[4].split(':')[1]
						if new_inv == '((n[2] = C) & (x = TRUE))':
							res += 'invOnXC(2)'
						elif new_inv == '((n[1] = C) & (x = TRUE))':
							res += 'invOnXC(1)'
						elif new_inv == '(((n[1] = C) & (n[2] = E))':
							res += 'aux_1(1,2)'
						elif new_inv == '((n[1] = E) & (x = TRUE))':
							res += 'invOnXE(1)'
						elif new_inv == '((n[1] = C) & (n[2] = C))':
							res += 'mutualInv(1,2)'
						elif new_inv == '((n[1] = C) & (x = TRUE))':
							res += 'invOnXC(1)'
						elif new_inv == '((n[1] = E) & (n[2] = E))':
							res += 'aux_2(1,2)'
						elif new_inv == '((n[1] = C) & (n[2] = E))':
							res += 'aux_1(1,2)'
						elif new_inv == '((n[2] = C) & (n[1] = E))':
							res += 'aux_1(2,1)'

					res += '\\\\'

					print(res)

if __name__ == "__main__":
	tbh = tbl_handle(sys.argv[1])
	tbh.stats()
