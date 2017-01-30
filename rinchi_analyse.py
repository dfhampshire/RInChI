#!/usr/bin/env python3

"""
RInChI analysis script.

    Copyright 2012 C.H.G. Allen
    Modified 2016 D. Hampshire

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


This script analyses RInChI databases.  These are files containing RInChIs
separated by newlines.  This script has been tested on a database of c. 2500
RInChIs.
"""

import argparse
import textwrap

from rinchi_tools import analysis


def __search(rinchi_path, inchi_path, reactant=False, product=False, eqm=False, agent=False, list_rinchis=False):
    """
    Searches a flat files containing RInChIs for a particular InChI. This is somewhat superseeded by the action of the
    search function in the database module.

    :param rinchi_path: Th path to the list of rinchis
    :param inchi_path: the path to the file containing the inchi to be searched for
    :param reactant: Look for inchi in reactants
    :param product: Look for inchi in products
    :param eqm: Look for inchi in reactants or products
    :param agent: look for inchi in agents layer
    :param list_rinchis: list the rinchis containing the inchi
    :return: none
    """
    if not (reactant or product or eqm or agent):
        reactant = True
        product = True
        eqm = True
        agent = True

    inchi_file = open('%s' % inchi_path).read()
    inchi = inchi_file.strip()
    rinchi_file = open('%s' % rinchi_path).read()
    rinchis = rinchi_file.splitlines()

    def results_publisher(role_letter, role_name):
        print(textwrap.fill('Searching for %s acting as a %s:' % (inchi, role_name), 79))
        results = analysis.search_4_inchi(inchi, rinchis, role_letter)
        print("Found %d hits!" % (len(results)))
        if list_rinchis:
            for rinchi_entry in results:
                print(rinchi_entry)
        return

    if reactant:
        results_publisher('r', 'reactant')
    if product:
        results_publisher('p', 'product')
    if eqm:
        results_publisher('e', 'equilibrium reagent')
    if agent:
        results_publisher('a', 'reaction agent')
    return


def __cyclic(input_path, list_rinchis=False, search=False, permol=False, perspecmol=False):
    """
    :param input_path:
    :param list_rinchis:
    :param search:
    :param permol:
    :param perspecmol:
    :return:
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
    return


def __stereochem(input_path, list_rinchis=False, well_defined=False, sp2=True, sp3=True, search=False, permol=False,
                 perspecmol=False):
    """
    :param input_path:
    :param list_rinchis:
    :param well_defined:
    :param sp2:
    :param sp3:
    :param search:
    :param permol:
    :param perspecmol:
    :return:
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
    return


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
