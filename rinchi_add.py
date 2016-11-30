#!/usr/bin/env python3

"""
RInChI addition script.

    Copyright 2012 C.H.G. Allen 2016 D.F. Hampshire

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0 .

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

The input RInChI file should contain the RInChIs representing the steps of the
reaction IN ORDER and separated by line breaks.

"""

import argparse

from rinchi_tools import utils, tools

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RInChI addition \n{}".format(__doc__))
    parser.add_argument("input_path", help="Path of file to input")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("-f","--fileout",action="store_false", help="Output to file instead of printing")
    args = parser.parse_args()
    if args.input_path:
        input_file = open('%s' % args.input_path).read()
        input_rinchis = input_file.strip().splitlines()
        overall_rinchi = tools.add(input_rinchis)
        utils.output(overall_rinchi, args.fileout, "rinchi")
