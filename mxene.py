from ase import Atoms
from ase.io import read, write
from ase.optimize import BFGS
from gpaw import GPAW, PW, FermiDirac
from convergence_tests import converge_ecut, converge_kpoints
import os

def check_optimized_mxene(name, path, functional):
    """Checks whether an mxene has already been optimized"""
    try:
        mxene = read(path + '/mxene/molecules/' + f'CONTCAR-{name}-optimized-{functional.upper()}')
        return mxene
    except:
        pass
    return None

def initialize_mxene_sheet(name, path):
    filename = f'CONTCAR-{name}'
    primitive = read(path + '/mxene/' + filename, format='vasp')
    mxene = primitive.repeat((3,3,1))
    return mxene


def optimize_mxene_sheet(structure, functional, name, path):
    try:
        calc = GPAW(path + '/mxene/calculator/' + functional.upper() + '-calculator.gpw')
    except:
        threshold = 0.01
        ecut_converged = converge_ecut(structure, functional, threshold)
        k_converged = converge_kpoints(structure, functional, threshold)

        calc = GPAW(mode=PW(ecut_converged),
                        kpts=(k_converged,k_converged,1),
                        xc=functional, 
                        occupations=FermiDirac(0.01), 
                        txt= path + '/mxene/calculator/' + functional.upper() + '.txt')
    
    structure.calc=calc
    opt=BFGS(structure,trajectory=(path + '/mxene/trajectories/' + functional.upper() +'.traj'))
    opt.run(fmax=0.01)
    calc.write(path + '/mxene/calculator/' + functional.upper() + '-calculator.gpw', mode='all')
    write(path + '/mxene/molecules/' + f'CONTCAR-{name}-optimized-{functional.upper()}', structure)


def initialize_optimized_mxene(mxene_name, functional, path):
    mxene_opt = check_optimized_mxene()
    if mxene_opt == None:
        sheet = initialize_mxene_sheet(mxene_name, path)
        optimize_mxene_sheet(sheet, functional, mxene_name, path)
    return read(path + '/mxene/molecules/' + f'CONTCAR-{mxene_name}-optimized-{functional.upper()}', format='vasp')