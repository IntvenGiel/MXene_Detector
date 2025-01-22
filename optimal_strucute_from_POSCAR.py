#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ase.build import find_optimal_cell_shape
from ase.build import make_supercell
from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac
from ase.io import vasp
from ase import Atoms
from ase.optimize import BFGS
from ase.optimize import QuasiNewton
from ase.lattice.hexagonal import Graphite #set up graphite using ASE
from ase.lattice.hexagonal import Graphene #set up graphene using ASE
from ase.visualize import view 
from ase import Atom
from ase.io import read,write
from ase.constraints import StrainFilter
from ase.io import Trajectory
from ase.visualize import view
import os
from gas import create_gas
from get_position import get_position

work_dir = os.path.dirname(os.path.realpath(__file__))


#deze code kijkt ook al of de file al bestaat voordat ie m gaat runne
#de twee namen die je nu mee moet geven slaan hem zo op

def optimal_structure(naam_deeltje, type_position):

    strucutre = read(filename='Mxene_poscar')
    

    calc = GPAW(mode=PW(400),
                kpts=(4,4,1), #Replace with optimised energy cut off and k mesh 
                xc='PBE', 
                occupations=FermiDirac(0.05), 
                txt=f'{work_dir}/opt_{naam_deeltje}_{naam_positie}.txt')

    if os.path.isfile(f'{work_dir}/output_{naam_deeltje}_{naam_positie}.xyz') == False:
        structure.calc=calc
        calcname = f'opt_{naam_deeltje}_{naam_positie}'
        opt=BFGS(structure,trajectory=(f'{work_dir}/{naam_deeltje}_opt_{naam_positie}.traj')) #performs a geometry optimisation
        opt.run(fmax=0.01) #convergence criteria for geometry optimisation. Test how this value affects your results

        print(structure.get_potential_energy())

        #Output optimised structure file
        write(f'{work_dir}/output_{naam_deeltje}_{naam_positie}.xyz', structure)  #xyz format
        write(f'{work_dir}/CONTCAR_{naam_deeltje}_{naam_positie}', structure) #POSCAR format 
    else:
        print('heb je al')
        structure.calc=calc
        print(structure.get_potential_energy())
    return
