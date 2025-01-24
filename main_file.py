import os
from gas import initialize_optimized_gas
from mxene import initialize_optimized_mxene
from inequivalents import calculate as inequivalent_sites
from place_gas_molecules import build_systems as place_gas
from optimize_system import optimized_system as system_optimize

current_dir = os.path.dirname(os.path.realpath(__file__))
mxene_supercell_size = 3
gas_cellsize = 4
adsorption_distance = 3.5
# A bit higher than https://doi.org/10.1016/j.surfin.2023.102639 and https://doi.org/10.1021/acs.jpcc.7b07921
# this way the optimization will probably decrease distance to most stable
from ase.visualize import view

def create_optimized_systems(gas_name, mxene_name, functional, index):
    gas_molecule = initialize_optimized_gas(gas_name, functional, current_dir)
    mxene = initialize_optimized_mxene(mxene_name, functional, current_dir, mxene_supercell_size)
    ineq_sites = inequivalent_sites(mxene, adsorption_distance)
    site = ineq_sites[index]
    unoptimized_systems = place_gas(mxene, gas_molecule, site, gas_cellsize, index, functional, current_dir)
    
    for orientation in range(len(unoptimized_systems)):
        view(unoptimized_systems[orientation])
        system_optimize(gas_molecule, index, orientation, functional, current_dir)


# Deze is CO2, SO2 of NO2, let op hoofdletters
molecule_name = 'NO2'
# Deze staat in principe vast
mxene_name = 'Ti2C'
# Ik zou hier nu alleen nog PBE gebruiken, voor andere functionalen moeten nieuwe convergence tests gerund worden, 
# die tests en het optimaliseren van de basis-mxene zijn ingebouwd maar duurt erg lang (ongeveer 4 uur).
functional = 'PBE'
# Dit is de index van de lattice site: 0, 1, 2, 3. De verschillende mogelijke oriëntaties van een molecuul worden automatisch geloopt
site = 0
create_optimized_systems(molecule_name, mxene_name, functional, site)