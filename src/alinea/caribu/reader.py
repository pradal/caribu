""" Readers for czribu input files
"""


def read_light(file_path):
    """Reader for *.light file format used by canestra

    Args:
        file_path: (str) a path to the file

    Returns:
        (list of tuples) a list of (Energy, (vx, vy, vz)) tuples defining light
    """

    lights = []
    with open(file_path, 'r') as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            nrj, vx, vy, vz = map(float, line.split())
            lights.append((nrj, (vx, vy, vz)))

    return lights


def read_pattern(file_path):
    """Reader for *.8 file format used by canestra

    Args:
        file_path: (str) a path to the file

    Returns:
        (tuple of floats) 2D Coordinates ( xmin, ymin, xmax, ymax) of the domain bounding the scene
    """

    pts = []
    with open(file_path, 'r') as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            x, y = map(float, line.split())
            pts.extend([x, y])

    return tuple(pts)


def read_opt(file_path):
    """Reader for *.opt file format used by canestra

    Args:
        file_path: (str) a path to the file

    Returns:
        - n (int) the number of optical species declared in the file
        - soil_reflectance (float) : the reflectance of the soil
        - opticals (dict of tuple of floats) : a {specie_id: (rho, rsup, tsup, rinf, tinf)}
         dict of optical properties for the different species
    """

    n, soil_reflectance = None, None
    eid = 0
    po = {}
    with open(file_path, 'r') as infile:
        for line in infile:
            if line.startswith('n'):
                n = int(line.split()[1])
            elif line.startswith('s'):
                soil_reflectance = float(line.split()[2])
            elif line.startswith('e'):
                eid += 1
                fields = line.split()
                opt = map(float, [fields[i] for i in (2, 4, 5, 7, 8)])
                po[eid] = tuple(opt)
            else:
                continue

    return n, soil_reflectance, po


def read_can(file_path):
    """Reader for *.can file format used by canestra

    Args:
        file_path: (str) a path to the file

    Returns:
        - labels (list of str): the barcodes associated to each triangle
        - triangles (list of list of tuples) a list of triangles, each being defined
                    by an ordered triplet of 3-tuple points coordinates.
    """

    labels = []
    triangles = []

    with open(file_path, 'r') as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            fields = line.split()
            label = fields[2]
            coords = map(float, fields[-9:])
            triangles.append(map(tuple, [coords[:3], coords[3:6], coords[6:]]))
            labels.append(label)

    return labels, triangles
