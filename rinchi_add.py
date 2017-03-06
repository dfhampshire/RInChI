#!/usr/bin/env python3
"""
RInChI addition script

This script adds together flat files of RInChIs separated by newlines.

    C.H.G. Allen 2012
    D.F. Hampshire 2016- Rewritten to use argparse module and Python3

"""

import argparse

from rinchi_tools import tools, utils


def add_addition(subparser):
    """

    Args:
        subparser:

    Returns:

    """

    assert isinstance(subparser, argparse.ArgumentParser)

    subparser.add_argument("input_path", help="Path of file to input")
    subparser.add_argument("-o", "--output", nargs='?', const='addition', default=False,
                           help="Output the result to a file. Optionally specify the file output name")


def addition_ops(args, parser):
    """

    Args:
        args:
        parser:

    Returns:

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
