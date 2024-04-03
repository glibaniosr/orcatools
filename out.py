#!/usr/bin/env python3

# Conversion factors
# hartree to kcal/mol
harkcal = 627.50946900


# To easily do from here --> get the calculation timings
def check_normal_termination(out_file):
    normal_termination = False
    with open(out_file, "r", encoding="utf8", errors="ignore") as data:
        lines = data.readlines()
        while not lines[-1].strip():
            del lines[-1]
        if "ORCA TERMINATED NORMALLY" in lines[-2]:
            normal_termination = True
    return normal_termination


def check_opt(out_file):
    optimization = False
    with open(out_file, "r", encoding="utf8", errors="ignore") as data:
        for line in data:
            if "END OF INPUT" in line:
                for idx, line in enumerate(data):
                    if idx == 3:
                        if "Geometry Optimization Run" in line:
                            optimization = True
                            break
    return optimization


def get_energy_from_out(out_file):
    opt = check_opt(out_file)
    scf_energy = 0
    with open(out_file, "r", encoding="utf8", errors="ignore") as data:
        for line in data:
            if opt:
                for line in data:
                    if "HURRAY" in line:
                        for line in data:
                            if "FINAL SINGLE POINT ENERGY" in line:
                                scf_energy = float(line.split()[4])
            else:
                for line in data:
                    if "FINAL SINGLE POINT ENERGY" in line:
                        scf_energy = float(line.split()[4])
    return scf_energy


