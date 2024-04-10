# Read input blocks from input file, change block and rewrite in new file
from orcatools.inp import ORCAINP as inp
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
