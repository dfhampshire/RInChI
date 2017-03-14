#!/usr/bin/env python3
"""
RInChI databasing tools script

Converts, creates, and removes from SQL databases

    B. Hammond 2014
    D. Hampshire 2016 - Major features added

"""

import argparse

from rinchi_tools import _external, database


def add_db(subparser):
    """

    Args:
        subparser:
    """
    assert isinstance(subparser, argparse.ArgumentParser)

    # Add main input arguments
    subparser.add_argument("database", nargs="?", default=_external.RINCHI_DATABASE,
                           help="The existing database to manipulate, or the name of database to be created")
    subparser.add_argument("input", nargs="?", default="rinchis03", help="The name of the input data file or table")
    subparser.add_argument('-o', "--output", nargs="?", help="The output table name or something else to output")

    # Add data insertion options
    adding = subparser.add_argument_group("Adding Data to a database")
    adding.add_argument('--rdf2db', action='store_true', help='Convert and add an rdfile to an SQL database')
    adding.add_argument('--csv2db', action='store_true',
                        help='Add the contents of a rinchi .csv file to an SQL database')

    # Add fingerprint related operations
    fpts = subparser.add_argument_group("Fingerprints")
    fpts.add_argument('--ufingerprints', action='store_true',
                      help='Adds new entries to the fpts table containing fingerprint data')
    fpts.add_argument('--rfingerprints', action='store_true', help='Returns the fingerprint of a given key')
    fpts.add_argument('--cfingerprints', action='store_true',
                      help='Returns all RInChIs containing the given InChI to STDOUT')

    # Add converting data operations
    convert = subparser.add_argument_group("Converting operations")
    convert.add_argument('--convert2_to_3', action='store_true',
                         help='Creates a new table of v.03 rinchis from a table of v.02 rinchis')
    convert.add_argument('--generate_rauxinfo', action='store_true',
                         help='Generate RAuxInfos from rinchis within a SQL database')
    convert.add_argument('-k', '--key', nargs='?', const='L', choices=['L', 'S', 'W'],
                         help='Returns the RInChI corresponding to a given key. Optionally accepts an argument '
                              'denoting the type of key to lookup ')


def db_ops(args, parser):
    """

    Args:
        args:
        parser:
    """
    args.output = args.output
    if args.rdf2db:
        database.rdf_to_sql(args.input, args.database, args.output)
    if args.csv2db:
        database.csv_to_sql(args.input, args.database, args.output)
    if args.ufingerprints:
        database.update_fingerprints(args.input, args.database, args.output)
    if args.rfingerprints:
        print(list(database.recall_fingerprints(args.input, args.database, args.output)))
    if args.cfingerprints:
        database.compare_fingerprints(args.input, args.database, args.output)
    if args.key:
        print(database.sql_key_to_rinchi(args.input, args.database, args.output, args.key))
    if args.convert2_to_3:
        # Names hardcoded because significant modification of the arparse system would be needed and would be complex
        v02_column_names = ["rinchi", "rauxinfo"]
        v03_column_names = ["rinchi", "rauxinfo", "longkey", "shortkey", "webkey"]
        column_names = v02_column_names + v03_column_names
        database.convert_v02_v03(args.database, args.input, *column_names)
    if args.generate_rauxinfo:
        database.gen_rauxinfo(args.database, args.input)


if __name__ == "__main__":
    role = "Database Tools Module"
    parser = argparse.ArgumentParser(description=role)
    add_db(parser)
    args = parser.parse_args()
    db_ops(args, parser)
