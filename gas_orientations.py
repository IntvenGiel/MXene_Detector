import numpy as np
from ase.io import read,write
from ase.visualize import view
from ase import Atoms
import os 

work_dir = os.path.dirname(os.path.realpath(__file__))

filenames = [f'{work_dir}/CONTCAR_co2-optimized-PBE', f'{work_dir}/CONTCAR_so2-optimized-PBE', f'{work_dir}/CONTCAR_no2-optimized-PBE']
for filename_gas in filenames:
    gas = read(filename=filename_gas, format='vasp')

    for i in range(len(gas)):
        if gas[i].symbol != 'O':
            main = [i]
            o1 = (i + 1)%3
            o2 = (i + 2)%3

    molecule = Atoms(gas[main].symbol, position=[[0,0,0]], cell=[3,3,3], pbc=False)
    bond_distance_o1 = gas.get_distance(main, o1)
    bond_distance_o2 = gas.get_distance(main, o2)