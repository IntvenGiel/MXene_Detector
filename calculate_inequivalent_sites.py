from ase.io import read,write
import numpy as np
from ase import Atom
from ase.visualize import view


filename = 'CONTCAR_Ti2C-mxene-PBE'
structure = read(filename=filename, format='vasp').repeat((3,3,1))

z_top = structure[0].position.copy()[2]
dist_to_mxene = .3

site0 = structure[0].position.copy()
site0[2] = z_top + dist_to_mxene

site1 = structure[2].position.copy()
site1[2] = z_top + dist_to_mxene

site2 = (structure[0].position.copy() + structure[3].position.copy()) / 2
site2[2] = z_top + dist_to_mxene

site3 = (structure[0].position.copy() + structure[9].position.copy() + structure[12].position.copy()) / 3
site3[2] = z_top + dist_to_mxene

struct = structure.copy()
struct.pbc = False

# view(struct + Atom('Li', position=site0, tag=1))
# view(struct + Atom('Li', position=site1, tag=2))
# view(struct + Atom('Li', position=site2, tag=3))
# view(struct + Atom('Li', position=site3, tag=4))

sites = np.array([site0, site1, site2, site3])
