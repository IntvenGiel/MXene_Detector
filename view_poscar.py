from ase.visualize import view
from ase.io import read,write

filename = 'Ti2C.poscar'

structure = read(filename=filename)
view(structure)
view(structure.repeat((3,3,1)))