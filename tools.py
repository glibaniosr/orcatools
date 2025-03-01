#!/usr/bin/env python3
import os, sys
import subprocess as sub
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
    :return coordinates, xyzstr:
        The coordinates in a list of elements lists and the XYZ string.
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
    coordinates = []
    for line in xyzstr.strip().splitlines():
        if line:
            content = line.split()
            coordinates.append(
                [content[0], float(content[1]), float(content[2]), float(content[3])]
            )
    # Standardize xyz string
    xyzstr = ""
    for line in coordinates:
        xyzstr += f"{line[0]:<6s} {line[1]:10.5f} {line[2]:10.5f} {line[3]:10.5f}\n"

    return coordinates, xyzstr


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


def interpolate(xyz_a, xyz_b, npoints):
    """
    Interpolate the coordinates from two .xyz files through npoints returning a list of the interpolated coordinates.

    :param xyz_a:
        A string block, .xyz file, or ORCAOUT list with XYZ coordinates.
    :param xyz_file:
        A second string block, .xyz file, or ORCAOUT list with XYZ coordinates.
    :param npoints:
        Number of interpolation points
    """
    # Get all the coordinates
    if isinstance(xyz_a, list):
        coord_a = xyz_a
    else:
        coord_a = get_coordinates_from_xyz(xyz_a)[0]

    if isinstance(xyz_b, list):
        coord_b = xyz_b
    else:
        coord_b = get_coordinates_from_xyz(xyz_b)[0]

    natoms = len(coord_a)
    # print("a ",natoms)
    # print("b ", len(coord_b))
    if len(coord_b) != natoms:
        print("Your .xyz files should have the same number of atoms.")
        sys.exit()

    # Constants of the distances to interpolate the points for each atom n
    constx = []
    consty = []
    constz = []
    n = 0
    while n < natoms:
        constx.append((coord_b[n][1] - coord_a[n][1]) / (npoints - 1))
        consty.append((coord_b[n][2] - coord_a[n][2]) / (npoints - 1))
        constz.append((coord_b[n][3] - coord_a[n][3]) / (npoints - 1))
        n = n + 1

    # Get the distance differences for coordinates interpolation
    np = 0
    all_coords = []
    while np < npoints:
        current_coords = []
        if np == 0:
            current_coords = coord_a
        elif np == npoints - 1:
            current_coords = coord_b
        # Generate new coordinates for file n outside the two minimuns
        # New coordinates
        else:
            n = 0
            while n < natoms:
                coordX = np * constx[n] + coord_a[n][1]
                coordY = np * consty[n] + coord_a[n][2]
                coordZ = np * constz[n] + coord_a[n][3]
                current_coords.append([coord_a[n][0], coordX, coordY, coordZ])
                n += 1

        all_coords.append(current_coords)
        np += 1

    return all_coords


def get_input_blocks_from_file(orcainp_name, verbose=False):
    obl_block = ""
    osi_block = ""
    xyzstr = ""
    charge = 0
    mult = 1
    inside_obl_block = False
    with open(orcainp_name, "r") as data:
        for line in data:
            if "!" in line:
                osi_block += line
            elif "%" in line:
                if not inside_obl_block:
                    inside_obl_block = True
                obl_block += line
            elif inside_obl_block:
                obl_block += line
            elif inside_obl_block and any(char in line for char in "*%!"):
                inside_obl_block = False
            if "*" in line:
                charge = line.split()[2]
                mult = line.split()[3]
                for line in data:
                    if "*" not in line:
                        xyzstr += line
                    else:
                        break
        if verbose:
            print("osi: ", osi_block)
            print("obl: ", obl_block)
            print("xyz ", xyzstr)
            print(f"Charge: {charge}\nMult: {mult}")

    return osi_block, obl_block, xyzstr, charge, mult


