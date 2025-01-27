#!/usr/bin/env python3
import os


# ----- Define the OUTPUT class
class ORCAOUT:
    """
    Class which holds information for a ORCA input object.

    :param orcaout_name:
        A string with the name of the output file.
    :param verbose=False:
        Specify verbosity when starting the ORCAOUT class.
    :param function_mode=False:
        Activate function mode, where attributes are not gathered at __init__. Useful for saving time when specific functions are requested.

    :attribute runtime:
        The runtime of the calculation.
    :attribute optimization:
        Boolean that tells if the calculation is an optimization.
    :attribute scf_energy:
        The final SCF energy.
    :attribute coordinates:
        The final coordinates of the system.
    :attribute xyzstr:
        The final coordinates of the system in string format.
    """

    def __init__(self, orcaout_name, verbose=False, function_mode=False):

        if not os.path.exists(orcaout_name):
            raise FileNotFoundError(f"File {orcaout_name} not found!")

        self.orcaout_name = orcaout_name

        if not function_mode:
            self.optimization = False
            self.scf_energy = 0
            self.coordinates = []
            self.xyzstr = ""
            self.runtime = 0
            self._process_output_file()

        if verbose:
            print(f"Orca Output -> {os.path.abspath(orcaout_name)}")
            if self.optimization:
                print("Optimization Run")
            else:
                print("Single Point Energy Run")
            print(f"(Final) Geometry: \n{self.xyzstr}")
            print(f"Final SCF Energy (Hartree) = {self.scf_energy:.12f}")
            print(f"Calculation Time = {self.runtime} s")

    def get_thermal_corrections(self):
        """
        Function that returns a dictionary with the thermal correction data from the output file.

        :return:
            A dictionary with the following keys:
            "ZPE" - Zero Point Energy
            "U" - Internal Energy
            "H" - Enthalpy
            "S" - Entropy
            "G" - Gibbs Free Energy
        """
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
        """
        Function that returns the CBS correlation energy from the output file.
        """
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
        """
        Function that returns the fraction occupation density (FOD) number from the output file.
        """
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

    def get_cc_diagnostic(self, extrapolation=False):
        """
        Function that returns the CCSD or CCSD(T) parameters from the output file.

        :param
            extrapolation=False - Change to True if your calculation uses basis set extrapolation.

        :return:
            Dictionary with the following keys:
            "corr" - Correlation energy
            "t1" - T1 diagnostic
            "ccsd" - CCSD energy
        """
        dic = None
        if self.optimization:
            raise BaseException(
                "The CC diagnostic must be used for Single Point Calculations only."
            )

        with open(self.orcaout_name, "r", encoding="utf8", errors="ignore") as out_file:
            for line in out_file:
                if extrapolation:
                    if "Extrapolated Energy 2" in line:
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
                                        break
                else:
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
                                break

        dic.update({"ccsd": e_ccsd})
        if not dic:
            raise BaseException(
                "It seems your output is not from a CCSD or CCSD(T) calculation. Please check it and try again!"
            )
        return dic

    def get_mcscf_correlation(self):
        """
        Function that returns the MCSCF correlation energy from the output file.

        :return: Dictionary with the following keys:
        "casscf" - CASSCF energy
        "corr" - Correlation energy
        """
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

    def get_absorption_data(self, unit="eV"):
        """
        Function that returns the absorption energies and oscillator strengths from the output file.

        :param unit="eV" - The unit of the absorption energies. Options are "cm" (cm-1), "nm" and "eV".

        :return: Tuple with two lists: (energies, fosc)

        1. Absorption energies
        2. Oscillator strengths
        """

        e_idx = {"cm": 5, "nm": 6, "eV": 5}
        energies = []
        fosc = []
        with open(self.orcaout_name, "r", encoding="utf8", errors="ignore") as out_file:
            in_block = False
            for line in out_file:
                if (
                    "------------------------------------------------------------------------------------------"
                    in line
                ):
                    for line in out_file:
                        if "ABSORPTION SPECTRUM" in line:
                            in_block = True
                        elif in_block and "CD SPECTRUM" in line:
                            break
                        elif in_block and "0(" in line:
                            fo = float(line.split()[7])
                            E = float(line.split()[e_idx[unit]])
                            if unit == "eV":
                                E = E * 0.000123984
                            energies.append(E)
                            fosc.append(fo)
        if not energies:
            raise ValueError(
                "No absorption spectrum values found in the specified output file."
            )
        return energies, fosc
    
    def get_active_space(self):
        """
        Function that returns the active space (initial and final orbital numbers) from the output file of a CASSCF calculation.
        """
        n = None
        m = None
        active_space = None
        with open(self.orcaout_name, "r", encoding="utf8", errors="ignore") as out_file:
            for line in out_file:
                if "Number of active electrons" in line:
                    n = int(line.strip().split()[-1])
                if "Number of active orbitals" in line:
                    m = int(line.strip().split()[-1])
                if "Determined orbital ranges" in line:
                    for line in out_file:
                        if "Active" in line:
                            active_space = (int(line.strip().split()[1]), int(line.strip().split()[3]))
                            break
        if not active_space or not n or not m:
            raise BaseException(
                "It seems your output is not from a CASSCF calculation. Please check it and try again!"
            )

        return n, m, active_space
    
    def get_occupation_numbers(self):
        """
        Function that returns the occupation numbers from the output file of a CASSCF calculation.
        """
        n, m, active_MOs = self.get_active_space()
        with open(self.orcaout_name, "r", encoding="utf8", errors="ignore") as out_file:
            for line in out_file:
                if "CASSCF RESULTS" in line:
                    occ_numbers = []
                    read_active_MOs = False
                    for line in out_file:
                        if read_active_MOs and int(line.strip().split()[0]) > active_MOs[1]:
                            break
                        if not line.strip():
                            continue
                        if line.strip().split()[0] == str(active_MOs[0]):
                            read_active_MOs = True
                        if read_active_MOs:
                            occ_numbers.append(float(line.strip().split()[1]))
        if not occ_numbers:
            raise BaseException(
                "It seems your output is not from a CASSCF calculation. Please check it and try again!"
            )

        return occ_numbers

    def _process_output_file(self):
        with open(self.orcaout_name, "r", encoding="utf8", errors="ignore") as out_file:

            lines = out_file.readlines()
            for line in reversed(lines):
                if line.strip():  # Skip blank lines
                    if "ORCA TERMINATED NORMALLY" in line:
                        normal_termination = True
                        clock = lines[lines.index(line) + 1].split()[3:]
                        self.runtime = (
                            float(clock[0]) * 86400
                            + float(clock[2]) * 3600
                            + float(clock[4]) * 60
                            + float(clock[6])
                            + float(clock[8]) / 1000
                        )
                        break
            if not normal_termination:
                raise BaseException(
                    """Your ORCA output file did not have a normal termination! Check your calculation and try again."""
                )

            for i, line in enumerate(lines):
                if "Geometry Optimization Run" in line:
                    self.optimization = True
                if "FINAL SINGLE POINT ENERGY" in line:
                    self.scf_energy = float(line.split()[-1])
                if "CARTESIAN COORDINATES (ANGSTROEM)" in line:
                    self.coordinates = []
                    self.xyzstr = ""
                    for j in range(i + 2, len(lines)):
                        if lines[j].strip() == "":
                            break
                        self.coordinates.append(lines[j].strip())
                        self.xyzstr += lines[j]
