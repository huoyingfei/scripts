#!/usr/bin/env python3

# Written on 2021-06-03
# For generating Transition State structures
# To use it: python3 idpp.py ini/POSCAR fin/POSCAR 4

from pymatgen.core import Structure
from pymatgen.analysis.diffusion.neb.pathfinder import IDPPSolver
import numpy as np
import os
import sys

sys.stdout = open(os.devnull, 'w')

if len(sys.argv) <4:
    raise SystemError('Sytax Error! Run as python idpp ini/POSCAR fin/POSCAR 4')

init_struct = Structure.from_file(sys.argv[1], False)
final_struct = Structure.from_file(sys.argv[2], False)

obj = IDPPSolver.from_endpoints(endpoints=[init_struct, final_struct], nimages=int(sys.argv[3]), 
                                sort_tol=1.0)
new_path = obj.run(maxiter=5000, tol=1e-5, gtol=1e-3,step_size=0.05,\
                         max_disp=0.05, spring_const=5.0)

for i in range(len(new_path)):
    image_file='{0:02d}'.format(i)
    if not os.path.exists(image_file):
        os.makedirs(image_file)
    POSCAR_file=image_file+'/POSCAR'
    new_path[i].to(fmt="poscar", filename=POSCAR_file)

sys.stdout = sys.__stdout__
