#!/usr/bin/env python3
import os
from contextlib import contextmanager


### Context manager for changing the current working directory ###
@contextmanager
def cd(newdir):
    """
    Context manager function to enter a directory, perform tasks, and go back to previous directory.

    :param newdir:
    The directory to enter and perform tasks
    :return:
    Get back to previous directory
    """
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def get_coordinates_from_xyz(xyz):
    """
    Reads molecule from file in XYZ format if file exists, or read from xyz string otherwise, and return the coordinates in a list of lists.

    :param xyz:
        File with molecular structure in XYZ format or XYZ string.
    :return:
        The coordinates in a list of elements lists.
    """
    if xyz and os.path.isfile(xyz):
        with open(xyz, "r") as fh:
            xyzstr = "\n".join(fh.readlines()[2:])
    elif isinstance(xyz, str):
        xyzstr = xyz
    else:
        raise BaseException(
            "Your XYZ coordinates must be a .xyz formatted file or string!"
        )
    # Place xyz str in array
    coords = []
    for line in xyzstr.strip().splitlines():
        if line:
            content = line.split()
            coords.append(
                [content[0], float(content[1]), float(content[2]), float(content[3])]
            )

    return coords


def write_xyzfile_from_xyzstr(xyzstr, xyz_file, title=None):
    """
    Write a .xyz formatted file from a string block of XYZ coordinates.

    :param coords:
        A string block of XYZ coordinates.
    :param xyz_file:
        A string with the .xyz file name.
    :param title=None:
        A title for the .xyz file where default is file basename.
    """
    natoms = xyzstr.count("\n")
    if not ".xyz" in xyz_file:
        xyz_file = xyz_file + ".xyz"
    if not title:
        title = xyz_file.replace(".xyz", "")
    with open(xyz_file, "w") as out:
        out.write(str(natoms) + "\n")
        out.write(title + "\n")
        out.writelines(xyzstr)

    return


def write_xyzfile_from_coordinates(coords, xyz_file, title=None):
    """
    Write a .xyz formatted file from a list of lists containing XYZ coordinates.

    :param coords:
        A string block of XYZ coordinates.
    :param xyz_file:
        A string with the .xyz file name.
    :param title=None:
        A title for the .xyz file where default is file basename.
    """
    natoms = len(coords)
    if not ".xyz" in xyz_file:
        xyz_file = xyz_file + ".xyz"
    if not title:
        title = xyz_file.replace(".xyz", "")
    xyzstr = [
        f"{line[0]:<4s} {line[1]:10.6f} {line[2]:11.6f} {line[3]:11.6f}\n"
        for line in coords
    ]
    with open(xyz_file, "w") as out:
        out.write(str(natoms) + "\n")
        out.write(title + "\n")
        out.writelines(xyzstr)

    return


def interpolate(xyz_a, xyz_b, n_points):

    # Get all the coordinates
    if isinstance(xyz_a, list):
        coord_a = xyz_a
    else:
        coord_a = get_coordinates_from_xyz(xyz_a)

    if isinstance(xyz_b, list):
        coord_b = xyz_b
    else:
        coord_b = get_coordinates_from_xyz(xyz_b)

    n_atoms = len(coord_a)
    if len(coord_b) != n_atoms:
        print("Your .xyz files should have the same number of atoms.")
        exit()

    # Constants of the distances to interpolate the points for each atom n
    constx = []
    consty = []
    constz = []
    n = 0
    while n < n_atoms:
        constx.append((coord_b[n][1] - coord_a[n][1]) / (n_points - 1))
        consty.append((coord_b[n][2] - coord_a[n][2]) / (n_points - 1))
        constz.append((coord_b[n][3] - coord_a[n][3]) / (n_points - 1))
        n = n + 1

    # Get the distance differences for coordinates interpolation
    np = 0
    all_coords = []
    while np < n_points:
        current_coords = []
        if np == 0:
            current_coords = coord_a
        elif np == n_points - 1:
            current_coords = coord_b
        # Generate new coordinates for file n outside the two minimuns
        # New coordinates
        else:
            n = 0
            while n < n_atoms:
                coordX = np * constx[n] + coord_a[n][1]
                coordY = np * consty[n] + coord_a[n][2]
                coordZ = np * constz[n] + coord_a[n][3]
                current_coords.append([coord_a[n][0], coordX, coordY, coordZ])
                n += 1

        all_coords.append(current_coords)
        np += 1

    return all_coords
