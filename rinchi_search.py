#!/usr/bin/env python3

# NEW PYTHON SCRIPTS
# TESTING PHASE

# BENJAMIN HAMMOND 2014


import argparse

import rinchi_database
import rinchi_rings


def advanced_search(db_filename, inchis=None, hyb=None, val=None, rings=None, formula=None):
    if hyb is None:
        hyb = {}
    if val is None:
        val = {}
    if rings is None:
        rings = {}
    if formula is None:
        formula = {}
    print("Starting search:")
    rinchis = rinchi_database.search_for_inchi(inchis, db_filename)
    print(len(rinchis), "inchi matches found")

    counter = 0
    for rin in rinchis:
        r = rinchi_rings.Reaction(rin)
        if r.detect_reaction(hyb_i=hyb, val_i=val, rings_i=rings, formula_i=formula):
            counter += 1
            # print r.rinchi

    print(counter, "exact matches found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TEST POST PLEASE IGNORE")
    parser.add_argument("database", help="")
    parser.add_argument("input", nargs="?", help="")

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--s', action='store_true', help='Search')

    args = parser.parse_args()

    if args.s:
        advanced_search(args.database, args.input, rings={6: 1}, hyb={"sp2": -4, "sp3": 4})