def plot_orbitals(gbw_file, orb, grid_dens=40, orca_plot_path=None, verbose=False):
    """
    Plot the molecular orbitals from a .gbw file in the range of orbitals.

    :param gbw_file:
        A string with the .gbw file name.
    :param orb:
        A single molecular orbital number or a tuple with the range of orbitals to plot.
    :param grid_dens:
        A string with the grid density to plot the orbitals.
    :param orca_plot_path:
        A string with the path to the orca_plot executable.
    """
    if not os.path.isfile(gbw_file):
        raise BaseException("The .gbw file does not exist!")
    if not orca_plot_path:
        raise BaseException("The path to the orca_plot executable is not defined!")

    log_file = gbw_file.replace(".gbw", f"_plot.log")

    if isinstance(orb, tuple):
        orbital_range = range(orb[0], orb[1] + 1)
    else:
        orbital_range = [orb]

    with open(log_file, "w") as stdout:
        for orbital in orbital_range:
            if verbose:
                print(f"Plotting Orbital = {orbital}, Grid-Density = {grid_dens} ...")
            
            command = f"{orca_plot_path} {gbw_file} -i"
            input_data = f"2\n{orbital}\n4\n{grid_dens}\n5\n7\n10\n11\n"  
            stdout.write(
                f"\n\n######################\n##### Orbital {orbital} #####\n######################\n\n"
            )
            stdout.flush()

            result = sub.run(
                command,
                input=input_data,
                text=True,
                shell=True,
                stdout=stdout,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"Command failed with return code {result.returncode}"
                )
                
def orbital_viewer(cube, isovalue=0.03, resolution=1.00):
    """
    View the molecular orbitals from a specified .cube file.
    
    :param cube:
        A string with the .cube file name.
    :param isovalue=0.03:
        A float with the isovalue to plot the orbitals.
        
        Requires py3Dmol package.
    """
    try:
        import py3Dmol as p3d
    except ImportError:"py3Dmol package is not installed. Please install it with 'pip install py3Dmol' or 'conda -c conda-forge install py3Dmol'."
    
    if not os.path.isfile(cube):
        raise BaseException("The .cube file does not exist!")
    
    viewer = p3d.view()
    viewer.addModel(open(cube).read(), "cube")
    viewer.setStyle({'stick': {}})
    viewer.addVolumetricData(open(cube).read(), "cube", {'isoval': isovalue, 'color': 'blue', "opacity": 0.85, "resolution": resolution })
    viewer.addVolumetricData(open(cube).read(), "cube", {'isoval': -isovalue, 'color': 'red', "opacity": 0.85, "resolution": resolution })
    viewer.zoomTo()
    # view.show()
    
    return viewer


def orca_run(
    orcainp,
    nprocs=None,
    maxcore=None,
    output=None,
    extrafiles=None,
    orcarun=None,
    orca_command=None,
):
    """
    Run ORCA calculation from an ORCA input file, either by orca_run.sh script or by supplying a command to run ORCA directly.

    :param nprocs:
        Number of cores to run.
    :param maxcore:
        Memory per core in MB.
    :param output:
       Output file name.
    :param [extrafile]:
        A list containing extra files to run ORCA, such as .gbw and .xyz.
    :param orcarun:
        Full path to orca_run.sh script. Default: orcatools orca_run.sh script.
    :param orca_command:
        Full command in order to run ORCA, in case orca_run.sh is not to be used.
    """
    if not os.path.isfile(orcainp):
        raise BaseException("ORCA input file does not exists!")

    if orca_command:
        command = orca_command
    else:
        if orcarun:
            command = orcarun
        else:
            command = f"{os.path.dirname(__file__)}/orca_run.sh"
        command += f" -i {orcainp}"
        if nprocs:
            command += f" -p {nprocs}"
        if maxcore:
            command += f" -m {maxcore}"
        if output:
            command += f" -o {output}"
        if extrafiles:
            files = " ".join(extrafiles)
            command += f" -a  {files}"

    sub.run(command.split())
