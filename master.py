#!/usr/bin/env python3
"""
RInChI Master Script. Contains all of the action of the RInChI module!

Uses a system of subparsers which can be called independently.

    Duncan Hampshire 2017

"""

import argparse
from collections import Counter

from rinchi_tools import database
from rinchi_tools.molecule import Molecule
from rinchi_tools.reaction import Reaction
from rinchi_tools.utils import Hashable


def _add_search(subparser):

    assert isinstance(subparser, argparse.ArgumentParser)

    # Add main search arguments
    subparser.add_argument("search_term", help="The search_term to find")
    subparser.add_argument("file", default="../rinchi.db",help="The database or flat file to search")
    subparser.add_argument("table_name", nargs="?", default=False,
                           help="The table name for the search to be performed on. Providing this argument asserts "
                                "that the input file is an SQL database")

    # Add action options
    action =subparser.add_argument_group("Action").add_mutually_exclusive_group(required=True)
    action.add_argument('-l','--key', action='store_true',
                        help='Returns the RInChI corresponding to a given Long Key')
    action.add_argument('-i','--inchi', action='store_true',
                        help='Returns all RInChIs containing the given InChI with filters')

    # Add search input/output options
    subparser.add_argument("-db","--is_database",action="store_true",
                           help="Assert that the input is a database. If the table_name argument is not provided then "
                                "the default value of 'rinchis03' is used")
    subparser.add_argument("-o", "--output_format", choices=['list', 'file', 'stats'], default="list",
                           help="The format of the output - must be one of 'list', 'file', 'stats'")

    # Filters for a the search
    subparser.add_argument("-hb", "--hybridisation", type=dict,
                           help="The changes in hybridisation sought as a python style dictionary")
    subparser.add_argument("-v", "--valence", type=dict,
                           help="The changes in valence sought as a python style dictionary")
    subparser.add_argument("-r", "--rings", type=dict,
                           help="The changes in ring numbers sought as a python style dictionary")
    subparser.add_argument("-f","--formula", type=dict,
                           help="The changes in the formula sought as a python style dictionary")

    # Where to search for the InChI
    subparser.add_argument("-rt","--reactant",action="store_true",help="Search for the InChI in the reactants")
    subparser.add_argument("-pt","--product",action="store_true",help="Search for the InChI in the products")
    subparser.add_argument("-a", "--agent", action="store_true", help="Search for the InChI in the agents")
    subparser.add_argument("-n", "--number", default=1000, help="Limit the number of initial search results")





    subparser.add_argument("--ringsearch", action="store_true",
                           help="Search a collection of RInChIs for a specific ring type, ")

    subparser.add_argument("--isotopic", action="store_true",
                           help="Search for reactions containing defined isotopic layers")
    subparser.add_argument("--ringelements", action="store_true", help="Search for reaction")
    subparser.add_argument("--quick", action="store_true", help="Speed up search at cost of accuracy")


def _add_file_convert(subparser):

    assert isinstance(subparser, argparse.ArgumentParser)

    subparser.add_argument("input_path", help="The path of the file or folder to be converted")

    # Add options for the type of conversion desired
    action = subparser.add_argument_group('Conversion Type',
                                          'Choose a type of conversion').add_mutually_exclusive_group(required=True)
    action.add_argument("--rxn2rinchi", action="store_true", help="RXN to RInChI conversion")
    action.add_argument("--rdf2rinchi", action="store_true", help="RDF to RInChI conversion")
    action.add_argument("--rinchi2file", action="store_true",
                        help="RInChI-to-File conversion. Accepts any file containing a rinchi and optionally rauxinfo. "
                             "The RAuxInfo must immediately follow the RInChI")
    action.add_argument("--rinchi2key", action="store_true", help="RInChi to RInChI-Key conversion")
    action.add_argument('--rdf2csv', action='store_true', help='Create or append a .csv with an rdfile')
    action.add_argument('--dir2csv', action='store_true', help='Convert a directory of rdfiles to a single csv file')
    action.add_argument("--svg", action="store_true", help="Convert a RInChI to a collection of .svg files")

    optional = subparser.add_argument_group("Optional Arguments")

    # Add options for all commands
    opt_all = optional.add_argument_group("All operations")
    opt_all.add_argument("-f", "--fileout", action="store_true", help="Save the output to disk")

    # Add options for converting to RInChI filetype
    opt_to_rinchi = optional.add_argument_group("Conversion to RInChI file")
    opt_to_rinchi.add_argument("-e", "--equilibrium", action="store_true",
                               help="Force output to be an equilibrium reaction")
    opt_to_rinchi.add_argument("-ra", "--rauxinfo", action="store_true", help="Generate and return RAuxInfo")
    opt_to_rinchi.add_argument("-l", "--longkey", action="store_true",
                               help="Generate and return the Long-RInChIKey along with the RInChI")
    opt_to_rinchi.add_argument("-s", "--shortkey", action="store_true",
                               help="Generate and return the Short-RInChIKey along with the RInChI")
    opt_to_rinchi.add_argument("-w", "--webkey", action="store_true",
                               help="Generate and return the Web-RInChIKey along with the RInChI")

    # Add options for converting to Keys
    opt_to_key = optional.add_argument_group("Converting RInChIs to Keys")
    opt_to_key.add_argument("-i", "--include_rinchi", action="store_true", help="Include original RInChI in the output")

    # Add options for converting to RXN/RDF
    opt_to_file = optional.add_argument_group("Converting to a RXN/RDF")
    opt_to_file.add_argument("-ordf", "--rdfileoutput", action="store_true", help="Output as RDFile")
    opt_to_file.add_argument("-orxn", "--rxnoutput", action="store_true", help="Output as RXN file(s)")


