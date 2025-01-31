import numpy as np
from ase import Atoms
from ase.optimize import BFGS
from gpaw import GPAW, PW, FermiDirac

pC = np.array([17.0000,10.0000,0.0000])   
pCO1 = np.array([18.0221,10.5679,0.0000])
pCO2 = np.array([15.9779,9.4321,0.0000])

pNO1 = np.array([34.0352,10.1257,0.0000])
pN = np.array([33.0792,9.3952,0.0000])
pNO2 = np.array([32.9439,8.1997,0.0000])

pS = np.array([17.0053,0.0632,0.0000])
pSO1 = np.array([18.3245,0.6972,0.0000])
pSO2 = np.array([15.8098,0.9076,0.0000])

print(np.linalg.norm(pCO1 - pC))
print(np.linalg.norm(pCO2 - pC))

print(np.linalg.norm(pNO1 - pN))
print(np.linalg.norm(pNO2 - pN))

print(np.linalg.norm(pSO1 - pS))
print(np.linalg.norm(pSO2 - pS))

import numpy as np

def bond_angle(p1, p2, p3):
    """Calculate the bond angle in degrees between three points."""
    v1 = p1 - p2  # Vector from central atom to first atom
    v2 = p3 - p2  # Vector from central atom to second atom

    # Compute cosine of the angle
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    # Convert to degrees
    theta = np.degrees(np.arccos(cos_theta))
    return theta

# Carbon-Oxygen bond angle (CO1 - C - CO2)
angle_C = bond_angle(pCO1, pC, pCO2)

# Nitrogen-Oxygen bond angle (NO1 - N - NO2)
angle_N = bond_angle(pNO1, pN, pNO2)

# Sulfur-Oxygen bond angle (SO1 - S - SO2)
angle_S = bond_angle(pSO1, pS, pSO2)

print(f"Bond angle CO1 - C - CO2: {angle_C:.2f}°")
print(f"Bond angle NO1 - N - NO2: {angle_N:.2f}°")
print(f"Bond angle SO1 - S - SO2: {angle_S:.2f}°")



co2 = Atoms(symbols='COO', positions=[pC, pCO1, pCO2])
no2 = Atoms(symbols='NOO', positions=[pN, pNO1, pNO2])
so2 = Atoms(symbols='SOO', positions=[pS, pSO1, pSO2])

co2.set_cell([10,10,10])
co2.center()
co2.pbc = False

no2.set_cell([10,10,10])
no2.center()
no2.pbc = False

so2.set_cell([10,10,10])
so2.center()
so2.pbc = False
# Set up GPAW calculator
calc = GPAW(mode=PW(600), xc='PBE', occupations=FermiDirac(0.01))

# Attach calculator to atoms
co2.calc = calc
no2.calc = calc
so2.calc = calc

c_optimizer = BFGS(co2)
c_optimizer.run(fmax=500)  # Relax until forces are below 0.05 eV/Å
E_C = co2.get_potential_energy()

n_optimizer = BFGS(no2)
n_optimizer.run(fmax=500)  # Relax until forces are below 0.05 eV/Å
E_N = no2.get_potential_energy()

s_optimizer = BFGS(so2)
s_optimizer.run(fmax=500)  # Relax until forces are below 0.05 eV/Å
E_S = so2.get_potential_energy()


print(f'co2: {E_C:.2f} eV')
print(f'no2: {E_N:.2f} eV')
print(f'so2: {E_S:.2f} eV')