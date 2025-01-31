import os
from gas import initialize_optimized_gas
from mxene import initialize_optimized_mxene
from inequivalents import calculate as inequivalent_sites
from place_gas_molecules import build_systems as place_gas
from optimize_system import optimized_system as system_optimize
from ase.visualize import view

current_dir = os.path.dirname(os.path.realpath(__file__))
mxene_supercell_size = 2
gas_cellsize = 4
adsorption_distance = 3.5

def create_optimized_systems(gas_name, mxene_name, functional, index):
    gas_molecule = initialize_optimized_gas(gas_name, functional, current_dir)
    mxene = initialize_optimized_mxene(mxene_name, functional, current_dir, mxene_supercell_size)
    ineq_sites = inequivalent_sites(mxene, adsorption_distance, mxene_supercell_size)
    site = ineq_sites[index]
    unoptimized_systems = place_gas(mxene, gas_molecule, site, gas_cellsize, index, functional, current_dir, mxene_supercell_size)

    if gas_name == 'CO2':
        orientation = 1
    else:
        orientation = 0

    view(unoptimized_systems[orientation])
    system_optimize(gas_molecule, index, orientation, functional, current_dir)

# Deze is CO2, SO2 of NO2, let op hoofdletters
molecule_name = 'CO2'
# Deze staat in principe vast
mxene_name = 'Ti2C'
# Ik zou hier nu alleen nog PBE gebruiken, voor andere functionalen moeten nieuwe convergence tests gerund worden, 
# die tests en het optimaliseren van de basis-mxene zijn ingebouwd maar duurt erg lang (ongeveer 4 uur).
functional = 'PBEU'
# Dit is de index van de lattice site: 0, 1, 2, 3. De verschillende mogelijke oriëntaties van een molecuul worden automatisch geloopt
site = 1