def _add_database(subparser):

    assert isinstance(subparser, argparse.ArgumentParser)

    # Add main input arguments
    subparser.add_argument("database", nargs="?",default="../rinchi.db",
                           help="The existing database to manipulate, or the name of database to be created")
    subparser.add_argument("input", nargs="?",default="rinchis03", help="The name of the input data file or table")
    subparser.add_argument('-o',"--output", nargs="?",
                           help="The output table name or something else to output")

    action = subparser.add_argument_group("Operation").add_mutually_exclusive_group(required=True)

    # Add data insertion options
    adding = action.add_argument_group("Adding Data to a database")
    adding.add_argument('--rdf2db', action='store_true', help='Convert and add an rdfile to an SQL database')
    adding.add_argument('--csv2db', action='store_true',
                        help='Add the contents of a rinchi .csv file to an SQL database')

    # Add fingerprint related operations
    fpts = action.add_argument_group("Fingerprints")
    fpts.add_argument('--ufingerprints', action='store_true',
                      help='Adds new entries to the fpts table containing fingerprint data')
    fpts.add_argument('--rfingerprints', action='store_true', help='Returns the fingerprint of a given key')
    fpts.add_argument('--cfingerprints', action='store_true',
                      help='Returns all RInChIs containing the given InChI to STDOUT')

    # Add converting data operations
    convert = action.add_argument_group("Converting databases")
    convert.add_argument('--convert2_to_3', action='store_true',
                         help='Creates a new table of v.03 rinchis from a table of v.02 rinchis')
    convert.add_argument('--generate_rauxinfo', action='store_true',
                         help='Generate RAuxInfos from rinchis within a SQL database')


def _add_changes(subparser):

    assert isinstance(subparser,argparse.ArgumentParser)

    subparser.add_argument("input", help="The file or string containing RInChI(s) or Long Key to be processed")

    # Add process arguments
    action = subparser.add_mutually_exclusive_group(required=True)
    action.add_argument('-b', '--batch', action='store_true', help='Process multiple RInChIs')
    action.add_argument('-r', '--rinchi', action='store_true', help='Process a single RInChI')
    action.add_argument("-k","--key", action="store_true", help="Process a RInChI key")

    # Add file options
    file_opt = subparser.add_argument_group("File options")
    file_opt.add_argument("--list", action="store_true", help="List RInChIs along with results. Otherwise returns count populations")
    file_opt.add_argument("--filein",action="store_true",help="Assert that the input is a file")

    # Add operation arguments
    operation = subparser.add_argument_group("Operation")
    operation.add_argument("--ringcount", action="store_true", help="Calculate the change in ring populations")
    operation.add_argument("--formula", action="store_true", help="Calculate the change in formula across a reaction")
    operation.add_argument("--valence", action="store_true", help="Change in valence across reaction")
    operation.add_argument("--hybrid", action="store_true", help="Change in hybridisation of C atoms across reaction")
    operation.add_argument("--ringcountelements", nargs="?", const=True, help="Calculate the change in ring populations with ")


