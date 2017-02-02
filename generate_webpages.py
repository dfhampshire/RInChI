#!/usr/bin/env python3
"""
Generate PHP web-pages that contain RInChIs, RAuxInfos and Keys for both the version 0.02 and 0.03 rinchi versions.

Duncan Hampshire 2017
"""

import argparse
import fileinput
import os


# TODO finish this!!!

files = []
nfiles = []
for file in os.listdir("."):
    if file.startswith("rinchi"):
        files.append(file)
files = sorted(files)
for filename in files:
    nfiles.append('<p><a href="{}">{}</a></p>'.format(filename, filename))
links = "\n".join(nfiles)
filein = fileinput.FileInput("index.php", inplace=True)
for line in filein:
    nl = line.replace("#links", links)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generation of PHP webpage files - Duncan Hampshire 2017 \n{}".format(__doc__))
    parser.add_argument("destination", help="The destination folder for the webpage files")
    parser.add_argument("file-prefix", help="The prefix to name the files in the folder")
    parser.add_argument("template",
                        help="The template for the files to be created - must include header and footer sections")
    parser.add_argument("database-path", help="path to the SQL database of RInChI files")
    parser.add_argument('-ri', '--rinchi', action='store_true', help='Include RInChI')
    parser.add_argument('-ra', '--rauxinfo', action='store_true', help='Include RAuxInfo')
    parser.add_argument('-l', '--longkey', action='store_true', help='Include LongKey')
    parser.add_argument('-s', '--shortkey', action='store_true', help='Include ShortKey')
    parser.add_argument('-w', '--webkey', action='store_true', help='Include WebKey')
    parser.add_argument('-c', '--custom', help='Use a different HTML tag e.g. <p> , <h1>')
    parser.add_argument('-i', '--index', action='store_true', help='generate an index page')
    parser.add_argument('-v2n', '--version02names', help='list of names of columns for the version 0.02 table',
                        default='["rinchi","rauxinfo","longkey","shortkey"]')
    parser.add_argument('-v2t', '--version02table', help='name of the version 0.02 table', default='rinchis02')
    parser.add_argument('-v3n', '--version03names', help='list of names of columns for the version 0.03 table',
                        default='["rinchi","rauxinfo","longkey","shortkey","webkey"]')
    parser.add_argument('-v3t', '--version03table', help='name of the version 0.03 table', default='rinchis03')
    args = parser.parse_args()
