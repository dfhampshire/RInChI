# !/usr/bin/env python3
"""
Script used to test various the module during development. Not for general distribution. Successful code is implemented
elsewhere.

Duncan Hampshire 2017
"""

import collections
import logging
import sqlite3

from rinchi_tools import v02_convert
from rinchi_tools.rinchi_lib import RInChI as RInChI_Handle


def test1():
    select_command = "SELECT rowid, {}, {} FROM rinchis02".format("rinchi", "rauxinfo")
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    def populate_list(db_filename, s_command):
        db = sqlite3.connect(db_filename)
        cursornew = db.cursor()
        logging.info("populating")
        for row in cursornew.execute(s_command):
            data_to_add = []
            try:
                the_rinchi = v02_convert.convert_rinchi(row[1])
                data_to_add.append(the_rinchi)
                data_to_add.append(v02_convert.convert_rauxinfo(row[2]))
                data_to_add.append(RInChI_Handle().rinchikey_from_rinchi(the_rinchi, "L"))
                data_to_add.append(RInChI_Handle().rinchikey_from_rinchi(the_rinchi, "S"))
                data_to_add.append(RInChI_Handle().rinchikey_from_rinchi(the_rinchi, "W"))
            except:
                logging.info(row[1])
                logging.info(row[2])
                logging.info(data_to_add)
        db.close()

    populate_list("rinchi.db", select_command)


def test2():
    class Item:
        def __init__(self, name):
            self.name = name

        def get_name(self):
            return self.name

    def do_method(instance, method):
        return method(instance)

    cow = Item("Mr Cow")
    print(do_method(cow, Item.get_name))


def test3():
    print(collections.Counter())


def test4():
    import sqlite3
    connection = sqlite3.connect('../rinchi.db')
    cursor = connection.cursor()
    cursor.execute('select * from rinchis02')
    names = [description[0] for description in cursor.description]
    print(names)
