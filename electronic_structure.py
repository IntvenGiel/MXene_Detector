from ase.dft.kpoints import bandpath
from gpaw import restart
import matplotlib.pyplot as plt
import numpy as np
import os
from gpaw import GPAW
from ase.visualize import view

def restart_calc(gas, functional):
    if gas == 'CO2':
        orient = 1
    else:
        orient = 0

    current_dir = os.path.dirname(os.path.realpath(__file__))
    calculator_dir = current_dir + '/system/calculator/'
    calculator_name = f'{gas}-{functional}-{1}-{orient}' + '-calculator.gpw'
    return restart(calculator_dir + calculator_name)

def main(gas, functional):
    # Reload the converged calculation
    atoms, calc = restart_calc(gas, functional)
    print(f'Energy: {calc.get_potential_energy()} eV')

    ef = calc.get_fermi_level()
    calc = calc.fixed_density(
    nbands=200,
    symmetry='off',
    kpts={'path': 'GMKG', 'npoints': 60},
    convergence={'bands': 16})

    bs = calc.band_structure()
    bs.plot(filename=f'bandstructure-{gas}-{functional}-centered.png', show=False, emin=ef-2.5, emax=ef+2.5)
    return ef

def get_fermi(gas, functional):
    atoms, calc = restart_calc(gas, functional)
    return f'{gas} Fermi energy: {calc.get_fermi_level()} eV'

# for gas in ['pristine']:
#     main(gas, 'PBEU')

fermis = []
for gas in ['pristine', 'CO2', 'NO2']:
    fermis.append(get_fermi(gas, 'PBEU'))

for line in fermis:
    print(line)