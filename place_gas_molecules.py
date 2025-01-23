from gas_orientations import initial_orientation, symmetric_orientations, asymmetric_orientations
import numpy as np

def build_systems(mxene, gas, position, cell_size):
    systems = []
    gas = initial_orientation(gas, cell_size)
    if 'C' in gas.symbols:
        orientations = symmetric_orientations(gas, cell_size)
    else:
        orientations = asymmetric_orientations(gas, cell_size)


    for state in orientations:
        gas_state = state.copy()
        gas_state.positions += np.array(position, position, position) - cell_size * np.ones((3,3))
        
        system = mxene + gas_state
        systems.append(system)
    return systems