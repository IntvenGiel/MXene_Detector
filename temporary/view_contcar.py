from ase.visualize import view
from ase.io import read,write

filename = 'CONTCAR'

structure = read(filename=filename, format='vasp')
view(structure)