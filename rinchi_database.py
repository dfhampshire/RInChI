#!/usr/bin/env python3
"""
RInChI databasing tools script

Converts, creates, and removes from SQL databases

    B. Hammond 2014
    D. Hampshire 2016 - Major features added

"""

import argparse

import rinchi_tools.conversion
from rinchi_tools import database
from rinchi_tools.rinchi_lib import RInChI as RInChI_Handle


def add_db(subparser):
    """

    Args:
        subparser:
    """
    assert isinstance(subparser, argparse.ArgumentParser)

    # Add main input arguments
    subparser.add_argument("database", nargs="?", default="../rinchi.db",
                           help="The existing database to manipulate, or the name of database to be created")
    subparser.add_argument("input", nargs="?", default="rinchis03", help="The name of the input data file or table")
    subparser.add_argument('-o', "--output", nargs="?", help="The output table name or something else to output")

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


def db_ops(args, parser):
    """

    Args:
        args:
        parser:
    """
    if args.lkey2rxninfo and args.input.startswith("RInChI"):
        try:
            args.input = RInChI_Handle().rinchikey_from_rinchi(args.input, "L")
        except ValueError:
            print("Could not convert RInChI to Long-RInChI-key")
            pass

    if args.rdf2csv:
        rinchi_tools.conversion.rdf_to_csv(args.input, return_longkey=True, return_rxninfo=True)
    if args.rdfappend:
        rinchi_tools.conversion.rdf_to_csv_append(args.input, args.database)
    if args.dir2csv:
        rinchi_tools.conversion.create_csv_from_directory(args.input, args.database, return_longkey=True,
                                                          return_rxninfo=True)
    if args.rdf2sql:
        database.rdf_to_sql(args.input, args.database, args.tablename)
    if args.csv2sql:
        database.csv_to_sql(args.input, args.database, args.tablename)

    if args.ufingerprints:
        database.update_fingerprints(args.input, args.database, args.tablename)
    if args.rfingerprints:
        print(list(database.recall_fingerprints(args.input, args.database, args.tablename)))
    if args.cfingerprints:
        database.compare_fingerprints(args.input, args.database, args.tablename)
    if args.lkey2rinchi:
        print(database.sql_key_to_rinchi(args.input, args.database, args.tablename))
    if args.conv0203:
        # Names hardcoded because significant modification of the arparse system would be needed and would be complex
        v02_column_names = ["rinchi", "rauxinfo"]
        v03_column_names = ["rinchi", "rauxinfo", "longkey", "shortkey", "webkey"]
        column_names = v02_column_names + v03_column_names
        database.convert_v02_v03(args.database, args.input, *column_names)
    if args.genrauxinfo:
        database.gen_rauxinfo(args.database, args.input)
    else:
        parser.print_help()


if __name__ == "__main__":
    role = "Database Tools Module"
    parser = argparse.ArgumentParser(description=role)
    add_db(parser)
    args = parser.parse_args()
    db_ops(args, parser)
