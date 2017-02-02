#!/usr/bin/env python3
"""
Search program for a python database.

BENJAMIN HAMMOND 2014

Significant restructuring and feature adding DUNCAN HAMPSHIRE 2017

"""

import argparse

from rinchi_tools import database

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for an InChi within a RInChI database")
    parser.add_argument("database", help="")
    parser.add_argument("inchi", nargs="?", help="The Inchi to find")
    parser.add_argument("tablename", nargs="?", help="The table name for the seach to be performed on")
    parser.add_argument("-o", "--outputrinchis", action="store_true", help="Output the RInChis themselves")

    args = parser.parse_args()

    if args.s:
        database.advanced_search(args.inchi, args.database, args.tablename, rings={6: 1}, hyb={"sp2": -4, "sp3": 4})
