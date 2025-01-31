from ase.visualize import view
from ase.io import read,write
from ase import Atom
from ase.optimize import BFGS
from gpaw import GPAW

for gas in ['CO2', 'NO2', 'SO2']:
    filename = f'/home/intvengiel/computerlab/project/gas/molecules/CONTCAR-{gas}-optimized-PBE'
    structure = read(filename=filename, format='vasp')
    calc = GPAW('/home/intvengiel/computerlab/project/gas/calculator/PBE-calculator.gpw')
    structure.calc = calc
    opt=BFGS(structure,trajectory=('/home/intvengiel/computerlab/project/gas/trajectories/' + gas +'-PBE.traj'))
    opt.run(fmax=0.01)
    calc.write('/home/intvengiel/computerlab/project/gas/calculator/' + gas +'PBE-calculator.gpw', mode='all')
    write('/home/intvengiel/computerlab/project/gas/molecules/' + f'CONTCAR-{gas}-optimized-PBE', structure)
    view(structure)