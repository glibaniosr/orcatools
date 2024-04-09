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
```python
# Read input, change block and rewrite in new file
from orcatools.inp import ORCAINP

# Read input
inp = ORCAINP("B.ccd.inp")
# Change ORCA simple input block
osi = "! CCSD(T) cc-pVDZ"
inp.update_osi(osi)
# Change input name and write input file
inp.update_name("example.inp")
inp.write_input()
```

## out
The output submodule, which can read ORCA output and some of their different properties.

## tools
A submodule with a series of functions and tools to help with ORCA or molecular modeling in general.