def get_xyz_from_out(out_file, opt):  # Have to include the scan option
    opt = check_opt(out_file)

    with open(out_file, "r", encoding="utf8", errors="ignore") as data:
        coords = []
        if opt:
            for line in data:
                if "HURRAY" in line:
                    for line in data:
                        if "CARTESIAN COORDINATES (ANGSTROEM)" in line:
                            for line in data:
                                if "---" in line:
                                    continue
                                if line and line != "\n":
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
                                    break
        else:
            for line in data:
                if "CARTESIAN COORDINATES (ANGSTROEM)" in line:
                    for line in data:
                        if "---" in line:
                            continue
                        if line and line != "\n":
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
                            break
                    break
    return coords


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
        orca_normal_termination = check_normal_termination(orcaout_name)
        if not orca_normal_termination:
            raise BaseException(
                """You ORCA output file did not have a normal termination! Check your calculation and try again.
            """
            )
        self.optimization = check_opt(orcaout_name)
        self.scf_energy = get_energy_from_out(orcaout_name, self.optimization)
        self.xyz_coords = get_xyz_from_out(orcaout_name, self.optimization)
        if verbose:
            print(f"Orca Output -> {orcaout_name}")
            if self.optimization:
                print("Optimization Run")
            else:
                print("Single Point Energy Run")
            print(f"Final SCF Energy (Hartree) = {self.scf_energy:.12f}")

    def get_thermal_corrections(self):
        out_file = self.orcaout_name
        with open(out_file, "r", encoding="utf8", errors="ignore") as data:
            zpe = 0
            u_correction = 0
            KbT_correction = 0
            h_correction = 0
            s_correction = 0
            g_correction = 0
            for line in data:
                if "Zero point energy" in line:
                    zpe = float(line.strip().split()[-4])
                if "Total correction" in line:
                    u_correction = float(line.strip().split()[-4])
                if "Thermal Enthalpy correction" in line:
                    KbT_correction = float(line.strip().split()[-4])
                    h_correction = u_correction + KbT_correction
                if "Final entropy term" in line:
                    s_correction = float(line.strip().split()[-4])
                if "G-E(el)" in line:
                    g_correction = float(line.strip().split()[-4])
        if (
            not zpe
            and not u_correction
            and not h_correction
            and not s_correction
            and not g_correction
        ):
            raise BaseException(
                "We did not find vibrational data in your output. Check your calculation!"
            )

        return {
            "ZPE": zpe,
            "U": u_correction,
            "H": h_correction,
            "S": s_correction,
            "G": g_correction,
        }

    def get_correlation_cbs(self):
        out_file = self.orcaout_name
        correction = None
        with open(out_file, "r", encoding="utf8", errors="ignore") as data:
            for line in data:
                if f"Extrapolated CBS correlation energy" in line and "SCF" not in line:
                    line = line.strip().split()
                    correction = float(line[-1].replace("(", "").replace(")", ""))
        return correction

    def get_nfod(self):
        out_file = self.orcaout_name
        n_fod = None
        with open(out_file, "r", encoding="utf8", errors="ignore") as data:
            for line in data:
                if f"N_FOD" in line and "alpha" not in line and "beta" not in line:
                    line = line.strip().split()
                    n_fod = float(line[-1])
        return n_fod

    def get_cc_diagnostic(self, triples=True, extrapolation=True):
        out_file = self.orcaout_name
        if self.optimization:
            raise BaseException(
                "The CC diagnostic must be used for Single Point Calculations only"
            )

        if extrapolation:
            with open(out_file, "r", encoding="utf8", errors="ignore") as data:
                e_ccsd = 0
                e_ccsdt = None
                t1_diagnostic = 0
                if triples:
                    for line in data:
                        if "Extrapolated Energy 2 Basis" in line:
                            for line in data:
                                if "T1 diagnostic" in line:
                                    line = line.strip().split()
                                    t1_diagnostic = float(line[-1])
                                if "Final correlation energy" in line:
                                    for line in data:
                                        if "E(CCSD)" in line:
                                            line = line.strip().split()
                                            e_ccsd = float(line[-1])
                                        if "E(CCSD(T))" in line:
                                            line = line.strip().split()
                                            e_ccsdt = float(line[-1])
                else:
                    for line in data:
                        if "Extrapolated Energy 2 Basis" in line:
                            for line in data:
                                if "T1 diagnostic" in line:
                                    line = line.strip().split()
                                    t1_diagnostic = float(line[-1])
                                if "Final correlation energy" in line:
                                    for line in data:
                                        if "E(CCSD)" in line:
                                            line = line.strip().split()
                                            e_ccsd = float(line[-1])
        else:
            with open(out_file, "r", encoding="utf8", errors="ignore") as data:
                e_ccsd = 0
                e_ccsdt = 0
                t1_diagnostic = 0
                if triples:
                    for line in data:
                        if "T1 diagnostic" in line:
                            line = line.strip().split()
                            t1_diagnostic = float(line[-1])
                        if "Final correlation energy" in line:
                            for line in data:
                                if "E(CCSD)" in line:
                                    line = line.strip().split()
                                    e_ccsd = float(line[-1])
                                if "E(CCSD(T))" in line:
                                    line = line.strip().split()
                                    e_ccsdt = float(line[-1])
                else:
                    for line in data:
                        if "T1 diagnostic" in line:
                            line = line.strip().split()
                            t1_diagnostic = float(line[-1])
                        if "Final correlation energy" in line:
                            for line in data:
                                if "E(CCSD)" in line:
                                    line = line.strip().split()
                                    e_ccsd = float(line[-1])

        return {"ccsd": e_ccsd, "ccsdt": e_ccsdt, "t1_diagnostic": t1_diagnostic}

    def get_mcscf_correlation(self, mrci=False):
        out_file = self.orcaout_name
        if self.optimization:
            raise BaseException(
                "The MCSCF correlation must be used for Single Point Calculations only"
            )

        with open(out_file, "r", encoding="utf8", errors="ignore") as data:
            e_casscf = 0
            e_corr = None
            e_mrci = None
            e_mrci_davidson = None
            e_mrci_mp2 = None

            for line in data:
                # First the code always do CASSCF and print
                if "Final CASSCF energy" not in line:
                    continue
                else:
                    e_casscf = float(line.strip().split()[4])
                    e_corr = self.scf_energy - e_casscf
                    # For MRCI calculations its useful to also get Davidson and MR-MP2 corrections
                    if mrci:
                        e_mrci = self.scf_energy
                        e_mrci_davidson = []
                        e_mrci_mp2 = []
                        for line in data:
                            getdata = None
                            if "DAVIDSON DONE" in line:
                                getdata = "dav"
                                for line in data:
                                    if getdata == "dav" and "Root" in line:
                                        line = line.strip().split()
                                        e_mrci_davidson.append(
                                            float(line[-1].replace("DE=", ""))
                                        )
                                    elif "Full relaxed MR-MP2 calculation" in line:
                                        getdata = "mp2"
                                        for line in data:
                                            if getdata == "mp2" and "Root" in line:
                                                line = line.strip().split()
                                                e_mrci_mp2.append(float(line[-1]))
                                            elif getdata == "mp2" and len(
                                                e_mrci_mp2
                                            ) == len(e_mrci_davidson):
                                                break

        return {
            "casscf": e_casscf,
            "corr": e_corr,
            "mrci": e_mrci,
            "mrci_davidson": e_mrci_davidson,
            "mrci_mp2": e_mrci_mp2,
        }
