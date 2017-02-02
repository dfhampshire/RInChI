#!/usr/bin/env python3

"""
RInChI addition script.

    Copyright 2012 C.H.G. Allen 2016 D.F. Hampshire

Rewritten to use argparse module

"""

import argparse

from rinchi_tools import utils, tools

# TODO refactor into a more logical command line call interface

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RInChI addition \n{}".format(__doc__))
    parser.add_argument("input_path", help="Path of file to input")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("-f", "--fileout", action="store_false", help="Output to file instead of printing")
    args = parser.parse_args()
    if args.input_path:
        input_file = open('%s' % args.input_path).read()
        input_rinchis = input_file.strip().splitlines()
        overall_rinchi = tools.add(input_rinchis)
        utils.output(overall_rinchi, args.fileout, "rinchi")
