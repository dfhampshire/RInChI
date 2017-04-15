"""
RInChI External and Module Variable
-----------------------------------

This module defines variables that specify the paths to external software and files
used by the RInChI tools.

Modifications:

- D. Hampshire 2016
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

# Set files and separators
SEPARATOR = os.sep
if SEPARATOR == "\\":
    lib_file = "librinchi.dll"
else:
    lib_file = "librinchi.so.1.0.0"

# Path to IUPAC's InChI executable.
EXEC_PATH = ROOT + '{0}rinchi_tools{0}libs'.format(SEPARATOR)
INCHI_PATH = EXEC_PATH + '{0}inchi-1'.format(SEPARATOR)

# Path to the v0.03 RInChI C library
LIB_RINCHI_PATH = EXEC_PATH + SEPARATOR + lib_file

# Set RInChI Version
RINCHI_VERSION = '0.03'

# Set RInChI database variables
RINCHI_DATABASE = ROOT + '{0}database{0}rinchi.db'.format(SEPARATOR)
RINCHI_DATABASE_PATH = os.path.dirname(RINCHI_DATABASE)
RINCHI_TEMP_DATABASE = RINCHI_DATABASE_PATH + SEPARATOR + "rinchi_temp.db"

# Set test folder
TEST_PATH = ROOT + "{0}test-resources".format(SEPARATOR)


# Define Error Handling

class RInChIError(ValueError):
    pass


class InChIError(ValueError):
    pass


class VersionError(Exception):
    pass


if __name__ == "__main__":
    # Print the variables defined here
    all_vars = copy.copy(locals())
    for name, value in all_vars.items():
        if not name.startswith('__') and name.upper() == name:
            print('{} : {}'.format(name, value))
