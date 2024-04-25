#!/usr/bin/env python3
import os


def _check_normal_termination(orcaout_name):
    normal_termination = False
    runtime = 0
    lines = os.popen(f"tail -n 2 {orcaout_name}").read().split("\n")
    if "ORCA TERMINATED NORMALLY" in lines[0]:
        normal_termination = True
        clock = lines[1].split()[3:]
        runtime = (
            float(clock[0]) * 86400
            + float(clock[2]) * 3600
            + float(clock[4]) * 60
            + float(clock[6])
            + float(clock[8]) / 1000
        )

    return normal_termination, runtime


def _get_basic_properties(orcaout_name):
    optimization = False
    scf_energy = 0
    coords = []
    xyzstr = ""
    with open(orcaout_name, "r", encoding="utf8", errors="ignore") as out_file:
        # Check opt
        for line in out_file:
            if "END OF INPUT" in line:
                for idx, line in enumerate(out_file):
                    if idx == 3:
                        if "Geometry Optimization Run" in line:
                            optimization = True
                            continue
            # Get SCF energy and coords
            if optimization:
                for line in out_file:
                    if "HURRAY" in line:
                        for line in out_file:
                            if "CARTESIAN COORDINATES (ANGSTROEM)" in line:
                                for line in out_file:
                                    if "---" in line:
                                        continue
                                    if line and line != "\n":
                                        xyzstr += line.strip() + "\n"
                                        content = line.split()
                                        coords.append(
                                            [
                                                content[0],
                                                float(content[1]),
                                                float(content[2]),
                                                float(content[3]),
                                            ]
                                        )
                                    else:
                                        for line in out_file:
                                            if "FINAL SINGLE POINT ENERGY" in line:
                                                scf_energy = float(line.split()[4])
                                                break

            else:
                for line in out_file:
                    if "CARTESIAN COORDINATES (ANGSTROEM)" in line:
                        for line in out_file:
                            if "---" in line:
                                continue
                            if line and line != "\n":
                                xyzstr += line.strip() + "\n"
                                content = line.split()
                                coords.append(
                                    [
                                        content[0],
                                        float(content[1]),
                                        float(content[2]),
                                        float(content[3]),
                                    ]
                                )
                            else:
                                for line in out_file:
                                    if "FINAL SINGLE POINT ENERGY" in line:
                                        scf_energy = float(line.split()[4])
                                        break

    return optimization, scf_energy, coords, xyzstr


# ----- Define the OUTPUT class
class ORCAOUT:
    """
    Class which holds information for a ORCA input object.

    :param orcaout_name:
        A string with the name of the output file.
    :param verbose=False:
        Specify verbosity when starting the ORCAOUT class.
    """

    def __init__(self, orcaout_name, verbose=False):
        self.orcaout_name = orcaout_name
        orca_normal_termination, self.runtime = _check_normal_termination(orcaout_name)
        if not orca_normal_termination:
            raise BaseException(
                """You ORCA output file did not have a normal termination! Check your calculation and try again.
            """
            )
        self.optimization, self.scf_energy, self.coordinates, self.xyzstr = (
            _get_basic_properties(orcaout_name)
        )
        if verbose:
            print(f"Orca Output -> {orcaout_name}")
            if self.optimization:
                print("Optimization Run")
            else:
                print("Single Point Energy Run")
            print(f"(Final) Geometry: \n{self.xyzstr}")
            print(f"Final SCF Energy (Hartree) = {self.scf_energy:.12f}")
            print(f"Calculation Time = {self.runtime} s")

    def get_thermal_corrections(self):

        with open(self.orcaout_name, "r", encoding="utf8", errors="ignore") as out_file:
            dic = None
            for line in out_file:
                if "Zero point energy" in line:
                    zpe = float(line.strip().split()[-4])
                if "Total correction" in line:
                    u_correction = float(line.strip().split()[-4])
                if "Thermal Enthalpy correction" in line:
                    kbt_correction = float(line.strip().split()[-4])
                    h_correction = u_correction + kbt_correction
                if "Final entropy term" in line:
                    s_correction = float(line.strip().split()[-4])
                if "G-E(el)" in line:
                    g_correction = float(line.strip().split()[-4])
            try:
                dic = {
                    "ZPE": zpe,
                    "U": u_correction,
                    "H": h_correction,
                    "S": s_correction,
                    "G": g_correction,
                }
            except:
                raise BaseException(
                    "We did not find vibrational data in your output. Check your calculation!"
                )

        return dic

    def get_correlation_cbs(self):

        correction = None
        with open(self.orcaout_name, "r", encoding="utf8", errors="ignore") as out_file:
            for line in out_file:
                if f"Extrapolated CBS correlation energy" in line and "SCF" not in line:
                    line = line.strip().split()
                    correction = float(line[-1].replace("(", "").replace(")", ""))
                    break
        if not correction:
            raise BaseException(
                "It seems your output is not from a CBS (extrapolate) calculation. Please check it and try again!"
            )

        return correction

    def get_nfod(self):

        n_fod = None
        with open(self.orcaout_name, "r", encoding="utf8", errors="ignore") as out_file:
            for line in out_file:
                if f"N_FOD" in line and "alpha" not in line and "beta" not in line:
                    line = line.strip().split()
                    n_fod = float(line[-1])
                    break
        if not n_fod:
            raise BaseException(
                "It seems your output is not from a FOD calculation. Please check it and try again!"
            )

        return n_fod

    def get_cc_diagnostic(self):

        dic = None
        if self.optimization:
            raise BaseException(
                "The CC diagnostic must be used for Single Point Calculations only."
            )

        with open(self.orcaout_name, "r", encoding="utf8", errors="ignore") as out_file:
            for line in out_file:
                if "E(CORR)" in line:
                    line = line.strip().split()
                    e_corr = float(line[-1])
                if "T1 diagnostic" in line:
                    line = line.strip().split()
                    t1_diagnostic = float(line[-1])
                    dic = {"corr": e_corr, "t1": t1_diagnostic}
                # Only for Triples calculation
                if "Final correlation energy" in line:
                    for line in out_file:
                        if "E(CCSD)" in line:
                            line = line.strip().split()
                            e_ccsd = float(line[-1])
                    dic.update({"ccsd": e_ccsd})
        if not dic:
            raise BaseException(
                "It seems your output is not from a CCSD or CCSD(T) calculation. Please check it and try again!"
            )
        return dic

    def get_mcscf_correlation(self):

        dic = None
        if self.optimization:
            raise BaseException(
                "The MCSCF correlation must be used for Single Point Calculations only."
            )

        with open(self.orcaout_name, "r", encoding="utf8", errors="ignore") as out_file:
            e_casscf = 0
            e_corr = None

            for line in out_file:
                # First the code always do CASSCF and print
                if "Final CASSCF energy" not in line:
                    continue
                else:
                    e_casscf = float(line.strip().split()[4])
                    e_corr = self.scf_energy - e_casscf
                    dic = {
                        "casscf": e_casscf,
                        "corr": e_corr,
                    }
                    break
        if not dic:
            raise BaseException(
                "It seems your output is not from a NEVPT2, CASPT2 or MRCI calculation. Please check it and try again!"
            )

        return dic
