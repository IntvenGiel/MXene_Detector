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
from ase.io import read,write
from ase.constraints import StrainFilter
from ase.io import Trajectory
import os 

work_dir = os.path.dirname(os.path.realpath(__file__))

# graphene_defected_2cell = read(filename='POSCARtwee')
# graphene_defect = read(filename='POSCARenkelecarbo')
# graphene_good_2cell = read(filename='POSCARtweebijtwee')

#for exc 2.3:
# graphene_three_musketeers = read(filename='POSCARdriemusketiers')
# grapheen_defectemusketiers = read(filename='POSCARdriemusketiers_metdefect')
grapheen = read(filename=f'{work_dir}/POSCAR')
# grapheen_defect =  read(filename= 'POSCARrechthoekdefect')




def geo_optimise(structure,saveto):
    calc = GPAW(mode=PW(500),
                kpts=(2,8,1), #Replace with optimised energy cut off and k mesh 
                xc='PBE', 
                occupations=FermiDirac(0.01))
    structure.calc=calc

    calcname = f'graphene_opt'
    opt=BFGS(structure,trajectory=('graphene_opt.traj')) #performs a geometry optimisation
    opt.run(fmax=0.01) #convergence criteria for geometry optimisation. Test how this value affects your results

    #Output optimised structure file
    write(f'{work_dir}/outputpiemol.xyz', structure)  #xyz format
    write(f'{work_dir}/CONTCAR_piemol', structure) #POSCAR format  
    return structure.get_potential_energy()

geo_optimise(grapheen,'Lalalalalalalallalalalalalla')
# print(geo_optimise(grapheen_defect,'CONTCARrechthoekdefect'))
