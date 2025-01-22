import numpy as np
from ase.build import find_optimal_cell_shape
from ase.build import make_supercell
from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac
from ase.io import vasp
from ase import Atoms
from ase.optimize import BFGS
from ase.optimize import QuasiNewton
from ase.lattice.hexagonal import Graphite #set up graphite using ASE
from ase.lattice.hexagonal import Graphene #set up graphene using ASE
from ase.visualize import view 
from ase import Atom
from ase.io import read,write
from ase.constraints import StrainFilter
from ase.io import Trajectory
from ase.visualize import view
import os
from optimal_strucute_from_POSCAR import optimal_structure

#voor deze functie
#als deeltjes
# co2,so2, no2
#als positie
#1  2  3  4

deeltje = 0
positie = 0
optimal_structure(type_deeltje = deeltje, type_position = positie)