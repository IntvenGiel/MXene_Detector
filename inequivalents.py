def calculate(structure, distance):
    z_top = structure[0].position.copy()[2]

    site0 = structure[0].position.copy()
    site0[2] = z_top + distance

    site1 = structure[2].position.copy()
    site1[2] = z_top + distance

    site2 = (structure[0].position.copy() + structure[3].position.copy()) / 2
    site2[2] = z_top + distance

    site3 = (structure[0].position.copy() + structure[9].position.copy() + structure[12].position.copy()) / 3
    site3[2] = z_top + distance

    return [site0, site1, site2, site3]