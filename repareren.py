from ase.visualize import view
from ase.io import read,write
import numpy as np
import ase.build
filename = 'Ti2C.poscar'

structure = read(filename=filename)

new_structure = ase.build.cut(structure, a=[1, 0, 0], b = [0, 1, 0], c = [0, 0, 1/3])

view(structure)
view(new_structure)

write('Ti2C_2.poscar', new_structure)