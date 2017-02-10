#!/usr/bin/env python3
"""
RInChI Master Script. Contains all of the action of the RInChI module!

Uses a system of subparsers which can be called independently.

    Duncan Hampshire 2017

"""

import argparse

import rinchi_add
import rinchi_changes
import rinchi_search
from rinchi_convert import _add_file_convert


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RInChI Master Script \n{}".format(__doc__))

    # Create subparser list
    main_functions = parser.add_subparsers(help='Main Function')

    # Create Search functionality
    search_role = 'Search for an InChi or Key within a RInChI database or flat file'
    search_parser = main_functions.add_parser('search', description=search_role, help=search_role, dest='op')
    rinchi_search.add_search(search_parser)

    # Add file conversion functionality
    convert_role = "Convert a file to/from RInChIs"
    convert_parser = main_functions.add_parser('convert', description=convert_role, help=convert_role, dest='op')
    _add_file_convert(convert_parser)

    # Add databasing tools
    database_role = "Database manipulation tools"
    database_parser = main_functions.add_parser('db', description=database_role, help=database_role, dest='op')
    _add_database(database_parser)

    # Add rinchi analysis tools
    changes_role = "RInChI Changes Analysis"
    changes_parser = main_functions.add_parser('changes', description=changes_role, help=changes_role, dest='op')
    rinchi_changes.add_changes(changes_parser)

    # Add addition functionality
    addition_role = "RInChI addition"
    addition_parser = main_functions.add_parser(description=addition_role, help=addition_role,dest='op')
    rinchi_add.add_addition(addition_parser)

    args = parser.parse_args()

    # Direct to the appropriate parser command
    if args.command == 'search':
        rinchi_search.search_ops(args,search_parser)
    elif args.command == 'convert':
        pass
    elif args.command == 'db':
        pass
    elif args.command == 'changes':
        rinchi_changes.changes_ops(args,changes_parser)
    elif args.command == 'addition':
        rinchi_add.addition_ops(args, parser)
    else:
        parser.print_help()

