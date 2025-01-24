from ase import Atoms
from ase.io import read, write
from ase.optimize import BFGS
from gpaw import GPAW, PW, FermiDirac
from convergence_tests import converge_ecut, converge_kpoints
import os

def check_optimized_system(gas, ineq, orient, functional, path):
    """Checks whether an mxene has already been optimized"""
    try:
        system = read(path + '/system/optimized/' + f'CONTCAR-system-{gas.symbols}-{functional}-{ineq}-{orient}')
        return system
    except:
        pass
    return None

def optimize(gas, functional, ineq, orient, path):
    structure = read(path + '/system/unoptimized/' + f'CONTCAR-system-{gas.symbols}-{functional}-{ineq}-{orient}', format='vasp')
    
    try:
        calc = GPAW(path + '/system/calculator/' + functional + f'{gas.symbols}-{ineq}-{orient}' + '-calculator.gpw')
    except:
        if functional == 'PBE':
            ecut_converged = 1150
            k_converged = 7
        else:
            threshold = 0.01
            ecut_converged = converge_ecut(structure, functional, threshold)
            k_converged = converge_kpoints(structure, functional, threshold, ecut_converged)

        calc = GPAW(mode=PW(ecut_converged),
                        kpts=(k_converged,k_converged,1),
                        xc=functional, 
                        occupations=FermiDirac(0.01), 
                        txt= path + '/system/calculator/' + f'{gas.symbols}-{functional}-{ineq}-{orient}' + '.txt')
    
    structure.calc=calc
    print('top')
    opt=BFGS(structure,trajectory=(path + '/system/trajectories/' + f'{gas.symbols}-{functional}-{ineq}-{orient}'+'.traj'))
    opt.run(fmax=0.01)
    calc.write(path + '/system/calculator/' + functional + f'{gas.symbols}-{ineq}-{orient}' + '-calculator.gpw', mode='all')
    write(path + '/system/optimized/' + f'CONTCAR-system-{gas.symbols}-{functional}-{ineq}-{orient}', structure)

def optimized_system(gas, ineq, orient, functional, path):
    system_opt = check_optimized_system(gas, ineq, orient, functional, path)
    if system_opt == None:
        optimize(gas, functional, ineq, orient, path)
    return read(path + '/system/optimized/' + f'CONTCAR-system-{gas.symbols}-{functional}-{ineq}-{orient}', format='vasp')