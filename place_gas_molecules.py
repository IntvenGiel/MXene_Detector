from ase.io import read,write
from ase.visualize import view
from gas_orientations import initial_orientation, symmetric_orientations, asymmetric_orientations
import numpy as np

mxene_file = 'CONTCAR_Ti2C-mxene-PBE'
gas_file = 'CONTCAR_co2-optimized-PBE'

mxene = read(mxene_file, format='vasp').repeat((3,3,1))
gas = read(gas_file, format='vasp')

gas = initial_orientation(gas, cell_size = 4)
if 'C' in gas.symbols:
    orientations = symmetric_orientations(gas, cell_size=4)
else:
    orientations = asymmetric_orientations(gas, cell_size=4)

inequivalent_positions = [np.array([0,1,7]), np.array([1,3,6])]

cell_size = 4
size = cell_size/2


systems = []
for pos in inequivalent_positions:
    for state in orientations:
        gas_state = state.copy()
        
        gas_state.positions += np.array([pos, pos, pos]) - size * np.ones((3,3))
        
        system = mxene + gas_state
        systems.append(system)