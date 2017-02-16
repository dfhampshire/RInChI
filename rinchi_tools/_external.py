"""
RInChI external software location module.

    C.H.G. Allen Copyright 2012
    D. Hampshire 2016

This module defines variables that specify the paths to external software and files
used by the RInChI tools.
"""
import copy
import os

# Set root path for the modules
ROOT = os.path.abspath(os.path.join(__file__, "../.."))

# Specify folders for the software components. Each tuple element represents a folder.
db_dir = ('database',)
test_dir = ('test-resources',)
cmd_dir = ('',)
module_dir = ('rinchi_tools',)

path = os.path.dirname(os.path.abspath(__file__))

# Set files and separators
SEPARATOR = os.sep
if SEPARATOR == "\\":
    lib_file = "librinchi.dll"
else:
    lib_file = "librinchi.so.1.0.0"

# Path to IUPAC's InChI executable.
INCHI_PATH = ROOT + path + '{0}libs{0}inchi-1'.format(SEPARATOR)

# Path to the v0.03 RInChI C library
LIB_RINCHI_PATH = path + "{0}libs{0}".format(SEPARATOR) + lib_file

# Set RInChI Version
RINCHI_VERSION = '0.03'

# Set RInChI database variables
RINCHI_DATABASE = os.path.abspath(os.path.join(__file__, "../..")) + '{}rinchi.db'.format(SEPARATOR)
RINCHI_DATABASE_PATH = path = os.path.dirname(RINCHI_DATABASE)
RINCHI_TEMP_DATABASE = RINCHI_DATABASE_PATH + SEPARATOR + "rinchi_temp.db"

# Set test folder
TEST_PATH = os.path.abspath(os.path.join(__file__, "../.."))

if __name__ == "__main__":
    # Print the variables defined here
    all_vars = copy.copy(locals())
    for name, value in all_vars.items():
        if not name.startswith('__') and name.upper() == name:
            print('{} : {}'.format(name, value))
