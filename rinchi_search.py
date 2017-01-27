#!/usr/bin/env python3

# NEW PYTHON SCRIPTS
# TESTING PHASE

# BENJAMIN HAMMOND 2014


import argparse

import rinchi_database
from rinchi_tools import rinchi


def advanced_search(db_filename, inchi, table_name, hyb=None, val=None, rings=None, formula=None):
    if hyb is None:
        hyb = {}
    if val is None:
        val = {}
    if rings is None:
        rings = {}
    if formula is None:
        formula = {}
    print("Starting search:")
    rinchis = rinchi_database.search_for_inchi(inchi, db_filename, table_name)
    print(len(rinchis), "inchi matches found")

    counter = 0
    for rin in rinchis:
        r = rinchi.Reaction(rin)
        if r.detect_reaction(hyb_i=hyb, val_i=val, rings_i=rings, formula_i=formula):
            counter += 1
            print(r.rinchi)

    print(counter, "exact matches found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for an InChi within a RInChI database")
    parser.add_argument("database", help="")
    parser.add_argument("inchi", nargs="?", help="The Inchi to find")
    parser.add_argument("tablename",nargs="?",help="The table name for the seach to be performed on")
    parser.add_argument("-o","--outputrinchis",action="store_true",help="Output the RInChis themselves")

    args = parser.parse_args()

    if args.s:
        advanced_search(args.database, args.tablename,args.inchi, rings={6: 1}, hyb={"sp2": -4, "sp3": 4})
