#!/usr/bin/env python3
"""
RInChI changes analysis script

This script analyses RInChI(s) for changes

    D. Hampshire 2017
"""

import argparse
import json
from collections import Counter

from rinchi_tools import Molecule, Reaction, _external, database, utils
from rinchi_tools.utils import Hashable


def changes_ops(args, parser):
    """
    Operations for the changes command line tool

    Args:
        args:
        parser:

    Returns:

    """
    if args.key:
        try:
            if args.input.startswith("Long-RInChIKey"):
                args.input = database.sql_key_to_rinchi(args.input, _external.RINCHI_DATABASE, args.arg2)
                args.rinchi = True
            else:
                raise ValueError
        except ValueError:
            raise ValueError("Could not find Long-RInChIKey in database")

    if args.rinchi:
        # Opens the file if the input is file containing a single RInChI. Otherwise it treats the input as RInChI itself
        if args.filein:
            try:
                with open(args.input) as f:
                    args.input = f.readline()
                    print(args.input)
                    if args.list:
                        print(args.input)
            except IOError:
                pass

        r = Reaction(args.input)
        if args.ringcount:
            out = r.change_across_reaction(Molecule.get_ring_count)
            print(utils.counter_to_print_string(out, "Ring Count"))
        if args.formula:
            out = r.change_across_reaction(Molecule.get_formula)
            print(utils.counter_to_print_string(out, "Formula"))
        if args.valence:
            out = r.change_across_reaction(Molecule.get_valence_count)
            print(utils.counter_to_print_string(out, "Valence Count"))
        if args.hybrid:
            out = r.change_across_reaction(Molecule.get_hybrid_count)
            print(utils.counter_to_print_string(out, "Hybridisation Count"))
        if args.ringcountelements:
            out = r.change_across_reaction(Molecule.get_ring_count_inc_elements)
            print(utils.counter_to_print_string(out, "Ring Count Elements"))
        if args.ringcountold:
            out = r.ring_change()
            print(utils.counter_to_print_string(out, "Ring Count (Old Method)"))
        if args.stereoold:
            out = r.stereo_change(args.stereoold.get('wd', None), args.stereoold.get('sp2', None),
                                  args.stereoold.get('sp3', None))
            print(utils.counter_to_print_string(out, "Stereocentre Count (Old Method)"))

    elif args.batch:
        master_counter = {'ringcount': Counter(), 'formula': Counter(), 'ringcountelements': Counter(),
                          'valence': Counter(), 'hybrid': Counter(), 'ringcount_old': Counter(),
                          'stereo_old': Counter()}
        with open(args.input) as data:
            for rinchi in data:
                r = Reaction(rinchi)
                if args.list:
                    print('\n__________________\n')
                    print(rinchi.strip())
                if args.ringcount:
                    # Count the change in ring populations across the reactions
                    ringcount = r.change_across_reaction(Molecule.get_ring_count)
                    if ringcount and args.list:
                        print(utils.counter_to_print_string(ringcount,"Ring Count"))
                    if ringcount:
                        master_counter['ringcount'][Hashable(ringcount)] += 1
                if args.ringcountelements:
                    # Count the change in rings returning the change in elemental structure of the rings e.g.  (
                    # CCCCCN : 1) would indicate the reaction forms a pyridine ring
                    ringcountelements = r.change_across_reaction(Molecule.get_ring_count_inc_elements)
                    if ringcountelements and args.list:
                        print(utils.counter_to_print_string(ringcountelements, "Ring Count Elements"))
                    if ringcountelements:
                        master_counter['ringcountelements'][Hashable(ringcountelements)] += 1
                if args.formula:
                    formula = r.change_across_reaction(Molecule.get_formula)
                    if formula and args.list:
                        print(utils.counter_to_print_string(formula, "Formula Change"))
                    if formula:
                        master_counter['formula'][Hashable(formula)] += 1
                if args.valence:
                    valence = r.change_across_reaction(Molecule.get_valence_count)
                    if valence and args.list:
                        print(utils.counter_to_print_string(valence, "Valence Count"))
                    if valence:
                        master_counter['valence'][Hashable(valence)] += 1
                if args.hybrid:
                    hybrid = r.change_across_reaction(Molecule.get_hybrid_count)
                    if hybrid and args.list:
                        print(utils.counter_to_print_string(hybrid, "Hybridisation Change Count"))
                    if hybrid:
                        master_counter['hybrid'][Hashable(hybrid)] += 1
                if args.ringcountold:
                    ringcountold = r.ring_change()
                    if ringcountold and args.list:
                        print(utils.counter_to_print_string(ringcountold, "Ring Count (Old Method)"))
                    if ringcountold:
                        master_counter['ringcount_old'][Hashable(ringcountold)] += 1
                if args.stereoold:  # TODO fix this

                    stereoold = r.stereo_change(args.stereoold.get('wd', None), args.stereoold.get('sp2', None),
                                                args.stereoold.get('sp3', None))
                    if stereoold and args.list:
                        print(utils.counter_to_print_string(stereoold, "Stereo Change Count (Old Method)"))
                    if stereoold:
                        master_counter['stereo_old'][Hashable(stereoold)] += 1
        print('\nStats\n-----')
        for key, value in master_counter.items():
            if value:
                print(utils.counter_to_print_string(value,key))
    else:
        parser.print_help()


def add_changes(subparser):
    """

    Args:
        subparser:
    """
    assert isinstance(subparser, argparse.ArgumentParser)
    subparser.add_argument("input", help="The file or string containing RInChI(s) or Long Key to be processed")

    # Add process arguments
    action = subparser.add_mutually_exclusive_group(required=True)
    action.add_argument('-b', '--batch', action='store_true', help='Process multiple RInChIs')
    action.add_argument('-r', '--rinchi', action='store_true', help='Process a single RInChI')
    action.add_argument("-k", "--key", action="store_true", help="Process a RInChI key")

    # Add file options
    file_opt = subparser.add_argument_group("File options")
    file_opt.add_argument("--list", action="store_true",
                          help="List RInChIs along with results. Otherwise returns count populations")
    file_opt.add_argument("--filein", action="store_true", help="Assert that the input is a file")

    # Add operation arguments
    operation = subparser.add_argument_group("Operation")
    operation.add_argument("--ringcount", action="store_true", help="Change in ring populations by size")
    operation.add_argument("--formula", action="store_true", help="Change in formula across a reaction")
    operation.add_argument("--valence", action="store_true", help="Change in valence across reaction")
    operation.add_argument("--hybrid", action="store_true", help="Change in hybridisation of C atoms across reaction")
    operation.add_argument("--ringcountelements", action="store_true",
                           help="Change in ring populations by ring elements")
    operation.add_argument("--ringcountold", action="store_true", help="Change in ring populations. Old method")
    operation.add_argument("--stereoold", nargs='?', type=json.loads,
                           help="Change stereocentres. Old method. Takes an argument as a dictionary "
                                "such as {'sp2':True,'sp3':False,'wd':True} for options to "
                                "1. Count sp2 centres 2. Count sp3 centre 3. Well defined stereocentres only")


if __name__ == "__main__":
    role = "RInChI Analysis and Manipulation"
    parser = argparse.ArgumentParser(description=role)
    add_changes(parser)
    args = parser.parse_args()
    changes_ops(args, parser)
