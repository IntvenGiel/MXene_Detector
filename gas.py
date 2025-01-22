from ase import Atom
from ase import Atoms
from ase.visualize import view


def create_gas(name):
    if name.lower() == 'co2':
        # Source: https://webbook.nist.gov/cgi/cbook.cgi?ID=C124389&Units=SI (NIST DATABASE)
        c_position = (0,0,0)
        o1_position = (1.0221,0.5679, 0)
        o2_position = (-1.0221, -0.5679, 0)
        CO2 = Atoms(symbols=['C', 'O', 'O'], positions=[c_position, o1_position, o2_position])
        return CO2
    if name.lower() == 'so2':
        # Source: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7446095&Units=SI (NIST DATABASE)
        s_position = (0,0,0)
        o1_position = (1.3192, 0.634, 0)
        o2_position = (-1.1954, 0.8444, 0)
        SO2 = Atoms(symbols=['S', 'O', 'O'], positions=[s_position, o1_position, o2_position])
        return SO2
    if name.lower() == 'no2':
        # Source: https://webbook.nist.gov/cgi/cbook.cgi?ID=C10102440&Units=SI (NIST DATABASE)
        n_position = (0,0,0)
        o1_position = (0.956, 0.7305, 0)
        o2_position = (-0.1353, -1.1955, 0)
        NO2 = Atoms(symbols=['N', 'O', 'O'], positions=[n_position, o1_position, o2_position])
        return NO2

from ase.optimize import BFGS
from gpaw import GPAW, PW, FermiDirac
from convergence_tests import converge_ecut, converge_kpoints
from ase.io import read,write
import os

def optimize_gas(structure, functional, filename, ecut_converged=None, k_converged=None):
    structure.set_cell([10,10,10])
    structure.center()
    structure.pbc = True

    if f'calculator_gas_{functional}.gpw'not in os.listdir():
        if ecut_converged == None:
            threshold = 0.01
            ecut_converged = converge_ecut(structure, functional, threshold)

        if k_converged == None:
            threshold = 0.01
            k_converged = converge_kpoints(structure, functional, threshold)

        calc = GPAW(mode=PW(ecut_converged),
                kpts=(k_converged,k_converged,1),
                xc=functional, 
                occupations=FermiDirac(0.01), 
                txt=filename+'.txt')
    else:
        calc = GPAW('calculator_gas_{functional}.gpw')
    
    structure.calc=calc
    opt=BFGS(structure,trajectory=(filename+'.traj'))
    opt.run(fmax=0.01)
    calc.write(f'calculator_gas_{functional}.gpw', mode='all')
    write('CONTCAR_'+filename, structure)