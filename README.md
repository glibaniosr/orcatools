# ORCA tools
##### --- by Gabriel Libânio Silva Rodrigues

ORCA tools is a Python module developed to to help users run electronic structure calculations with ORCA software. I plan to sporadically update the scripts and add more functionalities as I need them. But anyone is welcome to maybe request something interesting.

ORCA is developed and maintained by prof. Frank Neese and coworkers at Max Planck Institute for Chemical Energy Conversion. It's official website can be accessed at: https://orcaforum.kofo.mpg.de

About ORCA software for electronic structures calculations
The following text was taken from ORCA official website above.

"The program ORCA is a modern electronic structure program package written by F. Neese, with contributions from many current and former coworkers and several collaborating groups. The binaries of ORCA are available free of charge for academic users for a variety of platforms. ORCA is a flexible, efficient and easy-to-use general purpose tool for quantum chemistry with specific emphasis on spectroscopic properties of open-shell molecules. It features a wide variety of standard quantum chemical methods ranging from semi-empirical methods to DFT to single- and multireference correlated ab initio methods. It can also treat environmental and relativistic effects. Due to the user-friendly style, ORCA is considered to be a helpful tool not only for computational chemists, but also for chemists, physicists and biologists that are interested in developing the full information content of their experimental data with help of calculations."

More help using ORCA can be found at ORCA Input Library: https://sites.google.com/site/orcainputlibrary/

## inp
The input submodule, which can create ORCA inputs and control their properties.

Examples:

### Create, write an input file from string blocks, and run it.
```python
from orcatools.inp import ORCAINP
xyz = "B 0.0 0.0 0.8"
osi = "! CCSD(T) cc-pVDZ"
charge = 0
mult = 2

inp = ORCAINP("B.ccsd.inp", xyz_block=xyz, osi_block=osi, charge=charge, mult=mult)
inp.run(nprocs=2)

#help(ORCAINP)
#help(ORCAINP.run)
```

### Read input blocks from input file, change block and rewrite in new file
```python
from orcatools.inp import ORCAINP
from orcatools.tools import get_input_blocks_from_file

# Read input
osi, obl, xyz, charge, mult = get_input_blocks_from_file("B.ccsd.inp")
# Change ORCA input blocks
osi = "! CCSD(T) cc-pVTZ\n"
obl = "%scf MaxIter 250 end"
xyz = inp.xyzstr
xyz += "B 0.0 0.0 -0.8"

# Update input blocks
inp.update_osi(osi)
inp.update_obl(obl)
inp.update_xyz(xyz)
inp.update_name("B2.ccsd.inp")
inp.update_mult(3)
inp.write_input()

# help(ORCAINP.update_name)
# help(ORCAINP.update_osi)
# help(ORCAINP.update_obl)
# help(ORCAINP.update_xyz)
```

### Help on module orcatools.inp in orcatools:

NAME
    orcatools.inp

