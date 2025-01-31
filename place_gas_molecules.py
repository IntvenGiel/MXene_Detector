from gas_orientations import initial_orientation, symmetric_orientations, asymmetric_orientations
import numpy as np
from ase.io import write

def build_systems(mxene, gas, position, cell_size, ineq, functional, path, cellsize):
    systems = []
    gas = initial_orientation(gas, cell_size)
    if 'C' in gas.symbols:
        orientations = symmetric_orientations(gas, cell_size)
    else:
        orientations = asymmetric_orientations(gas, cell_size)


    for i in range(len(orientations)):
        state = orientations[i]
        gas_state = state.copy()
        gas_state.positions += np.array([position, position, position])
        
        system = mxene + gas_state
        write(path + '/system/unoptimized/' + f'CONTCAR-system-{cellsize}-{gas.symbols}-{functional}-{ineq}-{i}', system)
        systems.append(system)
    return systems