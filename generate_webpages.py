#!/usr/bin/env python3
"""
Generates web-pages

Automates the generation of PHP web-pages that contain RInChIs, RAuxInfos and Keys for both the version 0.02 and 0.03
rinchi versions.

    Duncan Hampshire 2017
"""

import argparse
import os
import sqlite3

from rinchi_tools import RInChI, _external, database


def create_index_page(directory, end="", start=""):
    """
    Creates an index page for all file in a directory
    Args:
        end:
        start:
        directory:

    Returns:

    """
    files = []
    nfiles = []
    for file in os.listdir(directory):
        if file.endswith(end) and file.startswith(start):
            files.append(file)
    files = sorted(files)
    for filename in files:
        nfiles.append('<p><a href="{}{}{}">{}</a></p>'.format(directory, _external.SEPARATOR, filename, filename))
    links = "\n".join(nfiles)
    head = '<?php $title = "{}"; include "/var/www/template/header.php"; ?>'.format("Index")
    foot = '<?php include "/var/www/template/footer.php"; ?>'
    file = head + links + foot
    filename = "index.php"
    with open(filename, mode='w+') as f:
        f.write(file)


def get_rinchis_rauxinfos(db, table_name, number=1000):
    """
    Gets a list of rinchi - rauxinfo tuples
    """
    db = sqlite3.connect(db)
    cursor = db.cursor()
    results = database._sql_search(cursor, table_name, columns=("rinchi", "rauxinfo"), limit=number)
    return results


def tuple_to_html_page(data_tuple, inc_rinchi=True, inc_rauxinfo=True, inc_longkey=True, inc_shortkey=True, inc_webkey=True,
                       custom=None):
    """
    Create HTML page text from a data_tuple
    """
    if custom is None:
        tag = "p"
    else:
        tag = custom
    wrappings = ("<{}>".format(tag), "</{}>".format(tag))
    head = '<?php $title = "{}"; include "/var/www/template/header.php"; ?>'.format("RInChI Example")
    foot = '<?php include "/var/www/template/footer.php"; ?>'
    main_text = head
    web = RInChI().rinchikey_from_rinchi(data_tuple[0], "W").join(wrappings)
    if inc_rinchi:
        main_text += data_tuple[0].join(wrappings)
    if inc_rauxinfo:
        main_text += data_tuple[1].join(wrappings)
    if inc_longkey:
        main_text += RInChI().rinchikey_from_rinchi(data_tuple[0], "L").join(wrappings)
    if inc_shortkey:
        main_text += RInChI().rinchikey_from_rinchi(data_tuple[0], "S").join(wrappings)
    if inc_webkey:
        main_text += web
    main_text += foot
    return main_text


def run(db, table_name, destination, prefix, inc_rinchi=True, inc_rauxinfo=True, inc_longkey=True, inc_shortkey=True,
        inc_webkey=True, custom=None, number=1000):
    results = get_rinchis_rauxinfos(db, table_name, number)
    indexer = 1
    for result in results:
        page = tuple_to_html_page(result, inc_rinchi, inc_rauxinfo, inc_longkey, inc_shortkey, inc_webkey, custom)
        filename = "{}{}{}-{}.php".format(destination, _external.SEPARATOR, prefix, indexer)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, mode='w+') as f:
            f.write(page)
        indexer += 1
    create_index_page(destination, start=prefix)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generation of PHP webpage files - Duncan Hampshire 2017 \n{}".format(__doc__))
    parser.add_argument("destination", help="The destination folder for the webpage files")
    parser.add_argument("file_prefix", help="The prefix to name the files in the folder")
    parser.add_argument("-d", default=_external.RINCHI_DATABASE, help="path to the SQL database of RInChI files")
    parser.add_argument('-ri', '--rinchi', action='store_true', help='Include RInChI')
    parser.add_argument('-ra', '--rauxinfo', action='store_true', help='Include RAuxInfo')
    parser.add_argument('-l', '--longkey', action='store_true', help='Include LongKey')
    parser.add_argument('-s', '--shortkey', action='store_true', help='Include ShortKey')
    parser.add_argument('-w', '--webkey', action='store_true', help='Include WebKey')
    parser.add_argument('-c', '--custom', help='Use a different HTML tag e.g. <span> , <h1>')
    parser.add_argument('-n', '--number', default=1000, type=int, help='number of pages to be generated')
    parser.add_argument('-t', '--table', help='name of the table', default='rinchis03')

    print(_external.RINCHI_DATABASE)
    args = parser.parse_args()
    run(args.d, args.table, args.destination, args.file_prefix, args.rinchi, args.rauxinfo, args.longkey, args.shortkey,
        args.webkey, args.custom, args.number)
