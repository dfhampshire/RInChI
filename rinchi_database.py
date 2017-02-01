#!/usr/bin/env python3
"""
# NEW PYTHON SCRIPTS
# TESTING PHASE

# RInChI Project
# BENJAMIN HAMMOND 2014
"""

import argparse

from rinchi_tools.database import rdf_to_csv, rdf_to_csv_append, create_csv_from_directory, rdf_to_sql, csv_to_sql, \
    sql_key_to_rinchi, compare_fingerprints, recall_fingerprints, update_fingerprints, search_for_inchi, \
    convert_v02_v03, gen_rauxinfo
from rinchi_tools.rinchi_lib import RInChI as RInChI_Handle

#######################################
# GENERATION AND CONVERSION OF DATABASES
#######################################


#####################################
# SEARCHING OF DATABASES
#####################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A collection of RInChI Tools")
    parser.add_argument("input",
                        help="Input - the RDFile or directory to be processed, or the search parameter for a search, or new table to be created")
    parser.add_argument("database", nargs="?",
                        help="The existing database to be modified or searched, or the name of new database to be created")
    parser.add_argument("tablename", nargs="?", help="The table name")

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--rdf2csv', action='store_true', help='Create a new .csv from an rdfile')
    action.add_argument('--rdfappend', action='store_true',
                        help='Append the contents of an rdfile to an existing .csv file')
    action.add_argument('--dir2csv', action='store_true', help='Convert a directory of rdfiles to a single csv file')
    action.add_argument('--rdf2sql', action='store_true', help='Convert and add an rdfile to an SQL database')
    action.add_argument('--csv2sql', action='store_true',
                        help='Add the contents of a rinchi .csv file to an SQL database')

    action.add_argument('--lkey2rinchi', action='store_true',
                        help='Returns the RInChI corresponding to a given Long Key')
    action.add_argument('--inchisearch', action='store_true',
                        help='Returns all RInChIs containing the given InChI to STDOUT')
    action.add_argument('--TEST', action='store_true', help='Returns all RInChIs containing the given InChI to STDOUT')

    action.add_argument('--ufingerprints', action='store_true',
                        help='Adds new entries to the fpts table containing fingerprint data')
    action.add_argument('--rfingerprints', action='store_true', help='Returns the fingerprint of a given key')
    action.add_argument('--cfingerprints', action='store_true',
                        help='Returns all RInChIs containing the given InChI to STDOUT')
    action.add_argument('--conv0203', action='store_true',
                        help='Creates a new table of v.03 rinchis from a table of v.02 rinchis')
    action.add_argument('--genrauxinfo', action='store_true',
                        help='Generate RAuxinfos from rinchis within a SQL database')

    args = parser.parse_args()

    if args.lkey2rxninfo and args.input.startswith("RInChI"):
        try:
            args.input = RInChI_Handle().rinchikey_from_rinchi(args.input, "L")
        except ValueError:
            print("Could not convert RInChI to Long-RInChI-key")
            pass

    if args.rdf2csv:
        rdf_to_csv(args.input, return_longkey=True, return_rxninfo=True)
    if args.rdfappend:
        rdf_to_csv_append(args.input, args.database)
    if args.dir2csv:
        create_csv_from_directory(args.input, args.database, return_longkey=True, return_rxninfo=True)
    if args.rdf2sql:
        rdf_to_sql(args.input, args.database, args.tablename)
    if args.csv2sql:
        csv_to_sql(args.input, args.database, args.tablename)

    if args.ufingerprints:
        update_fingerprints(args.input, args.database, args.tablename)
    if args.rfingerprints:
        print(list(recall_fingerprints(args.input, args.database, args.tablename)))
    if args.cfingerprints:
        compare_fingerprints(args.input, args.database, args.tablename)

    if args.TEST:
        tinchis = ["InChI=1S/C3H5Cl/c1-2-3-4/h2H,1,3H2", "InChI=1S/C3H5Br/c1-2-3-4/h2H,1,3H2",
                   "InChI=1S/C3H5I/c1-2-3-4/h2H,1,3H2", "InChI=1S/C3H6O/c1-2-3-4/h2,4H,1,3H2",
                   "InChI=1S/C3H5F/c1-2-3-4/h2H,1,3H2", "InChI=1S/C3H6/c1-3-2/h3H,1H2,2H3"]
        for inchi in tinchis:
            print(inchi, len(search_for_inchi(inchi, args.database, args.tablename)))

    if args.lkey2rinchi:
        print(sql_key_to_rinchi(args.input, args.database, args.tablename))
    if args.inchisearch:
        print("start")
        search_for_inchi(args.input, args.database, args.tablename)
    if args.conv0203:
        # Names hardcoded because significant modification of the arparse system would be needed and would be complex
        v02_column_names = ["rinchi", "rauxinfo"]
        v03_column_names = ["rinchi", "rauxinfo", "longkey", "shortkey", "webkey"]
        column_names = v02_column_names + v03_column_names
        convert_v02_v03(args.database, args.input, *column_names)
    if args.genrauxinfo:
        gen_rauxinfo(args.database, args.input)
    else:
        print(__doc__)
