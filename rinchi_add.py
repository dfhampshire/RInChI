#!/usr/bin/env python3
"""
RInChI addition script
----------------------

This script adds together flat files of RInChIs separated by newlines.

Modifications:
 - C.H.G. Allen 2012
 - D.F. Hampshire 2016
    Rewritten to use argparse module and Python3

"""

import argparse

from rinchi_tools import tools, utils


def add_addition(subparser):
    """
    Adds the arguments for the addition operation to the ``ArgumentParser`` object.
    
    Args:
        subparser: An ``ArgumentParser`` object
    """

    assert isinstance(subparser, argparse.ArgumentParser)

    subparser.add_argument("input_path", help="Path of file to input")
    subparser.add_argument("-o", "--output", nargs='?', const='addition', default=False,
                           help="Output the result to a file. Optionally specify the file output name")


def addition_ops(args, parser):
    """
    Executes the addition operations.
    
    Args:
        args: The output of the ``parser.parse_args()``. The command line arguments.
        parser: An ``ArgumentParser`` object
    """
    try:
        input_rinchis = (line.strip() for line in open(args.input_path))  # Use a generator
        overall_rinchi = tools.add(input_rinchis)
        utils.output(overall_rinchi, args.output, "rinchi")
    except ValueError:
        parser.error('An error occurred')

if __name__ == "__main__":
    role = "RInChI addition"
    parser = argparse.ArgumentParser(description=role)
    add_addition(parser)
    args = parser.parse_args()
    addition_ops(args, parser)
