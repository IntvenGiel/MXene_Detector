import numpy as np
from ase import Atoms
from ase.optimize import BFGS
from gpaw import GPAW, PW, FermiDirac
from ase.io import read,write
from ase.visualize import view

unopt = '/home/intvengiel/computerlab/project/mxene/Ti2C.poscar'
optPBE = '/home/intvengiel/computerlab/project/mxene/CONTCAR-Ti2C-2-optimized-PBE'
optPBEU = '/home/intvengiel/computerlab/project/mxene/CONTCAR-Ti2C-2-optimized-PBEU'

str_unopt = read(filename=unopt, format='vasp').repeat((2,2,1))
str_optPBE = read(filename=optPBE, format='vasp')
str_optPBEU = read(filename=optPBEU, format='vasp')

for str in [str_unopt, str_optPBE, str_optPBEU]:
    cell = str.get_cell()
    a, b, c = cell.lengths()  # Lattice constants in Ångstroms
    alpha, beta, gamma = cell.angles()  # Angles in degrees

    print(f"Lattice parameters: a={a:.2f}, b={b:.2f}, c={c:.2f}")
    print(f"Angles: α={alpha:.2f}°, β={beta:.2f}°, γ={gamma:.2f}°")


calc = GPAW(mode=PW(600), xc='PBE', occupations=FermiDirac(0.01))

calcPBE = GPAW(mode=PW(600),
                kpts=(5,5,1),
                xc='PBE', 
                setups={'Ti': ':d,3.0'},
                occupations=FermiDirac(0.01))
calcPBEU = GPAW(mode=PW(600),
                kpts=(5,5,1),
                xc='PBE', 
                occupations=FermiDirac(0.01))

str_unopt.calc = calcPBE
str_optPBE.calc = calcPBE
str_optPBEU.calc = calcPBEU

unopt_optimizer = BFGS(str_unopt)
unopt_optimizer.run(fmax=500)  # Relax until forces are below 0.05 eV/Å
E_unopt = unopt.get_potential_energy()

optPBE_optimizer = BFGS(str_optPBE)
optPBE_optimizer.run(fmax=500)  # Relax until forces are below 0.05 eV/Å
E_optPBE = optPBE.get_potential_energy()

optPBEU_optimizer = BFGS(str_optPBEU)
optPBEU_optimizer.run(fmax=500)  # Relax until forces are below 0.05 eV/Å
E_optPBEU = optPBEU.get_potential_energy()

print(f'unopt: {E_unopt:.2f} eV')
print(f'PBE: {E_optPBE:.2f} eV')
print(f'PBE+U: {E_optPBEU:.2f} eV')