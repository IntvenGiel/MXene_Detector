from ase import Atoms
from ase.build import bulk
from ase.io import read
from gpaw import GPAW, PW, FermiDirac
import numpy as np

# Read the MXene structure from a VASP CONTCAR file
MXene = read('CONTCAR-Ti2C', format='vasp')

# Define bulk carbon (hcp structure)
C = bulk('C', 'hcp', a=2.46, c=6.70)

# Define bulk titanium
Ti = bulk('Ti')

# Define the GPAW calculator for PBE functional with higher ecut and kpts
calcPBE = GPAW(mode=PW(800),  # Increased ecut to 800 eV
               xc='PBE',
               kpts=(10, 10, 10),  # Increased k-point grid density
               occupations=FermiDirac(0.01))

# Attach the PBE calculator to bulk carbon and calculate its energy
C.set_calculator(calcPBE)
E_C = C.get_potential_energy()
print(f"Energy of bulk carbon (PBE): {E_C} eV")

# Attach the PBE calculator to bulk titanium and calculate its energy
Ti.set_calculator(calcPBE)
E_Ti = Ti.get_potential_energy()
print('\n\n\n')
print(f"Energy of bulk carbon (PBE): {E_C} eV")
print(f"Energy of bulk titanium (PBE): {E_Ti} eV")

# Define a range of U-values to test
U_values = np.arange(1.6, 2.0, 0.1)  # U-values from 0.0 to 5.0 in steps of 0.5



# Initialize lists to store U-values and corresponding formation energies
U_list = []
formation_energies = []

# Loop over U-values
for U in U_values:
    print(f"\nCalculating for U = {U} eV")

    # Define the GPAW calculator for PBE+U functional with the current U-value
    calcPBEU = GPAW(mode=PW(800),  # Increased ecut to 800 eV
                    xc='PBE',
                    kpts=(10, 10, 10),  # Increased k-point grid density
                    setups={'Ti': f':d,{U}'},  # Apply the current U-value to Ti 3d orbitals
                    occupations=FermiDirac(0.01))

    # Attach the PBE+U calculator to MXene and calculate its energy
    MXene.set_calculator(calcPBEU)
    E_MXene = MXene.get_potential_energy()
    print(f"Energy of MXene (PBE+U, U={U} eV): {E_MXene} eV")

    # Calculate the formation energy of the MXene cell
    formation_energy = E_MXene - (E_Ti + E_C)
    print(f"Formation energy of MXene (U={U} eV): {formation_energy} eV")

    # Save the U-value and formation energy
    U_list.append(U)
    formation_energies.append(formation_energy)

# Save the results to a file
results = np.column_stack((U_list, formation_energies))
np.savetxt('formation_energy_vs_U.dat', results, header='U-value (eV)    Formation Energy (eV)', fmt='%.4f')

print("\nResults saved to 'formation_energy_vs_U.dat'")