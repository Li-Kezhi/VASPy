#!/usr/bin/env python

'''
    Script to convert XDATCAR to *.xyz file.
'''

import numpy as np

from vaspy.atomco import XyzFile
from vaspy.functions import str2list, line2list


filename = 'XDATCAR'

def __read_info(info):
    '''
    read lattice info
    '''
    # read lattice info
    info['bases_const'] = float(f.readline().strip())

    # lattice basis
    info['bases'] = []
    for i in range(3):
        vector = line2list(f.readline())
        info['bases'].append(vector)


info_nline = 7
info = {}
with open(filename, 'r') as f:
    system = f.readline().strip()
    __read_info(info)

    # atom info
    info['atom_types'] = str2list(f.readline())
    info['atoms_num'] = str2list(f.readline())
    info['atom_numbers'] = [int(i) for i in info['atoms_num']]
    info['natom'] = sum(info['atom_numbers'])
    info['atom_names'] = []
    for n, atom in zip(info['atoms_num'], info['atom_types']):
        info['atom_names'].extend([atom]*int(n))

    while True:
        try:
            content = ''
            flush = f.readline().strip()
            if flush == system:
                __read_info(info)  # update info
                # skip atom info
                f.readline()
                f.readline()
                step = f.readline().strip().split()[-1]
            else:
                step = flush.split()[-1]

            content += '          ' + str(info['natom']) + '\n'
            content += 'STEP =        ' + str(step) + '\n'

            for i in range(info['natom']):
                content += '%2s' % info['atom_names'][i]
                relative_coord = np.array(line2list(f.readline()), dtype='float64')
                direct_coord = np.dot(info['bases'], relative_coord) * info['bases_const']
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