CLASSES
    builtins.object
        ORCAINP

    class ORCAINP(builtins.object)
     |  ORCAINP(orcainp_name, xyz_block, osi_block, obl_block=None, charge=0, mult=1, guess_file=None)
     |
     |  Class which holds information for a ORCA input object.
     |
     |  :param xyz_block:
     |      A string block, a .xyz formatted file with xyz coordinates, or a ORCAOUT xyz_coords list.
     |  :param osi_block:
     |      A string block or file with ORCA simple input keywords. i.e. ! B3LYP def2-TZVP.
     |  :param obl_block:
     |      A string block or file with ORCA % input blocks. i.e. %scf MaxIter 250 end.
     |  :param orcainp_name:
     |      A string with the name of the ORCA input file.
     |  :param charge=0:
     |      Input molecule charge.
     |  :param mult=1:
     |      Input molecule multiplicity.
     |  :param guess_file=None:
     |      A string with the name of a file used for starting orbitals. Such as .gbw, .uno, etc.
     |
     |  Methods defined here:
     |
     |  __init__(self, orcainp_name, xyz_block, osi_block, obl_block=None, charge=0, mult=1, guess_file=None)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  add_atoms(self, atoms)
     |      Add atoms to ORCAINP object.
     |
     |      :param atoms:
     |          A list of atoms to add to ORCAINP object in the format [symbol, x, y, z].
     |
     |  change_to_dummy_atoms(self, start_index, end_index)
     |      Change regular atoms to dummy atoms in ORCAINP object.
     |
     |      :param start_index:
     |          Index to start dummy atoms (counting start from 0).
     |      :param end_index:
     |          Index to end dummy atoms.
     |
     |  run(self, nprocs=None, maxcore=None, output=None, extrafiles=[], orcarun=None, orca_command=None)
     |      Run ORCA calculation from an ORCAINP object, writing the input, either by the orca_run.sh script or by supplying a command to run ORCA directly.
     |
     |      :param nprocs:
     |          Number of cores to run.
     |      :param maxcore:
     |          Memory per core in MB.
     |      :param output:
     |         Output file name.
     |      :param [extrafile]:
     |          A list containing extra files to run ORCA, such as .gbw and .xyz.
     |      :param orcarun:
     |          Full path to orca_run.sh script. Default: orcatools orca_run.sh script.
     |      :param orca_command:
     |          Full command in order to run ORCA, in case orca_run.sh is not to be used.
     |
     |  update_charge(self, charge)
     |      Updates charge.
     |
     |  update_guess(self, guess_file)
     |      Updates guess file.
     |
     |  update_mult(self, mult)
     |      Updates multiplicity.
     |
     |  update_name(self, newname)
     |      Updates input name with newname.
     |
     |  update_obl(self, obl_block)
     |      Updates obl (ORCA % input) blocks.
     |
     |  update_osi(self, osi_block)
     |      Updates osi (ORCA simple input !) blocks.
     |
     |  update_xyz(self, xyzstr)
     |      Updates xyz coordinates.
     |
     |  write_input(self)
     |      Write a ORCA input file from ORCAINP object.
     |
     |  ----------------------------------------------------------------------

## out
The output submodule, which can read ORCA output and some of their different properties.

Examples:

```python
import orcatools as ot
from orcatools.out import ORCAOUT
from orcatools.tools import interpolate

xyz_a = ORCAOUT("a.out").xyz_coords
xyz_b = ORCAOUT("b.out").xyz_str

xyzs = interpolate(xyz_a, xyz_b, 5)

for idx,coords in enumerate(xyzs):
   ot.tools.write_xyzfile_from_coordinates(coords, f"xyzs/xyz_{idx+1:02d}.xyz")

# help(ORCAOUT)
# help(interpolate)
```
### Help on module orcatools.out in orcatools:

NAME
    orcatools.out

CLASSES
    builtins.object
        ORCAOUT

    class ORCAOUT(builtins.object)
     |  ORCAOUT(orcaout_name, verbose=False, function_mode=False)
     |
     |  Class which holds information for a ORCA input object.
     |
     |  :param orcaout_name:
     |      A string with the name of the output file.
     |  :param verbose=False:
     |      Specify verbosity when starting the ORCAOUT class.
     |  :param function_mode=False:
     |      Activate function mode, where attributes are not gathered at __init__. Useful for saving time when specific functions are requested.
     |
     |  :attribute runtime:
     |      The runtime of the calculation.
     |  :attribute optimization:
     |      Boolean that tells if the calculation is an optimization.
     |  :attribute scf_energy:
     |      The final SCF energy.
     |  :attribute coordinates:
     |      The final coordinates of the system.
     |  :attribute xyzstr:
     |      The final coordinates of the system in string format.
     |
     |  Methods defined here:
     |
     |  __init__(self, orcaout_name, verbose=False, function_mode=False)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  get_absorption_data(self, unit='eV')
     |      Function that returns the absorption energies and oscillator strengths from the output file.
     |
     |      :param unit="eV" - The unit of the absorption energies. Options are "cm" (cm-1), "nm" and "eV".
     |
     |      :return: Tuple with two lists: (energies, fosc)
     |
     |      1. Absorption energies
     |      2. Oscillator strengths
     |
     |  get_cc_diagnostic(self, extrapolation=False)
     |      Function that returns the CCSD or CCSD(T) parameters from the output file.
     |
     |      :param
     |          extrapolation=False - Change to True if your calculation uses basis set extrapolation.
     |
     |      :return:
     |          Dictionary with the following keys:
     |          "corr" - Correlation energy
     |          "t1" - T1 diagnostic
     |          "ccsd" - CCSD energy
     |
     |  get_correlation_cbs(self)
     |      Function that returns the CBS correlation energy from the output file.
     |
     |  get_mcscf_correlation(self)
     |      Function that returns the MCSCF correlation energy from the output file.
     |
     |      :return: Dictionary with the following keys:
     |      "casscf" - CASSCF energy
     |      "corr" - Correlation energy
     |
     |  get_nfod(self)
     |      Function that returns the fraction occupation density (FOD) number from the output file.
     |
     |  get_thermal_corrections(self)
     |      Function that returns a dictionary with the thermal correction data from the output file.
     |
     |      :return:
     |          A dictionary with the following keys:
     |          "ZPE" - Zero Point Energy
     |          "U" - Internal Energy
     |          "H" - Enthalpy
     |          "S" - Entropy
     |          "G" - Gibbs Free Energy
     |
     |  ----------------------------------------------------------------------


