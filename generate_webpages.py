#!/usr/bin/env python3
"""
Generate PHP web-pages that contain RInChIs, RAuxInfos and Keys for both the version 0.02 and 0.03 rinchi versions.

Duncan Hampshire 2017
"""

import argparse
import fileinput
import os

files = []
nfiles = []
for file in os.listdir("."):
    if file.startswith("rinchi"):
        files.append(file)
files = sorted(files)
for filename in files:
     nfiles.append('<p><a href="{}">{}</a></p>'.format(filename,filename))
links = "\n".join(nfiles)
filein =  fileinput.FileInput("index.php", inplace=True)
for line in filein:
    nl = line.replace("#links", links)
    print nl,

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database Tools - Duncan Hampshire 2016 \n{}".format(__doc__))
    parser.add_argument("database", help="Database File")
    parser.add_argument("tablename", help="Table Name")