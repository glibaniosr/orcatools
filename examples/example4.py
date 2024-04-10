# Run direct from input file and not ORCAINP object.
from orcatools.tools import orca_run

inp = "B2.ccsd.inp"
orca_run(inp, nprocs=2, output="orca_output.log")
