"""
Performs SQLite3 operations on a database
"""

import sqlite3

from rinchi_tools import v02_convert


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
    cursor.execute("UPDATE ? SET rauxinfo = convert(rinchi) WHERE rauxinfo IS NULL or rauxinfo = '';", table_name)
    return