def _changes_ops(args):

    try:
        if args.key and args.input.startswith("Long-RInChIKey"):
            args.input = database.sql_key_to_rinchi(args.input, "rinchi.db", args.arg2)
            args.rinchi = True
    except ValueError:
        print("Could not find Long-RInChIKey in database")
        pass

    if args.rinchi:
        # Opens the file if the input is file containing a single RInChI. Otherwise it treats the input as RInChI itself
        if args.filein:
            try:
                with open(args.input) as f:
                    args.input = f.readline()
                    if args.list:
                        print(args.input)
            except IOError:
                pass

        if args.ringcount:
            r = Reaction(args.input)
            print(r.change_across_reaction(Molecule.get_ring_count))
        elif args.formula:
            r = Reaction(args.input)
            print(r.change_across_reaction(Molecule.get_formula))
        elif args.valence:
            r = Reaction(args.input)
            print(r.change_across_reaction(Molecule.get_valence_count))
        elif args.hybrid:
            r = Reaction(args.input)
            print(r.change_across_reaction(Molecule.get_hybrid_count))
        elif args.ringcountelements:
            r = Reaction(args.input)
            print(r.change_across_reaction(Molecule.get_ring_count_inc_elements,loop=True))

    elif args.batch:
        master_counter = {'ringcount': Counter(),'formula': Counter(),'ringcountelements': Counter(),'valence': Counter(),'hybrid': Counter()}
        with open(args.input) as data:
            for rinchi in data:
                r = Reaction(rinchi)
                if args.list:
                    print(rinchi)
                if args.ringcount:
                    # Count the change in ring populations across the reactions
                    ringcount = r.change_across_reaction(Molecule.get_ring_count)
                    if ringcount and args.list:
                        print(ringcount)
                    elif ringcount:
                        master_counter['ringcount'].update(Hashable(ringcount))
                elif args.ringcountelements:
                    # Count the change in rings returning the change in elemental structure of the rings
                    # e.g.  (CCCCCN : 1) would indicate the reaction forms a
                    # pyridine ring
                    ringcountelements = r.change_across_reaction(Molecule.get_ring_count_inc_elements, args.args2, loop=True)
                    if ringcountelements and args.list:
                        print(ringcountelements)
                    elif ringcountelements:
                        master_counter['ringcountelements'].update(Hashable(ringcountelements))
                elif args.formula:
                    formula = r.change_across_reaction(Molecule.get_formula)
                    if formula and args.list:
                        print(formula)
                    elif formula:
                        master_counter['ringcount'].update(Hashable(formula))
                elif args.valence:
                    valence = r.change_across_reaction(Molecule.get_valence_count)
                    if valence and args.list:
                        print(valence)
                    elif valence:
                        master_counter['ringcount'].update(Hashable(valence))
                elif args.hybrid:
                    hybrid = r.change_across_reaction(Molecule.get_hybrid_count)
                    if hybrid and args.list:
                        print(hybrid)
                    elif hybrid:
                        master_counter['ringcount'].update(Hashable(hybrid))
        for key, value in master_counter.items():
            print(key,"  ",value)
    else:
        parser.print_help()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RInChI Master Script \n{}".format(__doc__))

    # Create subparser list
    main_functions = parser.add_subparsers(help='Main Function')

    # Create Search functionality
    search_role = 'Search for an InChi or Key within a RInChI database or flat file'
    search_parser = main_functions.add_parser('search', description=search_role, help=search_role)
    _add_search(search_parser)

    # Add file conversion functionality
    convert_role = "Convert a file to/from RInChIs"
    convert_parser = main_functions.add_parser('convert', description=convert_role, help=convert_role)
    _add_file_convert(convert_parser)

    # Add databasing tools
    database_role = "Database manipulation tools"
    database_parser = main_functions.add_parser('db', description=database_role,help=database_role)
    _add_database(database_parser)

    # Add rinchi analysis tools
    rinchi_role = "RInChI Analysis and Manipulation"
    rinchi_parser = main_functions.add_parser('rinchi', definition=rinchi_role,help=rinchi_role)
    _add_changes(rinchi_parser)

    parser.parse_args()

    if False:
        print(1)
    else:
        parser.print_help()

