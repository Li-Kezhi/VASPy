#!/usr/bin/env python

'''
    Script to convert XDATCAR to *.xyz file.
'''

import numpy as np

from vaspy.atomco import XyzFile
from vaspy.functions import str2list, line2list


filename = 'XDATCAR'

info_nline = 7
with open(filename, 'r') as f:
    # read lattice info
    system = f.readline().strip()
    bases_const = float(f.readline().strip())

    # lattice basis
    bases = []
    for i in range(3):
        basis = line2list(f.readline())
        bases.append(basis)

    # atom info
    atom_types = str2list(f.readline())
    atoms_num = str2list(f.readline())
    atom_numbers = [int(i) for i in atoms_num]
    natom = sum(atom_numbers)
    atom_names = []
    for n, atom in zip(atoms_num, atom_types):
        atom_names.extend([atom]*int(n))

    while True:
        try:
            content = ''
            for i in range(info_nline):
                f.readline()  # skip info lines

            step = f.readline().strip().split()[-1]
            content += '          ' + str(natom) + '\n'
            content += 'STEP =        ' + str(step) + '\n'

            for i in range(natom):
                content += '%2s' % atom_names[i]
                relative_coord = np.array(line2list(f.readline()), dtype='float64')
                direct_coord = np.dot(bases, relative_coord) * bases_const
                content += '%16.9f%16.9f%16.9f\n' %\
                        (direct_coord[0], direct_coord[1], direct_coord[2])

            out_name = 'xdatcar' + str(step) + '.xyz'
            with open(out_name, 'w') as f1:
                f1.write(content)
            with open('xdatcar.xyz', 'a') as f2:
                f2.write(content)
                f2.close()

        except IndexError:
            break
