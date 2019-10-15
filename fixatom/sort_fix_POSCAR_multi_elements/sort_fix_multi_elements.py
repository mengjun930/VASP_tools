import numpy as np
import os

def xyzsort(input_xyz, reverse_value = 1):
    for i in range(len(input_xyz)):
        input_xyz[i].reverse()
    input_xyz.sort(reverse = reverse_value)
    for i in range(len(input_xyz)):
        input_xyz[i].reverse()
    return input_xyz

def read_fix_list(filename, n):
    read_fix_list = open(filename, 'r')
    xyz = read_fix_list.readlines()
    read_fix_list.close()
    xyz = xyz[8:]
    read_z = [i.split()[2]  for i in xyz]
    fix_list = np.unique(read_z)
    return fix_list[:n]

def joinxyz(x):
    return  '     '+ '     '.join(x) + '\n'

def fix_atom_selected(source_file, target_file, fix_list):
    fixed_atom_num = 0
    row_sign = 0
    selected = 0
    with open(source_file, mode = 'r') as initial_file:
        with open(target_file, mode = 'w') as finished_file:
            for line in initial_file:
                if row_sign < 7:
                    finished_file.write(line)
                elif row_sign == 7:
                    if list(line.strip())[0] == 's' or list(line.strip())[0] == 'S':
                        selected = 1
                    else:
                        selected = 0
                        finished_file.write('selective\n')
                    finished_file.write(line)
                else:
                    if selected:
                        finished_file.write(line)
                    else:
                        finished_file.write(line.rstrip())
                        z=line.split()[2]
                        if z in fix_list:
                            finished_file.write(' F F F \n')
                            fixed_atom_num +=1
                        else:
                            finished_file.write(' T T T \n')
                row_sign += 1
            print 'there are %d atoms fixed' % fixed_atom_num
        return target_file
    
def get_vaspfile(infile):
    if infile != '':
        return infile
    filename_list = os.listdir('./')
    for filename in filename_list:
        if '.vasp' in filename:
            return filename
            
if __name__ == '__main__':
    input_vasp = ''
    input_vasp = get_vaspfile(input_vasp)
    fp = open(input_vasp , 'r')
    read_fp = fp.readlines()
    num = np.sum(np.array(map(int, read_fp[6].strip().split())))
    element = read_fp[5]
    element = element.strip().split()
    num_element = read_fp[6]
    num_element = num_element.strip().split()
    num_element = [int(i) for i in num_element]
    xyz = read_fp[ 8: ]
    xyz = [ i.strip().split()      for  i in xyz]
    fp.close()
    elem_xyz =[]
    top_to_bottom = 0 #ture
    for i in range(len(element)):
        elem_type = element[i]
        elem_num = num_element[i]
        elem_xyz.append(xyz[:elem_num])
        xyz = xyz[elem_num:]
        print elem_type, elem_num
    elem_xyz_sort = []
    for j in range(len(elem_xyz)):
        elem_xyz[j] = xyzsort(elem_xyz[j], top_to_bottom)
        for k in range(len(elem_xyz[j])):
            elem_xyz_sort.append(elem_xyz[j][k])
    del read_fp[8: ]
    read_fp.extend(map(joinxyz, elem_xyz_sort))
    write_fp = open('POSCAR_sort', 'w')
    write_fp.writelines(read_fp)
    write_fp.close()
    
    num_layer_fixed = 2
    input_file = 'POSCAR_sort'  
    output_file = 'POSCAR'
    a = fix_atom_selected(input_file, output_file, read_fix_list(input_file, num_layer_fixed))