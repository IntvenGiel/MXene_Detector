from ase.io import read,write
import numpy as np
from ase import Atom
from ase.visualize import view

filename = 'CONTCAR_co2-optimized-PBE'
structure = read(filename=filename, format='vasp')
view(structure)

filename = 'CONTCAR_no2-optimized-PBE'
structure = read(filename=filename, format='vasp')
view(structure)

filename = 'CONTCAR_so2-optimized-PBE'
structure = read(filename=filename, format='vasp')
view(structure)