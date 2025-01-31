from ase.visualize import view
from ase.io import read
from ase.build import bulk
from ase.optimize import BFGS
from gpaw import GPAW, PW, FermiDirac
import numpy as np

# ====================================================
# Load structures
# ====================================================
# Ti₂C MXene (ensure it has vacuum in z-direction!)
mxene = read('/home/intvengiel/workshop-physics/mxene/CONTCAR-Ti2C', format='vasp')

# Bulk Ti (hcp structure - correct lattice parameters)
# Define bulk carbon (hcp structure)
C_graphite = bulk('C', 'hcp', a=2.46, c=6.70)

# Define bulk titanium
Ti_bulk = bulk('Ti')


# ====================================================
# Define calculators
# ====================================================
# PBE calculator (no U)
calc_pbe = GPAW(
    mode=PW(600),
    xc='PBE',
    kpts=(6, 6, 4),  # Dense grid for hcp Ti
    occupations=FermiDirac(0.01),
    txt='pbe.txt'
)

# PBE+U calculator (U=3.0 eV for Ti 3d)
calc_pbeu = GPAW(
    mode=PW(800),
    xc='PBE',
    kpts=(10,10,10),
    setups={'Ti': ':d,1.5'},  # Hubbard U for Ti
    occupations=FermiDirac(0.01),
    txt='pbeu.txt'
)

# ====================================================
# Calculate energies
# ====================================================
def calculate_energy(structure, calc, label):
    """Optimize structure and return energy per atom."""
    atoms = structure.copy()
    atoms.calc = calc
    opt = BFGS(atoms)
    opt.run(fmax=0.01)
    energy = atoms.get_potential_energy()
    n_atoms = len(atoms)
    return energy, energy/n_atoms  # Return total energy and energy/atom

# -------------------------------
# PBE calculations
# -------------------------------
# Ti (hcp)
# energy_ti_pbe_total, energy_ti_pbe = calculate_energy(Ti_bulk, calc_pbe, "Ti-PBE")

# C (graphite)
energy_c_pbe_total, energy_c_pbe = calculate_energy(C_graphite, calc_pbe, "C-PBE")

# # Ti₂C MXene
# energy_mxene_pbe_total, energy_mxene_pbe = calculate_energy(mxene, calc_pbe, "MXene-PBE")

# -------------------------------
# PBE+U calculations
# -------------------------------
# Ti (hcp)
energy_ti_pbeu_total, energy_ti_pbeu = calculate_energy(Ti_bulk, calc_pbeu, "Ti-PBEU")

# Ti₂C MXene
energy_mxene_pbeu_total, energy_mxene_pbeu = calculate_energy(mxene, calc_pbeu, "MXene-PBEU")

# ====================================================
# Print results
# ====================================================
print("\n\n")
print("+----------------------------+----------------+----------------+")
print("| Structure                  | PBE (eV)       | PBE+U (eV)     |")
print("+----------------------------+----------------+----------------+")
print(f"| Bulk Ti (total)           | {0:14.3f} | {energy_ti_pbeu_total:14.3f} |")
print(f"| Bulk Ti (per atom)        | {0:14.3f} | {energy_ti_pbeu:14.3f} |")
print(f"| Graphite C (total)        | {energy_c_pbe_total:14.3f} | {'-':14} |")
print(f"| Graphite C (per atom)     | {energy_c_pbe:14.3f} | {'-':14} |")
print(f"| Ti₂C MXene (total)        | {0:14.3f} | {energy_mxene_pbeu_total:14.3f} |")
print(f"| Ti₂C MXene (per atom)     | {0:14.3f} | {energy_mxene_pbeu:14.3f} |")
print("+----------------------------+----------------+----------------+")

# ====================================================
# Calculate formation energy
# ====================================================
# Formula: E_form = E(Ti₂C) - [2*E(Ti) + E(C)]
#e_form_pbe = energy_mxene_pbe_total - (2*energy_ti_pbe + energy_c_pbe)
e_form_pbeu = energy_mxene_pbeu_total - (2*energy_ti_pbeu + energy_c_pbe)

print("\nFormation Energies:")
# print(f"PBE:   {e_form_pbe:.3f} eV")
print(f"PBE+U: {e_form_pbeu:.3f} eV")