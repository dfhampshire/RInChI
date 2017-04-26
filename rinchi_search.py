#!/usr/bin/env python3
"""
RInChI Searching Script
-----------------------

Searches an SQL database for InChIs.

Modifications:

 - B. Hammond 2014

 - D.F. Hampshire 2017

    Rewrote search function completely

"""

import argparse

from rinchi_tools import _external, database, utils
from rinchi_tools.utils import string_to_dict as sd


def add_search(subparser):
    """
    Adds the arguments for the search operation to the ``ArgumentParser`` object.

    Args:
        subparser: An ``ArgumentParser`` object
    """
    assert isinstance(subparser, argparse.ArgumentParser)

    # Add main search arguments
    subparser.add_argument("search_term", help="The search_term to find")
    subparser.add_argument("file", default=_external.RINCHI_DATABASE, help="The database or flat file to search")
    subparser.add_argument("table_name", nargs="?", default=False,
                           help="The table name for the search to be performed on. Providing this argument asserts "
                                "that the input file is an SQL database")

    # Add query options
    query = subparser.add_argument_group("Action").add_mutually_exclusive_group(required=True)
    query.add_argument('-k', '--key', nargs='?', const='N', choices=['L', 'S', 'W', 'N'],
                       help='Returns the RInChI corresponding to a given key. Optionally accepts an argument denoting '
                            'the type of key to lookup')
    query.add_argument('-i', '--inchi', action='store_true',
                       help='Returns all RInChIs containing the given InChI with filters')
    query.add_argument('-l', '--layer', action='store_true', help='Search for a component of an InChI in a database')

    # Add data input/output options
    io_options = subparser.add_argument_group('Input / Output Options')
    io_options.add_argument("-db", "--is_database", action="store_true",
                            help="Assert that the input is a database. If the table_name argument is not provided then "
                                 "the default value of 'rinchis1-00' is used")
    io_options.add_argument("-o", "--output_format", choices=['list', 'file', 'stats'], default="list",
                            help="The format of the output - must be one of 'list', 'file', 'stats'")

    # Filters for a the search
    filters = subparser.add_argument_group("Filters - the changes should be of the form 'sp2=1,sp3=-1,...'")
    filters.add_argument("-hb", "--hybridisation", help="The changes in hybridisation sought")
    filters.add_argument("-v", "--valence", help="The changes in valence sought")
    filters.add_argument("-r", "--rings", help="The changes in ring numbers sought by size")
    filters.add_argument("-f", "--formula", help="The changes in the formula sought by element")
    filters.add_argument('-re', '--ringelement', help="Search for reactions containing a certain ring type")
    filters.add_argument('-iso', "--isotopic", action='store_true',
                         help="Search for reactions containing defined isotopic layers")

    # Where to search for the InChI
    filters.add_argument("-rct", "--reactant", action="store_true", help="Search for the InChI in the reactants")
    filters.add_argument("-pdt", "--product", action="store_true", help="Search for the InChI in the products")
    filters.add_argument("-agt", "--agent", action="store_true", help="Search for the InChI in the agents")
    filters.add_argument("-n", "--number", default=1000, type=int,
                         help="Limit the number of initial search results. A value of 0 means no limit")


def search_ops(args):
    """
    Executes the search operations.

    Args:
        args: The output of the ``parser.parse_args()``
    """
    if args.table_name:
        args.is_database = True
    results = database.search_master(args.search_term, args.file, args.table_name, args.is_database,
                                     sd(args.hybridisation), sd(args.valence), sd(args.rings), sd(args.formula),
                                     args.reactant, args.product, args.agent, args.number, args.key, sd(args.ringelement),
                                     args.isotopic)

    if args.output_format == "list":
        outstring = utils.construct_output_text(results)
        print(outstring)
    if args.output_format == "file":
        utils.output(utils.construct_output_text(results), "search_result", ".rinchi")
    if args.output_format == "stats":
        total = 0
        for the_key, the_value in results.items():
            total += len(the_value)
            print('{} : {}'.format(the_key, len(the_value)))
        print('Total: {}'.format(total))


if __name__ == "__main__":
    role = "Search for RInChIs, InChIs & their components or RInChI Keys in a RInChI SQL Database / Flat File"
    parser = argparse.ArgumentParser(description=role)
    add_search(parser)
    args = parser.parse_args()
    search_ops(args)
