#!/usr/bin/env python3

"""
RInChI analysis script.

    Copyright 2012 C.H.G. Allen

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


Substance search:

    Invoked by having -search as the script's first argument.

    Sample use:
        ./rinchi_analysis -search /some/path/query.inchi
            /some/path/database.rinchi -options

    Options:
        -reactant
            Specifies searching for the query substance as a reactant.
        -product
            Specifies searching for the query substance as a product.
        -eq
            Specifies searching for the query substance as an equilibrium
            reagent.
        -agent
            Specifies searching for the query substance as a reaction agent;
            i.e. a substance present at the start and end of the reaction, like
            a catalyst or solvent.
        -list
            List the RInChIs found matching the query.

    N.B. The options can be used in tandem (e.g. use -product and -eq to search
        for the query substance as either a product or equilibrium agent.
        Specifying none has the same effect as specifying them all.


Stereochemical Analysis:

    Invoked by having -stereochem as the script's first argument.

    Sample use:
        ./rinchi_analysis -stereochem /some/path/database.rinchi -options

    Options:
        -list
            List the RInChIs found.
        -wd
            Ignore undefined or omitted stereocentres.
        -sp2
            Only search for sp2 centres.
        -sp3
            Only search for sp3 centres.
        -pm
            Return stereochanges-per-molecule.
        -psm
            Return stereochanges-per-stereochemical-molecule.
        -search:n
            Return only those reactions which create n stereocentres.  Use
            negative n to search for reactions which destroy stereocentres.


Cyclic Analysis:

    Invoked by having -cyclic as the script's first argument.

    Sample use:
        ./rinchi_analysis -cyclic /some/path/database.rinchi -options

    Options:
        -list
            List the RInChIs found.
        -pm
            Return cyclic changes-per-molecule.
        -pcm
            Return cyclic changes-per-cyclic-molecule.
        -search:n
            Return only those reactions which create n rings.  Use negative n
            to search for reactions which destroy rings.
"""

import sys
import textwrap

from rinchi_tools import analysis


def __search(args):
    """Called when module run as a script."""
    # Check that a RInChI file is specified.
    if not len(args) > 1:
        print("Please specify both an InChI and a RInChI file.")
        return
    reactant = False
    product = False
    equilib = False
    agent = False
    list_rinchis = False
    for arg in args[2:]:
        if arg.startswith('-r'):
            reactant = True
        if arg.startswith('-p'):
            product = True
        if arg.startswith('-e'):
            equilib = True
        if arg.startswith('-a'):
            agent = True
        if arg.startswith('-l'):
            list_rinchis = True
    if not (reactant or product or equilib or agent):
        reactant = True
        product = True
        equilib = True
        agent = True
    inchi_path = args[0]
    inchi_file = open('%s' % inchi_path).read()
    inchi = inchi_file.strip()
    rinchi_path = args[1]
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
    if equilib:
        results_publisher('e', 'equilibrium reagent')
    if agent:
        results_publisher('a', 'reaction agent')
    return


def __cyclic(args):
    """Called when module run as a script."""
    # Check that a RInChI file is specified.
    if not args:
        print("Please specify a RInChI file for analysis.")
        return
    list_rinchis = False
    search = False
    pm = (False, False)
    for arg in args[1:]:
        if arg.startswith('-l'):
            list_rinchis = True
        if arg.startswith('-search:'):
            search = True
            search_num = int(arg[8:])
        if arg == '-pm':
            pm = (True, False)
        if arg == '-pcm':
            pm = (True, True)
    input_path = args[0]
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
            result = results[search_num]
            print('Found %d reaction(s) creating %d ring(s)%s.' % (len(result), search_num, qualifier))
            if list_rinchis:
                for rinchi in result:
                    print(rinchi)
        except KeyError:
            print('Could not find any reactions creating %d ring(s)%s.' % (search_num, qualifier))
    else:
        for ring_change in results:
            print('Reactions creating %d ring(s)%s: %d' % (ring_change, qualifier, len(results[ring_change])))
            if list_rinchis:
                for rinchi in results[ring_change]:
                    print(rinchi)
    return


def __stereochem(args):
    """Called when module run as a script."""
    # Check that a RInChI file is specified.
    if not args:
        print("Please specify a RInChI file for analysis.")
        return
    list_rinchis = False
    well_defined = False
    sp2 = True
    sp3 = True
    search = False
    pm = (False, False)
    for arg in args[1:]:
        if arg.startswith('-l'):
            list_rinchis = True
        if arg.startswith('-wd'):
            well_defined = True
        if arg.startswith('-sp2'):
            sp3 = False
        if arg.startswith('-sp3'):
            sp2 = False
        if arg.startswith('-search:'):
            search = True
            search_num = int(arg[8:])
        if arg == '-pm':
            pm = (True, False)
        if arg == '-psm':
            pm = (True, True)
    if not (sp2 or sp3):
        print(textwrap.fill('''Cannot search for sp3-only AND sp2-only
            stereochemical changes simultaneously...  Try again.''', 79))
        return
    if sp2 and sp3:
        label = 'sp2 or sp3'
    elif sp2:
        label = 'sp2'
    elif sp3:
        label = 'sp3'
    input_path = args[0]
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
            result = results[search_num]
            print(
                'Found %d reaction(s) creating %d %s stereocentre(s)%s.' % (len(result), search_num, label, qualifier))
            if list_rinchis:
                for rinchi in result:
                    print(rinchi)
        except KeyError:
            print('Could not find any reactions creating %d %s stereocentre(s)%s.' % (search_num, label, qualifier))
    else:
        for stereochange in results:
            print('Reaction(s) creating %d %s stereocentre(s)%s: %d' % (
                stereochange, label, qualifier, len(results[stereochange])))
            if list_rinchis:
                for rinchi in results[stereochange]:
                    print(rinchi)
    return


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command_line_args = sys.argv[2:]
        if sys.argv[1] == '-cyclic':
            __cyclic(command_line_args)
        elif sys.argv[1] == '-search':
            __search(command_line_args)
        elif sys.argv[1] == '-stereochem':
            __stereochem(command_line_args)
        else:
            print('First argument must be one of:')
            print('-search')
            print('-cyclic')
            print('-stereochem')
    else:
        print(__doc__)
