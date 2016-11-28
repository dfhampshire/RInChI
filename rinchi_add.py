#!/usr/bin/env python3

"""
RInChI addition script.

    Copyright 2012 C.H.G. Allen 2016 D.F. Hampshire

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

This module provides a function for adding together RInChIs representing the
individual steps of a multi-step reaction into one RInChI representing the
overall process. It also interfaces with the RInChI v0.03 software as provided
by the InChI trust.

The RInChI library and programs are free software developed under the
auspices of the International Union of Pure and Applied Chemistry (IUPAC).

Sample use:
    ./rinchi_addition.py /some/path/steps.rinchi -f

Options:
    -fileout: Save the RInChI to the file

The input RInChI file should contain the RInChIs representing the steps of the
reaction IN ORDER and separated by line breaks.
"""

import argparse
import sys

from rinchi_tools import utils, tools

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RInChI addition \n{}".format(__doc__))
    parser.add_argument("input_path", help="Path of file to file to imput")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("-f","--fileout",action="store_true", help="Output to file instead of printing")
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        input_name = input_path.split('/')[-1].split('.')[0]
        input_file = open('%s' % input_path).read()
        input_rinchis = input_file.strip().splitlines()
        overall_rinchi = tools.add(input_rinchis)
        s_out = True
        for arg in sys.argv[2:]:
            if arg.startswith('-f'):
                s_out = False
        utils.output(overall_rinchi, s_out, "rinchi")
    else:
        print(__doc__)
