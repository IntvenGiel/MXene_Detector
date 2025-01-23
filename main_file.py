import os
from gas import initialize_optimized_gas
from mxene import initialize_optimized_mxene

mxene_name = 'Ti2C'
functional = 'functional'
current_dir = os.path.dirname(os.path.realpath(__file__))
mxene_cell_size = 3



def main(gas_name, mxene_name, functional):
    gas_molecule = initialize_optimized_gas(gas_name, functional, current_dir)
    mxene = initialize_optimized_mxene(mxene_name, functional, current_dir)
    # works up until this point
    

    pass


main('co2', 'Ti2C', 'pbe')


