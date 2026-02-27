#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ORCA Tools - Python module for ORCA quantum chemistry calculations.

Copyright (C) 2026 Gabriel Libânio Silva Rodrigues

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# Version of the orcatools package
__version__ = "0.5.0"
__author__ = "Gabriel Libânio Silva Rodrigues"
__license__ = "GPL-3.0-or-later"

# Import main classes
from orcatools.inp import ORCAINP
from orcatools.out import ORCAOUT

# Import utility functions
from orcatools.tools import (
    get_coordinates_from_xyz,
    write_xyzfile_from_xyzstr,
    write_xyzfile_from_coordinates,
    cd,
    interpolate,
    get_input_blocks_from_file,
    plot_orbitals,
    orbital_viewer,
    orca_run,
)

__all__ = [
    # Main classes
    "ORCAINP",
    "ORCAOUT",
    # Utility functions
    "get_coordinates_from_xyz",
    "write_xyzfile_from_xyzstr",
    "write_xyzfile_from_coordinates",
    "cd",
    "interpolate",
    "get_input_blocks_from_file",
    "plot_orbitals",
    "orbital_viewer",
    "orca_run",
    # Package metadata
    "__version__",
    "__author__",
    "__license__",
]
