"""
RInChI external software location module.

    C.H.G. Allen Copyright 2012
    D. Hampshire 2016

This module defines variables that specify the paths to external software
used by the RInChI tools.
"""
import os

path = os.path.dirname(os.path.abspath(__file__))

# Set files and separators
if os.sep == "\\":
    sep = "\\"
    lib_file = "{}librinchi.dll".format(sep)
else:
    sep = "/"
    lib_file = "{}librinchi.so.1.0.0".format(sep)

# Path to IUPAC's InChI executable.
INCHI_PATH = path + '{}inchi-1'.format(sep)

# Path to the v0.03 RInChI C library
LIB_RINCHI_PATH = path + "{}rinchi-lib-1".format(sep) + lib_file

# Set RInChI Version
RINCHI_VERSION = '0.03'

RINCHI_DATABASE = os.path.abspath(os.path.join(__file__,"../..")) + '{}rinchi.db'.format(sep)
