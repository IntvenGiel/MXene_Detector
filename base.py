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
from opt_from_POSCAR import optimal_structure

#voor deze functie
#als deeltjes
# 0 == Li
#1 ==
#2 == 
#als positie
#1 top
#2 hollow
#3 bridge

deeltje = 0
positie = 0
optimal_structure(type_deeltje = deeltje, type_position = positie)