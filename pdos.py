from gpaw import GPAW, restart
from gpaw.utilities.dos import LCAODOS
import matplotlib.pyplot as plt
import numpy as np
import os

def restart_calc(gas, functional):
    """Load calculation with proper basis verification"""
    if gas == 'CO2':
        orient = 1
    else:
        orient = 0

    path = os.path.join(os.path.dirname(__file__),
                       f'system/calculator/{gas}-{functional}-1-{orient}-calculator.gpw')
    atoms, calc = restart(path)
    
    # Verify basis set configuration
    if not isinstance(calc.wfs, GPAW.wfs.lcao.LCAOWaveFunctions):
        raise ValueError("PDOS requires LCAO basis. Re-run calculation with mode='lcao'")
    return atoms, calc

def calculate_pdos(atoms, calc, gas, functional):
    """Robust PDOS calculation with input validation"""
    plt.figure(figsize=(10, 8))
    e_f = calc.get_fermi_level()
    
    # Total DOS
    plt.subplot(211)
    e, dos = calc.get_dos(npts=2001, width=0.2)
    plt.plot(e - e_f, dos, 'k-', label='Total DOS')
    plt.xlim(-5, 5)
    plt.ylim(0, dos[(e >= e_f-5) & (e <= e_f+5)].max() * 1.1)
    plt.ylabel('DOS')
    plt.title(f'{gas} ({functional})')
    plt.legend()

    # PDOS Calculation
    plt.subplot(212)
    dos = LCAODOS(calc)
    energies = dos.get_energies() - e_f
    
    # Define species and orbitals
    species = {
        'Ti': {'orbitals': [('d', 2)], 'color': 'blue'},
        'C': {'orbitals': [('p', 1)], 'color': 'green'},
        'O': {'orbitals': [('p', 1)], 'color': 'red'}
    }

    for element, config in species.items():
        indices = [a for a, atom in enumerate(atoms) if atom.symbol == element]
        if not indices:
            print(f"No {element} atoms found")
            continue
            
        total_pdos = np.zeros_like(energies)
        for orbital, l in config['orbitals']:
            weights = dos.get_subspace_pdos([(a, l) for a in indices])
            total_pdos += weights.sum(axis=0)
            
        plt.plot(energies, total_pdos, 
                label=f'{element}({orbital})', 
                color=config['color'])

    plt.xlim(-5, 5)
    plt.ylim(bottom=0)
    plt.xlabel('Energy (eV)')
    plt.ylabel('PDOS')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'pdos_{gas}_{functional}.png', dpi=300)
    plt.close()

def main(gas, functional):
    atoms, calc = restart_calc(gas, functional)
    print(f"System energy: {calc.get_potential_energy():.3f} eV")
    calculate_pdos(atoms, calc, gas, functional)

if __name__ == "__main__":
    systems = ['pristine', 'CO2', 'SO2', 'NO2']
    for system in systems:
        main(system, 'PBEU')