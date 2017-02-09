#!/usr/bin/env python3
"""
RInChI analysis script

This script analyses flat files of RInChIs separated by newlines.

    C.H.G. Allen 2012
    D. Hampshire 2016 - Rewritten to use argparse module and Python3

"""

import argparse
import textwrap

from rinchi_search import __search
from rinchi_tools import analysis


# TODO refactor functions to include new and old search implementations, comment.


def __cyclic(input_path, list_rinchis=False, search=False, permol=False, perspecmol=False):
    """
    Find cyclic changes

    Args:
        input_path:
        list_rinchis:
        search:
        permol:
        perspecmol:
    """
    pm = [False, False]
    if permol:
        pm[0] = True
    if perspecmol:
        pm[1] = True
    input_file = open('%s' % input_path).read()
    rinchis = input_file.splitlines()
    results = analysis.rxns_ring_changes(rinchis, pm)
    qualifier = ''
    if pm[0]:
        if pm[1]:
            qualifier = ' per cyclic molecule'
        else:
            qualifier = ' per molecule'
    if search:
        try:
            result = results[search]
            print('Found %d reaction(s) creating %d ring(s)%s.' % (len(result), search, qualifier))
            if list_rinchis:
                for rinchi in result:
                    print(rinchi)
        except KeyError:
            print('Could not find any reactions creating %d ring(s)%s.' % (search, qualifier))
    else:
        for ring_change in results:
            print('Reactions creating %d ring(s)%s: %d' % (ring_change, qualifier, len(results[ring_change])))
            if list_rinchis:
                for rinchi in results[ring_change]:
                    print(rinchi)


def __stereochem(input_path, list_rinchis=False, well_defined=False, sp2=True, sp3=True, search=False, permol=False,
                 perspecmol=False):
    """
    Find stereochemical changes

    Args:
        input_path:
        list_rinchis:
        well_defined:
        sp2:
        sp3:
        search:
        permol:
        perspecmol:

    """
    pm = [False, False]
    if permol:
        pm[0] = True
    if perspecmol:
        pm[1] = True
    if sp2 and sp3:
        label = 'sp2 or sp3'
    elif sp2:
        label = 'sp2'
    elif sp3:
        label = 'sp3'
    else:
        print(textwrap.fill('''Cannot search for sp3-only AND sp2-only
        stereochemical changes simultaneously...  Try again.''', 79))
        return
    input_file = open('%s' % input_path).read()
    rinchis = input_file.splitlines()
    results = analysis.rxns_stereochem_changes(rinchis, well_defined, pm, sp2, sp3)
    qualifier = ''
    if pm[0]:
        if pm[1]:
            qualifier = ' per stereo-molecule'
        else:
            qualifier = ' per molecule'
    if search:
        try:
            result = results[search]
            print('Found %d reaction(s) creating %d %s stereocentre(s)%s.' % (len(result), search, label, qualifier))
            if list_rinchis:
                for rinchi in result:
                    print(rinchi)
        except KeyError:
            print('Could not find any reactions creating %d %s stereocentre(s)%s.' % (search, label, qualifier))
    else:
        for stereochange in results:
            print('Reaction(s) creating %d %s stereocentre(s)%s: %d' % (
                stereochange, label, qualifier, len(results[stereochange])))
            if list_rinchis:
                for rinchi in results[stereochange]:
                    print(rinchi)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RInChI Analytical tools \n{}".format(__doc__))
    parser.add_argument("database", help="The existing database path to be analysed or searched")

    action = parser.add_argument_group('Main Arguments',
                                       'Choose an argument from those below.').add_mutually_exclusive_group(
        required=True)
    action.add_argument("-c", "--cyclic", action="store_true", help="Get cyclic changes in a reaction")
    action.add_argument("-st", "--stereochem", action="store_true", help="Analyse stereochemical changes")
    action.add_argument("-se", "--search", help="Search for an inchi in a list of rinchis")
    optional = parser.add_argument_group("Optional Arguments", "n.b. Some arguments only apply to certain operations.")
    optional.add_argument("-r", "--reactant", action="store_true",
                          help="Specifies searching for the query substance as a reactant")
    optional.add_argument("-p", "--product", action="store_true",
                          help="Specifies searching for the query substance as a product")
    optional.add_argument("-e", "--equilibrium", action="store_true",
                          help="Specifies searching for the query substance as an equilibrium reagent")
    optional.add_argument("-a", "--agent", action="store_true",
                          help="Specifies searching for the query substance as a reaction agent; i.e. a substance "
                               "present at the start and end of the reaction, like a catalyst or solvent.")
    optional.add_argument("-l", "--list", action="store_true", help="List the RInChIs found")
    optional.add_argument("-w", "--welldefined", action="store_true", help="Ignore undefined or omitted stereocentres")
    optional.add_argument("-sp2", "--sp2", action="store_false", help="Only search for sp2 centres.")
    optional.add_argument("-sp3", "--sp3", action="store_false", help="Only search for sp3 centres.")
    optional.add_argument("-pm", "--permol", action="store_true", help="Return changes per molecule.")
    optional.add_argument("-psm", "--perspecmol", action="store_true",
                          help="Return changes per specified type of molecule (cyclic or stereocentered)")
    optional.add_argument("-n", "--number", type=int,
                          help='Return only those reactions which create n features. Use negative n to search for '
                               'reactions which destroy features.')
    args = parser.parse_args()

    if args.cyclic:
        __cyclic(args.database, args.list, args.search, args.pm, args.psm)
    elif args.search:
        __search(args.database, args.search, args.reactant, args.product, args.equilibrium, args.agent, args.list)
    elif args.stereochem:
        __stereochem(args.database, args.list, args.welldefined, args.sp3, args.sp2, args.search, args.pm, args.psm)
    else:
        parser.print_help()
