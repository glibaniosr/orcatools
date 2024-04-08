#!/usr/bin/env python3
import os
import subprocess as sub
from orcatools.tools import get_coordinates_from_xyz


# ----- General Functions
def get_input_block(block):
    if block and os.path.exists(block):
        with open(block, "r") as inp:
            block = inp.read()
    return block


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
        xyz_block,
        osi_block,
        obl_block=None,
        charge=0,
        mult=1,
        guess_file=None,
        # For the future
        # nprocs=None,
        # maxcore=None
    ):
        # Basename for input file
        self.basename = orcainp_name.replace(".inp", "")
        # Get input file name
        self.orcainp_name = orcainp_name
        # Get coordinates from .xyz file
        if isinstance(xyz_block, list):
            self.coordinates = xyz_block
        else:
            self.coordinates = get_coordinates_from_xyz(xyz_block)
        # Get OSI and OBL input-blocks
        self.osi_block = get_input_block(osi_block)
        self.obl_block = get_input_block(obl_block)
        # Charge and multiplicity
        self.charge = charge
        self.mult = mult
        self.guess_file = guess_file
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

    def run(self, output=None, nprocs=None, maxcore=None, extrafiles=[]):
        if not os.path.exists(self.orcainp_name):
            self.write_input()

        try:
            os.environ(["ORCAPATH"])
            os.environ(["ORCASCR"])
        except:
            print(
                'To use orca-run you need to first export ORCAPATH and ORCASCR variables in your enviroment. Example:\nexport ORCAPATH="/path/to/orca"\n export ORCASCR="/tmp/orca".'
            )
            exit()

        command = f"{os.path.dirname(__file__)}/orca_run.sh"
        command += f" -i {self.orcainp_name} "
        if output:
            command += f" -o {self.basename+'.out'}"
        if nprocs:
            command += f"-p {nprocs} "
        elif maxcore:
            command += f"-m {maxcore} "
        elif extrafiles:
            command += f'-a \"{''.join(extrafiles)} \"'

        sub.Popen(command.split(), stdout=sub.PIPE)

        return 