#!/usr/bin/env python3
import os
from contextlib import contextmanager


# ----- Functions
def get_coordinates_from_xyz(xyz):
    """
    Reads molecule from file in XYZ format if file exists, or read from xyz string otherwise, and return the coordinates in a list of lists.

    :param xyz:
        File with molecular structure in XYZ format or XYZ string.
    :return:
        The coordinates in a list of elements lists.
    """
    if xyz and os.path.exists(xyz):
        with open(xyz, "r") as fh:
            xyzstr = "\n".join(fh.readlines()[2:])
    else:
        xyzstr = xyz
    # Place xyz str in array
    coords = []
    for line in xyzstr.strip().splitlines():
        if line:
            content = line.split()
            coords.append(
                [content[0], float(content[1]), float(content[2]), float(content[3])]
            )
    return coords


def write_xyzfile_from_xyz(xyzstr, xyz_file, title=None):
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
        out.write(natoms)
        out.write(title)
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
    natoms = len(coords.count)
    if not ".xyz" in xyz_file:
        xyz_file = xyz_file + ".xyz"
    if not title:
        title = xyz_file.replace(".xyz", "")
    xyzstr = [
        f"{line[0]:<6s} {line[1]:10.5f} {line[2]:10.5f} {line[3]:10.5f}\n"
        for line in coords
    ]
    with open(xyz_file, "w") as out:
        out.write(natoms)
        out.write(title)
        out.writelines(xyzstr)

    return


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


def interpolate(file_a, file_b, n_points):

    ### Internal variables ###
    coord_a = []
    coord_b = []
    all_inp_a = []
    all_inp_b = []

    # Get all the coordinates
    coord_a = get_coordinates_from_xyz(file_a)
    coord_b = get_coordinates_from_xyz(file_b)
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
