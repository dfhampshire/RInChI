"""
RInChI C Library Interface Module
---------------------------------

This module provides functions defining how RInChIs and RAuxInfos are constructed from InChIs and reaction data.  It
also interfaces with the RInChI v1.00 software as provided by the InChI trust.

This file is based on that provided with the official v1.00 RInChI software release, but with modifications to ensure
Python 3 compatibility.  Documentation was adapted from the official v1.00 release document.

Modifications:

 - D. Hampshire 2017

"""

import ctypes as ct

from . import _external


class StringHandler(object):
    """
    Enables seamless use with Python 3 by converting to ascii within the argument objects
    """

    @classmethod
    def from_param(cls, value):
        """
        Performs the conversion
        """
        if isinstance(value, bytes):
            return value
        else:
            return value.encode('ascii')


class RInChI:
    """
    The RInChI class interfaces the C class in the librinchi library
    """

    def __init__(self, lib_path=_external.LIB_RINCHI_PATH):

        self.lib_handle = ct.cdll.LoadLibrary(lib_path)

        self.lib_latest_error_message = self.lib_handle.rinchilib_latest_err_msg
        self.lib_latest_error_message.restype = ct.c_char_p

        self.lib_rinchi_from_file_text = self.lib_handle.rinchilib_rinchi_from_file_text
        self.lib_rinchi_from_file_text.argtypes = [StringHandler, StringHandler, ct.c_bool, ct.POINTER(ct.c_char_p),
                                                   ct.POINTER(ct.c_char_p)]
        self.lib_rinchi_from_file_text.restype = ct.c_long

        self.lib_rinchikey_from_file_text = self.lib_handle.rinchilib_rinchikey_from_file_text
        self.lib_rinchikey_from_file_text.argtypes = [StringHandler, StringHandler, StringHandler,
                                                      ct.c_bool, ct.POINTER(ct.c_char_p)]
        self.lib_rinchikey_from_file_text.restype = ct.c_long

        self.lib_file_text_from_rinchi = self.lib_handle.rinchilib_file_text_from_rinchi
        self.lib_file_text_from_rinchi.argtypes = [StringHandler, StringHandler, StringHandler,
                                                   ct.POINTER(ct.c_char_p)]
        self.lib_file_text_from_rinchi.restype = ct.c_long

        self.lib_inchis_from_rinchi = self.lib_handle.rinchilib_inchis_from_rinchi
        self.lib_inchis_from_rinchi.argtypes = [StringHandler, StringHandler, ct.POINTER(ct.c_char_p)]
        self.lib_inchis_from_rinchi.restype = ct.c_long

        self.lib_rinchikey_from_rinchi = self.lib_handle.rinchilib_rinchikey_from_rinchi
        self.lib_rinchikey_from_rinchi.argtypes = [StringHandler, StringHandler, ct.POINTER(ct.c_char_p)]
        self.lib_rinchikey_from_rinchi.restype = ct.c_long

    def rinchi_errorcheck(self, return_code):
        """
        Specifies Python error handling behavior

        Args:
            return_code : the return code from the C library
        """
        if return_code != 0:
            err_message = str(self.lib_latest_error_message(), 'utf-8')
            print(err_message)
            raise Exception(err_message)

    def rinchi_from_file_text(self, input_format, rxnfile_data, force_equilibrium=False):
        """
        Generates RInChI string and RAuxInfo from supplied RD or RXN file text.

        Args:
            input_format: “AUTO”, "RD" or "RXN" (with “AUTO” as default value)
            rxnfile_data: text block of RD or RXN file data
            force_equilibrium (bool) : Force interpretation of reaction as equilibrium reaction

        Returns:
            tuple pair of the RInChI and RAuxInfo generated
        """
        result_rinchi_string = ct.c_char_p()
        result_rinchi_auxinfo = ct.c_char_p()
        self.rinchi_errorcheck(
            self.lib_rinchi_from_file_text(input_format, rxnfile_data, force_equilibrium,
                                           ct.byref(result_rinchi_string),
                                           ct.byref(result_rinchi_auxinfo)))
        res_rinchi = str(result_rinchi_string.value, 'utf-8')
        res_auxinfo = str(result_rinchi_auxinfo.value, 'utf-8')
        return res_rinchi, res_auxinfo

    def rinchikey_from_file_text(self, input_format, file_text, key_type, force_equilibrium=False):
        """
        Generates RInChI key of supplied RD or RXN file text.

        Args:
            input_format: "RD" or "RXN"
            file_text: text block of RD or RXN file data
            key_type: 1 letter controlling the type of key generated; “L” for Long-RInChIKey, “S” for Short key
            (Short-RInChIKey), “W” for Web key (Web-RInChIKey)
            force_equilibrium (bool): Force interpretation of reaction as equilibrium reaction

        Returns:
            a RInChIKey
        """

        result = ct.c_char_p()
        self.rinchi_errorcheck(
            self.lib_rinchikey_from_file_text(input_format, file_text, key_type, force_equilibrium, ct.byref(result)))
        result_uc = str(result.value, 'utf-8')
        return result_uc

    def file_text_from_rinchi(self, rinchi_string, rinchi_auxinfo, output_format):
        """
        Reconstructs (or attempts to reconstruct) RD or RXN file from RInChI string and RAuxInfo

        Args:
            rinchi_string: The RInChI string to convert
            rinchi_auxinfo: The RAuxInfo to convert (optional, recommended)
            output_format: "RD" or "RXN"

        Returns:
            The text block for the file
        """
        result = ct.c_char_p()
        self.rinchi_errorcheck(
            self.lib_file_text_from_rinchi(rinchi_string, rinchi_auxinfo, output_format, ct.byref(result)))
        result_uc = str(result.value, 'utf-8')
        return result_uc

    def inchis_from_rinchi(self, rinchi_string, rinchi_auxinfo=""):
        """
        Splits an RInChI string and optional RAuxInfo into components.

        Args:
            rinchi_string: A RInChI string
            rinchi_auxinfo: RAuxInfo string.  May be blank but may not be NULL.

        Raises:
            Exception: RInChi format related errors

        Returns:
            A dictionary of data returned. The structure is as below::

                {'Direction': [direction character],
                 'No-Structures': [list of no-structures],
                 'Reactants': [list of inchis & auxinfos],
                 'Products': [list of inchis & auxinfos],
                 'Agents': [list of inchis] & auxinfos}

            Each Reactant, Product, and Agent list contains a set of (InChI, AuxInfo) tuples. The
            No-Structures list contains No-Structure counts for Reactants, Products, and Agents.
        """
        inchis = ct.c_char_p()
        self.rinchi_errorcheck(self.lib_inchis_from_rinchi(rinchi_string, rinchi_auxinfo, ct.byref(inchis)))
        inchis_unicode = str(inchis.value, 'utf-8')
        lines = inchis_unicode.split("\n")

        # Get rid of trailing line, if any.
        if lines[len(lines) - 1] == "":
            lines = lines[:len(lines) - 1]

        # Sanity check: Must contain an even number of lines (direction line +
        # No-Structure count line + n * InChI+AuxInfo line pairs).
        if len(lines) % 2 != 0:
            raise Exception("Invalid number of lines (" + str(
                len(lines)) + ") produced by RInChI library function 'rinchilib_inchis_from_rinchi()'.")

        direction = lines[0]
        if direction[:2] != "D:":
            raise Exception("""Invalid direction line (must be first line received from RInChI library function"
                             'rinchilib_inchis_from_rinchi()'.""")
        direction = direction[2:]
        lines = lines[1:]

        nostruct_count_line = lines[0]
        if nostruct_count_line[:2] != "N:":
            raise Exception("""Invalid No-Structure count line (must be second line received from RInChI library function
                'rinchilib_inchis_from_rinchi()'.""")
        nostruct_count_line = nostruct_count_line[2:]
        nostruct_counts = [int(x) for x in nostruct_count_line.split(",")]
        lines = lines[1:]

        reactants = []
        products = []
        agents = []

        for i in range(0, len(lines) // 2):
            component_prefix = lines[i * 2][:2]
            inchi_string = lines[i * 2][2:]
            aux_info = lines[i * 2 + 1][2:]

            # Sanity check: Must contain InChI + AuxInfo pairs.
            if not inchi_string.startswith("InChI"):
                raise Exception("Invalid InChI string '" + inchi_string + "'.")
            if aux_info != "" and (not aux_info.startswith("AuxInfo")):
                raise Exception("Invalid AuxInfo '" + aux_info + "'.")
            if component_prefix == "R:":
                reactants.append((inchi_string, aux_info))
            elif component_prefix == "P:":
                products.append((inchi_string, aux_info))
            elif component_prefix == "A:":
                agents.append((inchi_string, aux_info))
            else:
                raise Exception("Unsupported component prefix '" + component_prefix + "'.")

        return {"Direction": direction, "No-Structures": nostruct_counts, "Reactants": reactants, "Products": products,
                "Agents": agents}

    def rinchikey_from_rinchi(self, rinchi_string, key_type):
        """
        Generates RInChI key of supplied RD or RXN file text.

        Args:
            rinchi_string: A RInChI string
            key_type: 1 letter controlling the type of key generated with “L” for the Long-RInChIKey, “S” for the Short
                key (Short-RInChIKey), “W” for the Web key (Web-RInChIKey)

        Returns:
            the RInChiKey
        """
        result = ct.c_char_p()
        self.rinchi_errorcheck(self.lib_rinchikey_from_rinchi(rinchi_string, key_type, ct.byref(result)))
        result_uc = str(result.value, 'utf-8')
        return result_uc
