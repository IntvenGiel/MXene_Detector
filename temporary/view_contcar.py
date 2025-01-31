from ase.visualize import view
from ase.io import read,write

filename = 'CONTCAR-Ti2C'

structure = read(filename=filename, format='vasp').repeat((2,2,2))
view(structure)