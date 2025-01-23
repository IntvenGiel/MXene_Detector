from ase import Atoms
from ase.io import read, write
from ase.optimize import BFGS
from gpaw import GPAW, PW, FermiDirac
from convergence_tests import converge_ecut, converge_kpoints
import os

def check_gas_exists(name, path, functional):
    """
    Checks whether a gas has already been created and optimized, and saved as a file.
    """
    try:
        gas_files = os.listdir(path + '/gas/molecules')
        filename = f'CONTCAR-{name.upper()}-optimized-{functional.upper()}'
        if filename in gas_files:
            file_path = path + '/gas/molecules/' + filename

            gas = read(file_path, format='vasp')
        return gas
    except:
        pass
    return None

def create_gas(name):
    """"
    Creates the initial state of CO2, SO2 or NO2 from data out of NIST database.
    """
    if name.upper() == 'CO2':
        # Source: https://webbook.nist.gov/cgi/cbook.cgi?ID=C124389&Units=SI (NIST DATABASE)
        c_position = (0,0,0)
        o1_position = (1.0221,0.5679, 0)
        o2_position = (-1.0221, -0.5679, 0)
        CO2 = Atoms(symbols=['C', 'O', 'O'], positions=[c_position, o1_position, o2_position])
        return CO2
    if name.upper() == 'SO2':
        # Source: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7446095&Units=SI (NIST DATABASE)
        s_position = (0,0,0)
        o1_position = (1.3192, 0.634, 0)
        o2_position = (-1.1954, 0.8444, 0)
        SO2 = Atoms(symbols=['S', 'O', 'O'], positions=[s_position, o1_position, o2_position])
        return SO2
    if name.upper() == 'NO2':
        # Source: https://webbook.nist.gov/cgi/cbook.cgi?ID=C10102440&Units=SI (NIST DATABASE)
        n_position = (0,0,0)
        o1_position = (0.956, 0.7305, 0)
        o2_position = (-0.1353, -1.1955, 0)
        NO2 = Atoms(symbols=['N', 'O', 'O'], positions=[n_position, o1_position, o2_position])
        return NO2

def optimize_gas(structure, functional, path, gas_name):
    """"
    Optimizes the initial structure of a gas molecule, convergence tests if none have been performed for the functional.
    """
    structure.set_cell([10,10,10])
    structure.center()
    structure.pbc = True

    # Either reads out calculator or creates one and runs convergence tests
    try:
        calc = GPAW(path + '/gas/calculator/' + functional.upper() + '-calculator.gpw')
    except:
        threshold = 0.01
        ecut_converged = converge_ecut(structure, functional, threshold)
        k_converged = converge_kpoints(structure, functional, threshold)

        calc = GPAW(mode=PW(ecut_converged),
                kpts=(k_converged,k_converged,1),
                xc=functional, 
                occupations=FermiDirac(0.01), 
                txt= path + '/gas/calculator/' + functional.upper() + '.txt')
         
    structure.calc=calc
    opt=BFGS(structure,trajectory=(path + '/gas/trajectories/' + functional.upper() +'.traj'))
    opt.run(fmax=0.01)
    calc.write(path + '/gas/calculator/' + functional.upper() + '-calculator.gpw', mode='all')
    write(path + '/gas/molecules/' + f'CONTCAR-{gas_name.upper()}-optimized-{functional.upper()}', structure)


def initialize_optimized_gas(gas_name, functional, path):
    """"
    Initializes an optimized gas, might take quite a long time on first time running with a functional,
    but should be quicker when ran again since calculators are saved to files.
    """
    gas_molecule = check_gas_exists(gas_name, path, functional)
    if gas_molecule == None:
        gas_molecule = create_gas(gas_name)
        optimize_gas(gas_molecule, functional, path, gas_name)
    
    return read(path + '/gas/molecules/' + f'CONTCAR-{gas_name.upper()}-optimized-{functional.upper()}', format='vasp')