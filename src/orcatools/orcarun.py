#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ORCA run module for managing ORCA job execution.

This submodule is for the future, as an idea to translate orca_run.sh to Python.

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

import os


def run(orcainp, orcaout=None, nprocs=None, maxcore=None, extrafiles=[]):
    command = os.popen("echo $ORCARUN").read()
    command += f" -i {orcainp} "
    if nprocs:
        command += f"-n {nprocs}"
    elif maxcore:
        command += f"-m {maxcore}"
    elif extrafiles:
        command += f'-a "{''.join(extrafiles)} "'
    elif orcaout:
        command += f"-o {orcaout}"

    os.popen(f"{command}")