## tools
A submodule with a series of functions and tools to help with ORCA or molecular modeling in general.

Examples:

### Use the supplied orca_run.sh script to run a calculation from a Python script and an input file.
```python
from orcatools.tools import orca_run

inp = "B2.ccsd.inp"
# If you want to use the supplied orca_run.sh script (also in my GitHub)
orca_run(inp, nprocs=2, output="orca_output.log")
# If you want to run ORCA yourself
orca_run(inp, orca_command=f"orca {inp} > output.out")

# help(orca_run)
```
### Help on module orcatools.tools in orcatools:

NAME
    orcatools.tools

FUNCTIONS

    get_coordinates_from_xyz(xyz)
        Reads molecule from file in XYZ format if file exists, or read from xyz string otherwise, and return the coordinates in a list of lists.

        :param xyz:
            File with molecular structure in XYZ format or XYZ string.
        :return coordinates, xyzstr:
            The coordinates in a list of elements lists and the XYZ string.

    get_input_blocks_from_file(orcainp_name, verbose=False)

    interpolate(xyz_a, xyz_b, npoints)
        Interpolate the coordinates from two .xyz files through npoints returning a list of the interpolated coordinates.

        :param xyz_a:
            A string block, .xyz file, or ORCAOUT list with XYZ coordinates.
        :param xyz_file:
            A second string block, .xyz file, or ORCAOUT list with XYZ coordinates.
        :param npoints:
            Number of interpolation points

    orca_run(orcainp, nprocs=None, maxcore=None, output=None, extrafiles=None, orcarun=None, orca_command=None)
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

    plot_orbitals(gbw_file, orb, grid_dens=40, orca_plot_path=None)
        Plot the molecular orbitals from a .gbw file in the range of orbitals.

        :param gbw_file:
            A string with the .gbw file name.
        :param orb:
            A single molecular orbital number or a tuple with the range of orbitals to plot.
        :param grid_dens:
            A string with the grid density to plot the orbitals.
        :param orca_plot_path:
            A string with the path to the orca_plot executable.

    write_xyzfile_from_coordinates(coords, xyz_file, title=None)
        Write a .xyz formatted file from a list of lists containing XYZ coordinates.

        :param coords:
            A string block of XYZ coordinates.
        :param xyz_file:
            A string with the .xyz file name.
        :param title=None:
            A title for the .xyz file where default is file basename.

    write_xyzfile_from_xyzstr(xyzstr, xyz_file, title=None)
        Write a .xyz formatted file from a string block of XYZ coordinates.

        :param coords:
            A string block of XYZ coordinates.
        :param xyz_file:
            A string with the .xyz file name.
        :param title=None:
            A title for the .xyz file where default is file basename.
