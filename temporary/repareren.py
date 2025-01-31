from ase.visualize import view
from ase.io import read,write
import numpy as np
import ase.build

# Should only be ran once, to create correct Ti2C poscar file, is not necessary if poscar file is downloaded from github
filename = 'CONTCAR-Ti2C'

structure = read(filename=filename)
params = structure.get_cell_lengths_and_angles()
a, b = params[:2]
structure.set_cell([a,b,10])
view(structure)
write('CONTCAR-Ti2C', structure)