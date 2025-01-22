from ase.io import read,write
import numpy as np
from ase import Atom
from ase.visualize import view
import os

work_dir = os.path.dirname(os.path.realpath(__file__))

filename = f'{work_dir}/CONTCAR_0pops'
structure = read(filename=filename, format='vasp').repeat((3,3,1))

def getposition(name):
    
    z_top = structure[0].position.copy()[2]
    dist_to_mxene = .3
    struct = structure.copy()
    struct.pbc = False

    #vanaf hier kijk hij welke structuur die gebruikt en dan zo vult ie de goede coordinaten in
    if name.lower() == 'bridge':
        site0 = structure[0].position.copy()
        site0[2] = z_top + dist_to_mxene
        view(struct + Atom('Li', position=site0, tag=1))
        print('ja')
        return(site0)
    if name.lower() == 'hollow':
        site1 = structure[2].position.copy()
        site1[2] = z_top + dist_to_mxene
        view(struct + Atom('Li', position=site1, tag=2))
        print('ja')
        return(site1)
    if name.lower() == 'halfbridge':
        site2 = (structure[0].position.copy() + structure[3].position.copy()) / 2
        site2[2] = z_top + dist_to_mxene
        view(struct + Atom('Li', position=site2, tag=3))
        print('ja')
        return(site2)
    if name.lower() == 'top':
        site3 = (structure[0].position.copy() + structure[9].position.copy() + structure[12].position.copy()) / 3
        site3[2] = z_top + dist_to_mxene
        view(struct + Atom('Li', position=site3, tag=4))
        print('ja')
        return(site3)
    # sites = np.array([site0, site1, site2, site3])
