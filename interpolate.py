#!/usr/bin/env python3

##################################################################################################
###### This script was written by Gabriel Libânio Silva Rodrigues (Gabriel L. S. Rodrigues) ######
##################################################################################################

# This module takes two .xyz files from two different eletronic states and generate structures
# for a PES calculation in ORCA.

# Imports
from tools import cd, get_coordinates_from_xyz
from inp import ORCAINP as oinp
import os


def interpolate(file_a, file_b, n_points, pes_xyz_file=None):
    # ### External input, get parameters ###

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

        # # Write the new coordinates in the .inp files
        # with cd(dir_a):  # Files 1
        #     with open(all_inp_a[np], "a") as output:
        #         output.write("\n")
        #         for lines in current_coords:
        #             output.write(
        #                 "{0:3s} {1:14f} {2:14f} {3:14f}".format(
        #                     lines[0], lines[1], lines[2], lines[3]
        #                 )
        #             )
        #             output.write("\n")
        #             # Write the bottom of the file
        #         output.write(
        #             "*\n"
        #         )  # Later add the option to write contents of the file
        # with cd(dir_b):  # Files 2
        #     with open(all_inp_b[np], "a") as output:
        #         output.write("\n")
        #         for lines in current_coords:
        #             output.write(
        #                 "{0:3s} {1:14f} {2:14f} {3:14f}".format(
        #                     lines[0], lines[1], lines[2], lines[3]
        #                 )
        #             )
        #             output.write("\n")
        #             # Write the bottom of the file
        #         output.write(
        #             "*\n"
        #         )  # Later add the option to write contents of the file

        # if pes_xyz_file:
        #     # Write current coordinates to the file with all coordinates if requested.
        #     with open(pes_xyz_file, "w") as output:
        #         for coords in all_coords:
        #             output.write(f"{str(n_atoms)}\n")
        #             output.write(f"PES calculation step {np}\n")
        #             for lines in coords:
        #                 output.write(
        #                     f"{lines[0]:3s} {lines[1]:14f} {lines[2]:14f} {lines[3]:14f}\n"
        #                     )
        #             if np != n_points:
        #                 output.write(">\n")
