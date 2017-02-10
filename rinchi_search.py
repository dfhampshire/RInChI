#!/usr/bin/env python3
"""
RInChI Searching Script

Searches an SQL database for InChIs.

    D. Hampshire 2017 - Rewrote search function completely. Based on the work of B. Hammond 2014
"""

import argparse

from rinchi_tools import utils


def __search(inchi, db=None, table_name=None, is_sql_db=False, hyb=None, val=None, rings=None, formula=None,
             reactant=False, product=False, agent=False, limit=1000, out_format="list"):
    results = db.search_master(inchi, db, table_name, is_sql_db, hyb, val, rings, formula, reactant,
                               product, agent, limit)
    if out_format == "list":
        print(utils.construct_output_text(results))
    if out_format == "file":
        utils.output(utils.construct_output_text(results),"search_result","rinchi")
    if out_format == "stats":
        num_r = len(results['as_reactant'])
        num_p = len(results['as_product'])
        num_a = len(results['as_agent'])
        total = num_r + num_p + num_a
        print('Number with Inchi as a Reactant : {}'.format(num_r))
        print('Number with Inchi as a Product : {}'.format(num_p))
        print('Number with Inchi as a Agent : {}'.format(num_a))
        print('Total: {}'.format(total))


def add_search(subparser):

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
    subparser.add_argument("-hb", "--hybridisation", type=json.loads,
                           help="The changes in hybridisation sought as a python style dictionary")
    subparser.add_argument("-v", "--valence", type=json.loads,
                           help="The changes in valence sought as a python style dictionary")
    subparser.add_argument("-r", "--rings", type=json.loads,
                           help="The changes in ring numbers sought as a python style dictionary")
    subparser.add_argument("-f","--formula", type=json.loads,
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

def search_ops(args, parser):
    """

    Args:
        args:
        parser:

    Returns:

    """
    if args.table_name:
        args.is_database = True
    try:
        __search(args.inchi,args.file,args.tablename,args.is_database,args.hybridisation,args.valence,args.rings,
                 args.formula,args.reactant,args.product,args.agent,args.limit,args.output_format)
    except Exception as detail:
        print(detail)
        parser.print_help()


if __name__ == "__main__":
    role = "Search for an InChi within a RInChI database or flat file"
    parser = argparse.ArgumentParser(description=role)
    add_search(parser)
    args = parser.parse_args()
    search_ops(args,parser)
