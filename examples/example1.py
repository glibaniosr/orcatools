# Create, write an input file from string blocks, and run it.
from orcatools.inp import ORCAINP

xyz = "B 0.0 0.0 0.8"
osi = "! CCSD(T) cc-pVDZ"
charge = 0
mult = 2

inp = ORCAINP("B.ccsd.inp", xyz_block=xyz, osi_block=osi, charge=charge, mult=mult)
inp.run(nprocs=2)

# help(ORCAINP)
# help(ORCAINP.run)
