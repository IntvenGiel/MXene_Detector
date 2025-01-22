from gpaw import GPAW, PW, FermiDirac
from ase.io import read,write
from matplotlib import pyplot as plt

graphene = read('CONTCAR_so2-optimised-PBE')

def energygetter(structure):
    calc = GPAW(mode=PW(1000),
                kpts=(7,7,1), #Replace with optimised energy cut off and k mesh 
                xc='PBE', 
                occupations=FermiDirac(0.01))
    structure.calc=calc
    return structure.get_potential_energy() 


print(energygetter(graphene))  #Chemical potentials for gas absorption, free energy of particle
chempot_NO2 = -18.741834830764454
chempot_CO2 = -23.602405582927695
chempot_SO2 = -17.39757573987345