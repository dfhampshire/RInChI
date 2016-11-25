"""
Performs SQLite3 operations on a database
"""

import argparse
import sqlite3

from rinchi_tools import v02_convert, utils


def gen_rauxinfo(db_filename, table_name):
    """
    Updates a table in a database to give rauxinfos
    :param db_filename: Database filename
    :param table_name: name of table
    :return: None
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    def converter(rinchi):
        """Interfaces the rauxinfo converter in v02_convert.py"""
        rauxinfo = v02_convert.gen_rauxinfo(rinchi)
        return rauxinfo

    db.create_function("convert", 1, converter)
    cursor.execute("UPDATE {} SET rauxinfo = convert(rinchi) WHERE rauxinfo IS NULL or rauxinfo = '';".format(table_name))
    db.commit()
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database Tools - Duncan Hampshire 2016")
    parser.add_argument("database", help="Database File")
    parser.add_argument("tablename", help="Table Name")

    args = parser.parse_args()
    print(args.database, args.tablename)

    if True:
        print("Generating RAuxInfos")
        spinner = utils.Spinner()
        spinner.start()
        gen_rauxinfo(args.database, args.tablename)
        spinner.stop()
        print("Done")