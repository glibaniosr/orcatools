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
