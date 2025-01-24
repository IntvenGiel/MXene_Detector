import os
from gas import initialize_optimized_gas
from mxene import initialize_optimized_mxene
from inequivalents import calculate as inequivalent_sites
from place_gas_molecules import build_systems as place_gas
from optimize_system import optimized_system as system_optimize

current_dir = os.path.dirname(os.path.realpath(__file__))
mxene_supercell_size = 3
gas_cellsize = 4
adsorption_distance = 4 #We should look this up in literature, might also be dependent on the gas

def create_optimized_systems(gas_name, mxene_name, functional, index):
    gas_molecule = initialize_optimized_gas(gas_name, functional, current_dir)
    mxene = initialize_optimized_mxene(mxene_name, functional, current_dir, mxene_supercell_size)
    ineq_sites = inequivalent_sites(mxene, adsorption_distance)
    site = ineq_sites[index]
    unoptimized_systems = place_gas(mxene, gas_molecule, site, gas_cellsize, index, functional, current_dir)
    
    for orientation in range(len(unoptimized_systems))
        system_optimize(gas_molecule, site, orientation, functional, current_dir)

molecule_name = 'CO2'
mxene_name = 'Ti2C'
functional = 'PBE'
for site in range(4):
    create_optimized_systems(molecule_name, mxene_name, functional, site)

