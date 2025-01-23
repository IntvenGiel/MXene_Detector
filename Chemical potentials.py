import numpy as np
from gpaw import GPAW, PW, FermiDirac
from ase import Atoms
from ase.optimize import BFGS
from ase.visualize import view 
from ase.io import read,write
# from ase.constraints import StrainFilter
# from ase.io import Trajectory
from matplotlib import pyplot as plt
from numpy import cos,sin
import os

work_dir = os.path.dirname(os.path.realpath(__file__))

graphene = read(f'{work_dir}/CONTCAR_so2-optimised-PBE')

def energygetter(structure):
    calc = GPAW(mode=PW(1000),
                kpts=(7,7,1), #Replace with optimised energy cut off and k mesh 
                xc='PBE', 
                occupations=FermiDirac(0.01))
    structure.calc=calc
    return structure.get_potential_energy() 


print(energygetter(graphene))  #Chemical potentials for gas absorption, free energy of particle
NO2 = -18.741834830764454
CO2 = -23.602405582927695
SO2 = -17.39757573987345