# This submodule is for the future, as an idea to translate orca_run.sh to Python

#!/usr/bin/env python3
import os

def run(orcainp, orcaout=None, nprocs=None, maxcore=None, extrafiles=[]):
        command = os.popen("echo $ORCARUN").read()
        command += f" -i {orcainp} "
        if nprocs:
            command += f"-n {nprocs}"
        elif maxcore:
            command += f"-m {maxcore}"
        elif extrafiles:
            command += f'-a \"{''.join(extrafiles)} \"'
        elif orcaout:
            command += f"-o {orcaout}"

        os.popen(f"{command}")