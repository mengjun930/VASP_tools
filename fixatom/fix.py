import numpy as np
import os

def get_vaspfile(infile):
    if infile != '':
        return infile
    filename_list = os.listdir('./')
    for filename in filename_list:
        if '.vasp' in filename:
            return filename

if __name__ == '__main__':
    input_file = ''
    input_file = get_vaspfile(input_file)
    fp = open(input_file , 'r')
    fp_fix = open('POSCAR' , 'w')
    fix_list = ['0.021690000', '0.069660001']
    a=0
    b=0
    for line in fp:
        if b<8:
            fp_fix.write(line)
        else:
            fp_fix.write(line.rstrip())
            z=line.split()[2]
            if z in fix_list:
                fp_fix.write(' F F F \n')
                a+=1
            else:
                fp_fix.write(' T T T \n')
        b+=1
    fp_fix.close()
    fp.close()
    print 'there are %s atoms fixed' % a