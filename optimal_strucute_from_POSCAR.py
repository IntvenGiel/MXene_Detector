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
from convergence_tests import converge_kpoints, converge_ecut

work_dir = os.path.dirname(os.path.realpath(__file__))


#deze code kijkt ook al of de file al bestaat voordat ie m gaat runne
#de twee namen die je nu mee moet geven slaan hem zo op

def optimal_structure(naam_deeltje, position, functional):
    threshold = 0.01
    structure = read(filename='Mxene_poscar')

    #hier ga ik kijken of we de k points en encuts al hebben en anders bereken je ze
    if os.path.isfile(f'{work_dir}/data_for_simulation/convergence_{functional}') == False:
        encuts = converge_ecut(atoms= structure, functional = functional,threshold= threshold )
        k =  converge_kpoints(atoms = structure,functional = functional, threshold = threshold, encut=encuts)
        lijst_convergence = [encuts, k]

        with open(f'{work_dir}/data_for_simulation/convergence/convergence_{functional}', "w") as file:
            # Write each item in the list to a new line
            for item in lijst_convergence:
                file.write(str(item) + "\n") 
    else:
        with open(f'{work_dir}/data_for_simulation/convergence/convergence_{functional}', "r") as file:
            # Read all lines and strip newline characters
            lijst_convergence = [line.strip() for line in file]  
            encuts, k = lijst_convergence

    #op welke positie wil je hem
    positie = get_position(position)

    #welke deeltje wil je
    Molecule = read(f'CONTCAR_{naam_deeltje}-optimized-{functional}')

    #deeltje op de goede plek zetten
   
    Molecule.position = positie

    #molecuul toevoegen
    structure =+ Molecule

    #vanaf hiet gaan we de brekeningen doen
    calc = GPAW(mode=PW(encuts),
                kpts=(k,k,1), #Replace with optimised energy cut off and k mesh 
                xc='PBE', 
                occupations=FermiDirac(0.05), 
                txt=f'{work_dir}/opt_{naam_deeltje}_{position}.txt')


    #hier doen we de geometry optimilization
    if os.path.isfile(f'{work_dir}/output_{naam_deeltje}_{position}.xyz') == False:
        structure.calc=calc
        calcname = f'opt_{naam_deeltje}_{position}'
        opt=BFGS(structure,trajectory=(f'{work_dir}/{naam_deeltje}_opt_{position}.traj')) #performs a geometry optimisation
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
