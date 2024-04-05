#!/usr/bin/env python3
import os
from orcatools.tools import get_coordinates_from_xyz


# ----- General Functions
def __get_input_block(block):
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
        xyz_block,
        osi_block,
        obl_block,
        orcainp_name,
        charge=0,
        mult=1,
        guess_file=None,
    ):
        # Basename for input file
        basename = orcainp_name.replace(".inp", "")
        # Get input file name
        self.orcainp_name = orcainp_name
        # Get coordinates from .xyz file
        if isinstance(xyz_block, list):
            self.coordinates = xyz_block
        else:
            self.coordinates = get_coordinates_from_xyz(xyz_block)
        # Get OSI and OBL input-blocks
        self.osi_block = __get_input_block(osi_block)
        self.obl_block = __get_input_block(obl_block)
        # Charge and multiplicity
        self.charge = charge
        self.mult = mult
        self.guess_file = guess_file

    def write_input(self):
        """
        Write a ORCA input file from ORCAINP object.
        """
        input_blocks = f"{self.osi_block}\n{self.obl_block}\n"
        if self.guess_file:
            input_blocks = f'{input_blocks}!MORead\n%moinp "{self.guess_file}"\n\n'
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
