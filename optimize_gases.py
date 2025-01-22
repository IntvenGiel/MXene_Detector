from gas import create_gas, optimize_gas
from ase.visualize import view

gases = ['CO2', 'NO2', 'SO2']
filenames = ['co2-optimized', 'no2-optimized', 'so2-optimized']


for i in range(len(gases)):
    struct = create_gas(gases[i])
    optimize_gas(struct, 'PBE', filenames[i] + '-PBE')