import os
from gas import initialize_optimized_gas
from mxene import initialize_optimized_mxene
from inequivalents import calculate as inequivalent_sites
from place_gas_molecules import build_systems as place_gas

current_dir = os.path.dirname(os.path.realpath(__file__))
mxene_supercell_size = 3
gas_cellsize = 4
adsorption_distance = 3 #We should look this up in literature, might also be dependent on the gas

def main(gas_name, mxene_name, functional, index):
    gas_molecule = initialize_optimized_gas(gas_name, functional, current_dir)
    mxene = initialize_optimized_mxene(mxene_name, functional, current_dir, mxene_supercell_size)
    inequivalent_sites = inequivalent_sites(mxene, adsorption_distance)
    
    site = inequivalent_sites[index]
    systems = place_gas(mxene, gas_molecule, site, gas_cellsize)

    pass



# ONLY CHANGE BELOW THIS

inequivalent_index = 1
molecule_name = 'CO2'
mxene_name = 'Ti2C'
functional = 'PBE'

main(molecule_name, mxene_name, functional)


