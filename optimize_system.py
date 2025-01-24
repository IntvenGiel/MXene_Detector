from ase import Atoms
from ase.io import read, write
from ase.optimize import BFGS
from gpaw import GPAW, PW, FermiDirac
from convergence_tests import converge_ecut, converge_kpoints
import os

def check_optimized_system(ineq, orient, functional, path):
    """Checks whether an mxene has already been optimized"""
    try:
        system = read(path + '/system' + f'CONTCAR-system-optimized-{functional}-{ineq}-{orient}')
        return system
    except:
        pass
    return None

def optimize(structure, functional, ineq, orient, path):
    try:
        calc = GPAW(path + '/system/calculator/' + functional + f'-{ineq}-{orient}' + '-calculator.gpw')
    except:
        threshold = 0.01
        ecut_converged = converge_ecut(structure, functional, threshold)
        k_converged = converge_kpoints(structure, functional, threshold, ecut_converged)

        calc = GPAW(mode=PW(ecut_converged),
                        kpts=(k_converged,k_converged,1),
                        xc=functional, 
                        occupations=FermiDirac(0.01), 
                        txt= path + '/system/calculator/' + functional + f'-{ineq}-{orient}' + '.txt')
    
    structure.calc=calc
    opt=BFGS(structure,trajectory=(path + '/system/trajectories/' + functional +'.traj'))
    opt.run(fmax=0.01)
    calc.write(path + '/system/calculator/' + functional + f'-{ineq}-{orient}' + '-calculator.gpw', mode='all')
    write(path + '/system' + f'CONTCAR-system-optimized-{functional}-{ineq}-{orient}', structure)

def optimized_system(system, ineq, orient, functional, path):
    system_opt = check_optimized_system(ineq, orient, functional, path)
    if system_opt == None:
        optimize(system, functional, ineq, orient, path)
    return read(path + '/system' + f'CONTCAR-system-optimized-{functional}-{ineq}-{orient}', format='vasp')