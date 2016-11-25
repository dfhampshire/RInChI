import sqlite3
import sys

from rinchi_tools import v02_convert


def gen_keys(db_filename, table_name):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    rows = cursor.execute(
        "SELECT rinchi,longkey FROM {} WHERE shortkey IS NULL or shortkey ='' LIMIT 1000;".format(table_name))
    while rows is not None:
        shortkeys = []
        for row in rows:
            shortkey = v02_convert.rinchi_2_shortkey(row[0])
            shortkeys.append((shortkey, row[1]))
        print("-")
        sys.stdout.flush()
        cursor.executemany("UPDATE {} SET shortkey = ? WHERE longkey = ?;".format(table_name),
                           shortkeys)
        db.commit()
        cursor.execute(
            "SELECT rinchi,rauxinfo,longkey,shortkey FROM {} WHERE shortkey IS NULL or shortkey ='' LIMIT 1000;".format(
                table_name))
        print(".")
        sys.stdout.flush()
    return


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
        rauxinfo = v02_convert.gen_rauxinfo(rinchi)
        return rauxinfo
    db.create_function("convert",1,converter)
    cursor.execute("UPDATE ? SET rauxinfo = convert(rinchi) WHERE rauxinfo IS NULL or rauxinfo = '';",table_name)
    return


gen_rauxinfo("rinchi.db", "rinchis02")
