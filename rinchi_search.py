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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for an InChi within a RInChI database or flat file")
    parser.add_argument("file", default="../rinchi.db",help="The database or flat file to search")
    parser.add_argument("inchi", help="The Inchi to find")
    parser.add_argument("table_name", nargs="?", default=False, help="The table name for the search to be performed on")
    parser.add_argument("-db","--is_database",action="store_true",help="Assert that the input is a database")
    parser.add_argument("-o", "--output_format", choices=['list', 'file', 'stats'], default="list",
                        help="The format of the output - must be one of 'list', 'file', 'stats'")
    parser.add_argument("-h", "--hybridisation", type=dict,
                        help="The changes in hybridisation sought as a python style dictionary")
    parser.add_argument("-v", "--valence", type=dict,
                        help="The changes in valence sought as a python style dictionary")
    parser.add_argument("-r", "--rings", type=dict,
                        help="The changes in ring numbers sought as a python style dictionary")
    parser.add_argument("-f","--formula", type=dict,
                        help="The changes in the formula sought as a python style dictionary")
    parser.add_argument("-rt","--reactant",action="store_true",help="Search for the InChI in the reactants")
    parser.add_argument("-pt","--product",action="store_true",help="Search for the InChI in the products")
    parser.add_argument("-a", "--agent", action="store_true", help="Search for the InChI in the agents")
    parser.add_argument("-l", "--limit", default=1000, help="Limit the number of initial search results")

    args = parser.parse_args()

    if args.table_name:
        args.is_database = True
    try:
        __search(args.inchi,args.file,args.tablename,args.is_database,args.hybridisation,args.valence,args.rings,
             args.formula,args.reactant,args.product,args.agent,args.limit,args.output_format)
    except Exception as detail:
        print(detail)
        parser.print_help()


