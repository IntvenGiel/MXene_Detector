import matplotlib.pyplot as plt
from gpaw import GPAW
from gpaw import PW
from ase import Atoms
from ase.build import bulk
from ase.lattice.hexagonal import Graphene #set up graphene using ASE
from ase.io import Trajectory
import numpy as np
import os

work_dir = os.path.dirname(os.path.realpath(__file__))

def converge_ecut(atoms,functional, threshold):
    # edif = float('inf')
    # prev_energy = 0
    # ecut = 200
    # estep = 50
    # while edif > threshold:
    #     ecut += estep
    #     atoms.calc = GPAW(mode=PW(ecut),
    #                     xc=functional,
    #                     kpts=(4, 4, 1)
    #                     )
    #     energy=atoms.get_potential_energy()
    #     edif = abs(energy - prev_energy) / len(atoms)
    #     prev_energy = energy
    # print(f'Energy cut converged at ecut: {ecut}')
    ecut = 700
    return ecut

def converge_kpoints(atoms,functional, threshold, encut):
    # edif = float('inf')
    # prev_energy=0
    # k = 1
    # while edif > threshold:
    #     k += 1
    #     atoms.calc = GPAW(mode=PW(encut),
    #                     xc=functional,
    #                     kpts=(k, k, 1))
    #     energy=atoms.get_potential_energy() 
    #     edif = abs(energy - prev_energy) / len(atoms)
    #     prev_energy = energy
    # print(f'k-value converged at {k}')
    k = 5
    return k