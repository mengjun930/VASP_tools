#print the number of atoms whose z coordinate is listed in fix_list

import re

dir = 'nonperodic.xyz'
fix_list = ['0.000000', '.878000', '1.475000', '2.353000', '0.738000', '1.616000']

ln = 0
fix_num = 0
with open(dir, mode = 'r') as fp:
	for line in fp:
		ln += 1
		for fix_coor in fix_list:
			if re.search(fix_coor, line.split()[-1]):
				# print (ln, end = ' ')
				print ln, 
				fix_num += 1
				continue
print '\natoms fixed: ' + str(fix_num)