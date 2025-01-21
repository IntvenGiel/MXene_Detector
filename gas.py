from ase import Atom
from ase import Atoms
from ase.visualize import view


def create_gas(name):
    if name.lower == 'co2':
        # Source: https://webbook.nist.gov/cgi/cbook.cgi?ID=C124389&Units=SI (NIST DATABASE)
        c_position = (0,0,0)
        o1_position = (1.0221,0.5679, 0)
        o2_position = (-1.0221, -0.5679, 0)
        CO2 = Atoms(symbols=['C', 'O', 'O'], positions=[c_position, o1_position, o2_position])
        return CO2
    if name.lower == 'so2':
        # Source: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7446095&Units=SI (NIST DATABASE)
        s_position = (0,0,0)
        o1_position = (1.3192, 0.634, 0)
        o2_position = (-1.1954, 0.8444, 0)
        SO2 = Atoms(symbols=['S', 'O', 'O'], positions=[s_position, o1_position, o2_position])
        return SO2
    if name.lower == 'no2':
        # Source: https://webbook.nist.gov/cgi/cbook.cgi?ID=C10102440&Units=SI (NIST DATABASE)
        n_position = (0,0,0)
        o1_position = (0.956, 0.7305, 0)
        o2_position = (-0.1353, -1.1955, 0)
        NO2 = Atoms(symbols=['N', 'O', 'O'], positions=[n_position, o1_position, o2_position])
        return NO2