import numpy as np
from ase.io import read,write
from ase.visualize import view
from ase import Atoms, Atom

def initial_orientation(gas, cell_size):
    size = cell_size/2
    for i in range(len(gas)):
        if gas[i].symbol != 'O':
            main = i
            o1 = (i + 1)%3
            o2 = (i + 2)%3
    molecule = Atoms(gas[main].symbol, positions=[[size,size,size]], cell=[cell_size, cell_size, cell_size], pbc=False)

    bond_distance_o1 = gas.get_distance(main, o1)
    bond_distance_o2 = gas.get_distance(main, o2)
    bond_angle = (gas.get_angle(o1, main, o2) / 180 * np.pi) % np.pi

    if gas[main].symbol == 'C':
        pos_o1 = np.array([-np.sin(bond_angle) * bond_distance_o1, np.cos(bond_angle)*bond_distance_o1, 0])
        pos_o2 = -1 * pos_o1.copy()
        pos_o1 += np.array([size, size, size])
        pos_o2 += np.array([size, size, size])

    else:
        pos_o1 = [-np.sin(bond_angle) * bond_distance_o1 + size, np.cos(bond_angle)*bond_distance_o1 + size, size]
        pos_o2 = [np.sin(bond_angle) * bond_distance_o2 + size, np.cos(bond_angle)*bond_distance_o2 + size, size]
    
    molecule += Atom('O', position=pos_o2)
    molecule += Atom('O', position=pos_o1)
    return molecule


def symmetric_orientations(molecule, cell_size):
    size = cell_size/2
    mol1 = molecule.copy()
    molecule.rotate(90, 'z', center=(size,size,size))
    mol2 = molecule.copy()
    molecule.rotate(90, 'y', center=(size,size,size))
    mol3 = molecule.copy()

    return [mol1, mol2, mol3]

def asymmetric_orientations(molecule, cell_size):
    size = cell_size /2
    axis_orientations = [molecule.copy()]
    molecule.rotate(90, 'z', center=(size,size,size))
    axis_orientations.append(molecule.copy())
    molecule.rotate(90, 'y', center=(size,size,size))
    axis_orientations.append(molecule.copy())

    axes_orientations = axis_orientations.copy()

    for orientation in axis_orientations:
        temp = orientation.copy()
        temp.rotate(90, 'x', center=(size,size,size))
        axes_orientations.append(temp)

    orientations = []
    for state in axes_orientations:
        new_positions = state.positions * -1 + cell_size
        new_state = state.copy()
        new_state.positions = new_positions
        orientations.append(state)
        orientations.append(new_state)
    return orientations