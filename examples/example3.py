# Interpolate coordinates from two output files and write xyz files.
import orcatools as ot
from orcatools.out import ORCAOUT
from orcatools.tools import interpolate

xyz_a = ORCAOUT("a.out").xyz_coords
xyz_b = ORCAOUT("b.out").xyz_str

xyzs = interpolate(xyz_a, xyz_b, 5)

for idx, coords in enumerate(xyzs):
    ot.tools.write_xyzfile_from_coordinates(coords, f"xyzs/xyz_{idx+1:02d}.xyz")

# help(ORCAOUT)
# help(interpolate)
