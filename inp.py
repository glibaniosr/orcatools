#!/usr/bin/env python3
import os
import subprocess as sub
from orcatools.tools import get_coordinates_from_xyz


# ----- General Functions
def _get_input_block(block):
    if block and os.path.exists(block):
        with open(block, "r") as inp:
            block = inp.read()
    return block

def _get_input_blocks_from_file(orcainp_name, verbose=False):
    obl_block = ""
    osi_block = ""
    xyzstr = ""
    charge = 0
    mult = 1
    with open(orcainp_name, 'r') as data:
        for line in data:
            if "!" in line:
                osi_block += line
            elif "%" in line:
                obl_block += line
                for line in data:
                    # Here we have a problem with keywords that also have and additional "end" inside a % block.
                    if "end" not in line:
                        obl_block += line
                        continue
                    else:
                        break
            if "*" in line:
                charge = line.split()[2]
                mult = line.split()[3]
                for line in data:
                    if "*" not in line:
                        xyzstr += line
                        continue
                    else:
                        break
        if verbose:
            print("osi: ",osi_block)
            print("obl: ",obl_block)
            print("xyz ", xyzstr)
            print(f"Charge: {charge}\nMult: {mult}")
    return osi_block, obl_block, xyzstr, charge, mult


# ----- Define the INPUT class
# OSI = Orca Simple Input
# OBL = Orca Blocks
class ORCAINP:
    """
    Class which holds information for a ORCA input object.

    :param xyz_block:
        A string block, a .xyz formatted file with xyz coordinates, or a ORCAOUT xyz_coords list.
    :param osi_block:
        A string block or file with ORCA simple input keywords. i.e. ! B3LYP def2-TZVP.
    :param obl_block:
        A string block or file with ORCA % input blocks. i.e. %scf MaxIter 250 end.
    :param orcainp_name:
        A string with the name of the ORCA input file.
    :param charge=0:
        Input molecule charge.
    :param mult=1:
        Input molecule multiplicity.
    :param guess_file=None:
        A string with the name of a file used for starting orbitals. Such as .gbw, .uno, etc.
    """

    def __init__(
        self,
        orcainp_name,
        xyz_block=None,
        osi_block=None,
        obl_block=None,
        charge=0,
        mult=1,
        guess_file=None,
        verbose=False
        # For the future
        # nprocs=None,
        # maxcore=None
    ):
        # Basename for input file
        self.basename = orcainp_name.replace(".inp", "")
        # Get input file name and parameters if is a file with ORCA input
        self.orcainp_name = orcainp_name
        if os.path.isfile(orcainp_name):
            osi_block, obl_block, xyz_block, charge, mult = _get_input_blocks_from_file(orcainp_name, verbose)
        # Get OSI and OBL input-blocks
        self.osi_block = _get_input_block(osi_block)
        self.obl_block = _get_input_block(obl_block)
        # Charge and multiplicity
        self.charge = charge
        self.mult = mult
        self.guess_file = guess_file
        # Get coordinates from .xyz file
        if isinstance(xyz_block, list):
            self.coordinates = xyz_block
        else:
            self.coordinates = get_coordinates_from_xyz(xyz_block)

        # For the future
        # self.nprocs = nprocs
        # self.maxcore = maxcore

    def write_input(self):
        """
        Write a ORCA input file from ORCAINP object.
        """
        input_blocks = ""

        # For future orca_run in Python
        # if self.nprocs:
        #     input_blocks += f"%pal {self.nprocs}\n"
        # if self.maxcore:
        #     input_blocks += f"%maxcore {self.maxcore}\n"

        input_blocks += f"{self.osi_block}\n"
        if self.obl_block:
            input_blocks += f"{self.obl_block}\n"
        if self.guess_file:
            input_blocks += f'!MORead\n%moinp "{self.guess_file}"\n'
        input_blocks += "\n"
        header = f"{input_blocks}* xyz {self.charge} {self.mult}\n"
        xyzstr = [
            f"{line[0]:<6s} {line[1]:10.5f} {line[2]:10.5f} {line[3]:10.5f}\n"
            for line in self.coordinates
        ]
        filename = self.orcainp_name

        with open(filename, "w") as out:
            out.write(header)
            for line in xyzstr:
                out.write(line)
            out.write("*")

    def update_name(self, newname):
        """
        Updates input name with newname.
        """
        self.orcainp_name = newname
    
    def update_osi(self, osi_block):
        """
        Updates osi (ORCA simple input !) blocks.
        """
        self.osi_block = osi_block

    def update_obl(self, obl_block):
        """
        Updates obl (ORCA % input) blocks.
        """
        self.osi_block = obl_block

    def update_xyz(self, xyzstr):
        """
        Updates xyz coordinates.
        """
        self.coordinates = get_coordinates_from_xyz(xyzstr)

    def run(self, nprocs=None, maxcore=None, output=None, extrafiles=[], orcarun=None, orca_command=None):
        """
        Run ORCA calculation from an ORCAINP object, writing the input, either by the orca_run.sh script or by supplying a command to run ORCA directly.

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
        self.write_input()
        if orca_command:
            command = orca_command
        else:
            if orcarun:
                command = orcarun
            else:
                if orcarun:
                    command = orcarun
                else:
                    command = f"{os.path.dirname(__file__)}/orca_run.sh"
                command += f" -i {self.orcainp_name}"
                if output:
                    command += f" -o {output}"
                if nprocs:
                    command += f" -p {nprocs}"
                elif maxcore:
                    command += f" -m {maxcore}"
                elif extrafiles:
                    command += f' -a \"{''.join(extrafiles)} \"'

        sub.Popen(command.split())

        return 