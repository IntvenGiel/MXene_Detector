#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ase.build import find_optimal_cell_shape
from ase.build import make_supercell
from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac
from ase.io import vasp
from ase import Atoms
from ase.optimize import BFGS
from ase.optimize import QuasiNewton
from ase.lattice.hexagonal import Graphite #set up graphite using ASE
from ase.lattice.hexagonal import Graphene #set up graphene using ASE
from ase.visualize import view 
from ase import Atom
from ase.io import read,write
from ase.constraints import StrainFilter
from ase.io import Trajectory
from ase.visualize import view
import os
from get_deeltje import get_deeltje

def get_position(type_positie):
    if type_positie == 0:
        positie = 2.46803 , -1.42492 ,2.36
        naam_positie = 'top'
    if type_positie == 1:
        positie = (2.46803 +1.23402 )/2 , (-1.42492+ -0.71246)/2 , 2.36
        naam_positie = 'top'
    if type_positie == 2:
        positie = (2.46803+ 2.46803 )/2, ( 1.42492 +-1.42492)/2,  2.36
        naam_positie = 'top'
    naam_positie = positie
    return(positie, naam_positie)


#ccdist = 1.42
#layerdist = 9
pops = 8

ccdist = 1.42
c = 9

a = ccdist * np.sqrt(3)
# graphene = Graphene('C', size=(2,1,1), latticeconstant={'a': a, 'c': c})  #Set up the initial guess for structure and lattice constants for a 1x1x1 supercell of graphene
# # graphene.pop()