#!/usr/bin/env python3

# NEW PYTHON SCRIPTS
# TESTING PHASE

# RInChI Project
# BENJAMIN HAMMOND 2014


import argparse
import csv
import os
import pickle
import sqlite3
import sys
import threading
import time
from ast import literal_eval
from heapq import nsmallest

from scipy.spatial import distance

from rinchi_tools import conversion, rinchi_lib, rinchi, v02_convert

# Define a handle for the RInChI class within the C++ library
rinchi_handle = rinchi_lib.RInChI()


#######################################
# GENERATION AND CONVERSION OF DATABASES
#######################################


def convert_rdf_to_dict(rdf, header, force_equilibrium=False):
    """ Helper function accepts an RDFile and a list of parameters and returns a dict containing
    converted rinchis, keys, and reaction information
    """
    with open(rdf) as data:
        input_data = data.read()

    # Set optional conversion parameters
    start_index = 0
    stop = 0

    # Set which columns to include
    return_rauxinfo = "RAuxInfo" in header
    return_longkey = "LongKey" in header
    return_shortkey = "ShortKey" in header
    return_webkey = "WebKey" in header
    return_rxninfo = "RXNInfo" in header

    # Run RInChI conversion functions.
    rinchidata = conversion.rdf_2_rinchis(input_data, start_index, stop, force_equilibrium, return_rauxinfo,
                                          return_longkey, return_shortkey, return_webkey, return_rxninfo)

    # Transpose nested list into a list of data entries
    data_transpose = map(list, zip(*rinchidata))

    # Force uniqueness
    return {x[0]: x[1:] for x in data_transpose}


def rdf_to_csv(rdf, outfile=None, return_rauxinfo=False, return_longkey=False, return_shortkey=False,
               return_webkey=False, return_rxninfo=False):
    """ Takes an .rdf file as input and returns a .csv file containing RInChIs and other optional
        parameters
    """

    # Check that input was supplied
    if not rdf:
        return None

    # Extract filename only
    input_name = rdf.split(".")[-2]
    input_name = input_name.split("/")[-1]

    header = ["RInChI"]
    if return_rauxinfo:
        header.append("RAuxInfo")
    if return_longkey:
        header.append("LongKey")
    if return_shortkey:
        header.append("ShortKey")
    if return_webkey:
        header.append("WebKey")
    if return_rxninfo:
        header.append("RXNInfo")

    data_dict = convert_rdf_to_dict(rdf, header)

    # Prevent overwriting, create output in an output folder in the current
    # directory
    if not os.path.exists('output'):
        os.mkdir('output')

    # Set name of new file
    if outfile:
        new_name = os.path.join("output", outfile)
    else:
        new_name = os.path.join("output", input_name)

    # Add a number suffix if chosen filename already exists
    if os.path.exists('%s-rinchi.csv' % new_name):
        index = 1
        while os.path.exists('%s_%d-rinchi.csv' % (new_name, index)):
            index += 1
        output_name = '%s_%d-rinchi.csv' % (new_name, index)
    else:
        output_name = '%s-rinchi.csv' % new_name

    # Write new database file as .csv
    with open(output_name, 'w') as f:
        writer = csv.writer(f, delimiter='$')
        writer.writerow(header)
        writer.writerows([[i] + data_dict[i] for i in data_dict.keys()])
    return output_name


def rdf_to_csv_append(rdf, database):
    """ Takes an .rdf file and an existing .csv database and appends uniquely the reactions in the rdf file to the database
    """

    # Initialise a list that will contain all the RInChIs currently in the
    # database
    old_rinchis = []

    # Open the existing database and read the header defining which fields are
    # present
    with open(database) as db:
        reader = csv.reader(db, delimiter="$")
        # Add all rinchis in the existing database to a list
        header = reader.next()
        for row in reader:
            old_rinchis.append(row[0])

    # Construct a dictionary of RInChIs and RInChI data from the supplied rd
    # file
    new_data_dict = convert_rdf_to_dict(rdf, header)

    # Convert both lists of rinchis into sets - unique, does not preserve order
    old_rinchis = set(old_rinchis)
    new_rinchis = set(new_data_dict.keys())

    # The rinchis that need to be added to the database are the complement of
    # the new rinchis in the old
    rinchis_to_add = list(new_rinchis - old_rinchis)

    # Add all new, unique rinchis to the database
    with open(database, "a") as db:
        writer = csv.writer(db, delimiter='$')
        writer.writerows([[i] + new_data_dict[i] for i in rinchis_to_add])


def create_csv_from_directory(root_dir, outname, return_rauxinfo=False, return_longkey=False, return_shortkey=False,
                              return_webkey=False, return_rxninfo=False):
    """ Given a root directory, an output filename, and a list of parameters, iterates recursively over
    all rdf files in the given folder and combines them into a single .csv database.
    """

    # Flag for whether the database should be created or appended
    database_has_started = False

    # Iterate over all files in the roo directory
    for root, folders, files in os.walk(root_dir):
        for file in files:
            filename = os.path.join(root, file)
            try:
                # Only try to process files with an .rdf extension
                if file.split(".")[-1] == "rdf":
                    if database_has_started:
                        rdf_to_csv_append(filename, db_name)
                    else:
                        db_name = rdf_to_csv(filename, outname, return_rauxinfo, return_longkey, return_shortkey,
                                             return_webkey, return_rxninfo)
                        database_has_started = True
            except IndexError:
                # Send the names of any files that failed to be recognised to
                # STDOUT
                print(("Failed to recognise {}".format(filename)))


def rdf_to_sql(rdfile, db_filename):
    """ Creates or adds to an SQLite database the contents of a given RDFile.
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS
    rinchis(
        rinchi TEXT,
        longkey TEXT UNIQUE ON CONFLICT REPLACE,
        rxninfo TEXT)
    ''')

    cursor.execute(''' PRAGMA main.page_size = 4096 ''')
    cursor.execute(''' PRAGMA main.cache_size=10000''')
    cursor.execute(''' PRAGMA main.locking_mode=EXCLUSIVE''')
    cursor.execute(''' PRAGMA main.synchronous=NORMAL''')
    cursor.execute(''' PRAGMA main.cache_size=5000''')

    # Open the rdfile and convert its contents to a dict of rinchis and rinchi
    # data
    rdf_data = convert_rdf_to_dict(rdfile, ["RInChI", "LongKey", "RXNInfo"])

    # Transform in place the dicts storing rxn info to their string
    # representations
    for i in rdf_data.keys():
        rdf_data[i][1] = repr(rdf_data[i][1])

    rdf_data_tuple = [tuple([i] + rdf_data[i]) for i in rdf_data.keys()]

    # Add the rdf data to the dictionary
    cursor.executemany(''' INSERT INTO rinchis(rinchi, longkey, rxninfo) VALUES(?,?,?) ''', rdf_data_tuple)

    db.commit()


def sql_to_csv(db_filename, csv_name):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    with open(csv_name, 'rb') as csvfile:
        pass


def csv_to_sql(csv_name, db_filename):
    """ Opens a given dabase, or creates one if none exists, and appends the contents of a .csv file to the end,
    as generated above.
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS
    rinchis(
        rinchi TEXT,
        longkey TEXT UNIQUE ON CONFLICT REPLACE,
        rxninfo TEXT)
    ''')

    # May break on windows machines
    cursor.execute(''' PRAGMA main.page_size = 4096 ''')
    cursor.execute(''' PRAGMA main.cache_size=10000''')
    cursor.execute(''' PRAGMA main.locking_mode=EXCLUSIVE''')
    cursor.execute(''' PRAGMA main.synchronous=NORMAL''')
    cursor.execute(''' PRAGMA main.journal_mode=WAL''')
    cursor.execute(''' PRAGMA main.cache_size=5000''')
    ###

    with open(csv_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter="$")
        reader.next()
        for row in reader:
            cursor.execute(''' INSERT INTO     rinchis(rinchi, longkey, rxninfo) VALUES(?,?,?) ''', row)
    db.commit()
    db.close()


#####################################
# SEARCHING OF DATABASES
#####################################


def sql_key_to_rxninfo(longkey, db_filename):
    """ Returns the $DATA/$DATUM field for the entry with the given long rinchi key
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    cursor.execute('''SELECT rxninfo FROM rinchis WHERE longkey=?''', (longkey,))

    try:
        entry = cursor.fetchone()
        return literal_eval(entry[0])
    except (KeyError, TypeError):
        print("Data not found")
        return None
    finally:
        db.close()


def sql_key_to_rinchi(longkey, db_filename):
    """ Returns the RInChI matching the given Long RInChI key for a given database
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    cursor.execute('''SELECT rinchi FROM rinchis WHERE longkey=?''', (longkey,))
    rinchi = cursor.fetchone()[0]
    db.close()
    return rinchi


def search_for_inchi(inchi, db_filename):
    """ Searches for an inchi within a rinchi database.
    Approx. 20x faster than the version in rinchi_tools.analyse
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    query = "%" + "/".join(inchi.split("/")[1:]) + "%"
    cursor.execute('''SELECT rinchi FROM rinchis WHERE rinchi LIKE ?''', (query,))
    for r in cursor:
        print((r[0]))

    db.close()
    return [i[0] for i in cursor.fetchall()]


def ring_bitstring():
    pass


def advanced_search(db_filename, inchis=None, hyb=None, val=None, rings=None, formula=None):
    if hyb is None:
        hyb = {}
    if val is None:
        val = {}
    if rings is None:
        rings = {}
    if formula is None:
        formula = {}
    rinchis = search_for_inchi(inchis, db_filename)
    print((len(rinchis), "inchi matches found"))

    counter = 0
    for rin in rinchis:
        r = rinchi.Reaction(rin)
        if r.detect_reaction(hyb_i=hyb, val_i=val, rings_i=rings, formula_i=formula):
            counter += 1
            print(r.rinchi)

    print(counter, "exact matches found")

    ##########################################################
    # Fingerprinting
    ##########################################################


def update_fingerprints(db_filename):
    """ Currently testing only.
        Calculates the reaction fingerprint as defined in rinchi_rings, and stores it in the given database in a compressed form """
    db = sqlite3.connect(db_filename)

    cursor = db.cursor()
    cursor2 = db.cursor()

    cursor.execute('''SELECT rinchi, longkey FROM rinchis''')

    counter = 0
    for lkey in cursor:

        try:
            # cursor.execute('''SELECT rinchi FROM rinchis WHERE longkey LIKE ?''', (lkey,))
            # rinchi = cursor.fetchone()[0]
            r = rinchi.Reaction(lkey[0])
            r.calculate_reaction_fingerprint()

            # Pickle the reaction fingerprint - store it as binary data within
            # an SQL BLOB field
            fingerprint = pickle.dumps(r.reaction_fingerprint)
            # cursor.execute('''UPDATE fingerprints SET fingerprint = ? WHERE longkey = ? ''', (fingerprint, lkey[1]))
            cursor2.execute('''INSERT INTO fpts (longkey, fingerprint) VALUES (?, ?) ''', (lkey[1], fingerprint))
            counter += 1
            print(counter)
            db.commit()

        except sqlite3.IntegrityError:
            counter += 1
            print(counter, "ERR", "\n")
    db.commit()
    db.close()


def recall_fingerprints(lkey, db_filename):
    """ Given a long RInChI key, returns as a numpy array the reaction fingerprint as stored in the reaction database """
    db = sqlite3.connect(db_filename)

    cursor = db.cursor()
    cursor.execute('''SELECT fingerprint FROM fpts WHERE longkey = ?''', (lkey,))

    # Unpickle the binary data, and return a Numpy array containing the
    # reaction fingerprint
    fpt = pickle.loads(str(cursor.fetchone()[0])).toarray()[0]
    db.close()

    return fpt


def compare_fingerprints(lk1, db_filename):
    db_size = 830000
    counter = 1

    if lk1.startswith("Long-RInChIKey"):
        fp1 = recall_fingerprints(lk1, db_filename)
    elif lk1.startswith("RInChI"):
        r = rinchi.Reaction(lk1)
        r.calculate_reaction_fingerprint()
        fp1 = r.reaction_fingerprint.toarray()
    else:
        print("Invalid input")
        return

    db = sqlite3.connect(db_filename)

    res = []
    cursor = db.cursor()
    cursor.execute('''SELECT longkey, fingerprint FROM fpts LIMIT -1''')
    for r in cursor:
        counter += 1
        res.append((r[0], distance.euclidean(fp1, pickle.loads(str(r[1])).toarray()[0])))
        if counter % 10000 == 0:
            per = int(float(100 * counter) / db_size)
            sys.stdout.write("\r {0}% complete".format(per))
            sys.stdout.flush()

    out = nsmallest(10, res, key=lambda s: s[1])
    print("\n", out)


def convert_v02_v03(db_filename, table_name, v02_rinchi=False, v02_rauxinfo=False, v03_rinchi=False, v03_rauxinfo = False,
                    v03_longkey = False, v03_shortkey = False, v03_webkey=False):
    """
    Converts a database of v02 rinchis into a database of v03 rinchis and associated information. N.B keys for v02 are
    not required as new keys must be generated for the database. Because of the nature of this problem, this is achieved
    by creating a new database for the processed data and then transferring back to the original

    Parameters:
    :param db_filename: The database filename to which the changes should be made. The new database is added as a new table
    :param table_name: the name for the new v03 rinchi table.
    :param v02_rinchi: The name of the v02 rinchi column. Defaults to False (No rinchi in database).
    :param v02_rauxinfo: The name of the v02 rauxinfo column. Defaults to False (No rauxinfos in database).
    :param v03_rinchi: The name of the v03 new rinchi column. Defaults to False (No rinchi column will be created).
    :param v03_rauxinfo: The name of the v03 new rinchi column. Defaults to False (No rauxinfo column will be created).
    :param v03_longkey: The name of the v03 new rinchi column. Defaults to False (No longkey column will be created).
    :param v03_shortkey: The name of the v03 new rinchi column. Defaults to False (No shortkey column will be created).
    :param v03_webkey: The name of the v03 new webkey column. Defaults to False (No webkey column will be created).

    """

    # Create database connections including for a temperary database
    db = sqlite3.connect(db_filename)
    db_temp = sqlite3.connect("rinchi_temp.db")
    cursor = db.cursor()
    temp_cursor = db_temp.cursor()

    def checkTableExists(tablename,dbcur):
        tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name= ?"
        if not dbcur.execute(tb_exists,(tablename,)).fetchone():
            return False
        return True

    if checkTableExists(table_name,cursor):
        approved = input("Table {} will be deleted and recreated. Continue? (type YES) :".format(table_name))
        if approved == "YES":
            cursor.execute('drop table if exists {}'.format(table_name))
        else:
            print("Operation Aborted")
            return

    # Construct SQL strings
    col_list = [v03_rinchi,v03_rauxinfo,v03_longkey,v03_shortkey,v03_webkey]
    cols_to_create = []
    cols_to_insert = []
    colcount = 0
    for column in col_list:
        if column:
            cols_to_create.append(column + " text")
            colcount += 1
    cols_to_create = ", ".join(cols_to_create)

    if colcount == 0:
        raise ValueError("Cannot create empty table")

    #Define base commands
    select_command = "SELECT ?, ? FROM rinchis02 LIMIT 5"
    create_command = "CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, cols_to_create)
    insert_command = "INSERT INTO {} VALUES (" + ", ".join(["?"]*colcount) + ")"

    print(insert_command,create_command,select_command)

    data_list = []
    finished_populating = False

    def populate_list():
        global finished_populating
        data = cursor.execute(select_command, (v02_rinchi, v02_rauxinfo))
        for row in data:
            the_rinchi = v02_convert.convert_rinchi(row[0])
            data_to_add = []
            if v03_rinchi:
                data_to_add.append(the_rinchi)
            if v03_rauxinfo:
                data_to_add.append(v02_convert.convert_rauxinfo(row[1]))
            if v03_longkey:
                data_to_add.append(rinchi_handle.rinchikey_from_rinchi(the_rinchi, "L"))
            if v03_shortkey:
                data_to_add.append(rinchi_handle.rinchikey_from_rinchi(the_rinchi, "S"))
            if v03_webkey:
                data_to_add.append(rinchi_handle.rinchikey_from_rinchi(the_rinchi, "W"))
            data_list.append(tuple(data_to_add))
            while len(data_list) > 1000:
                time.sleep(0.01)
        finished_populating = True


    def depopulate_list():
        global finished_populating
        temp_cursor.execute(create_command)
        while finished_populating:
            if data_list:
                temp_cursor.execute(insert_command,data_list.pop())
                db_temp.commit()
            else:
                time.sleep(0.01)

    popul8 = threading.Thread(target=populate_list)
    depopul8 = threading.Thread(target=depopulate_list)

    depopul8.start()
    popul8.start()
    depopul8.join()
    popul8.join()

    db_temp.close()
    cursor.execute("ATTACH DATABASE ? AS db2", ("rinchi_temp.db",))
    cursor.execute("SELECT sql FROM db2.sqlite_master WHERE type='table' AND name=?",(table_name,))
    cursor.execute(cursor.fetchone()[0])  # Contains: CREATE TABLE current (framenum INTEGER, nextKanji INTEGER)
    cursor.execute("INSERT INTO rinchi.{0} SELECT * FROM db2.{0}".format(table_name))

    db.commit()
    db.close()






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A collection of RInChI Tools - Benjamin Hammond 2014")
    parser.add_argument("input",
                        help="Input - the RDFile or directory to be processed, or the search parameter for a search, or new table to be created")
    parser.add_argument("database", nargs="?",
                        help="The existing database to be modified or searched, or the name of new database to be created")
    parser.add_argument("arg3", nargs="?", help="optional arg 3")

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
    action.add_argument('--lkey2rxninfo', action='store_true', help='Returns the RXNInfo for a given Long Key')
    action.add_argument('--inchisearch', action='store_true',
                        help='Returns all RInChIs containing the given InChI to STDOUT')
    action.add_argument('--TEST', action='store_true', help='Returns all RInChIs containing the given InChI to STDOUT')

    action.add_argument('--ufingerprints', action='store_true',
                        help='Adds new entries to the fpts table containing fingerprint data')
    action.add_argument('--rfingerprints', action='store_true', help='Returns the fingerprint of a given key')
    action.add_argument('--cfingerprints', action='store_true',
                        help='Returns all RInChIs containing the given InChI to STDOUT')
    action.add_argument('--conv0203',action='store_true',
                        help='Creates a new table of v.03 rinchis from a table of v.02 rinchis')

    args = parser.parse_args()

    if args.lkey2rxninfo and args.input.startswith("RInChI"):
        try:
            args.input = rinchi_handle.rinchikey_from_rinchi(args.input, "L")
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
        rdf_to_sql(args.input, args.database)
    if args.csv2sql:
        csv_to_sql(args.input, args.database)

    if args.ufingerprints:
        update_fingerprints(args.input)
    if args.rfingerprints:
        print(list(recall_fingerprints(args.input, args.database)))
    if args.cfingerprints:
        compare_fingerprints(args.input, args.database)

    if args.TEST:
        tinchis = ["InChI=1S/C3H5Cl/c1-2-3-4/h2H,1,3H2", "InChI=1S/C3H5Br/c1-2-3-4/h2H,1,3H2",
                   "InChI=1S/C3H5I/c1-2-3-4/h2H,1,3H2", "InChI=1S/C3H6O/c1-2-3-4/h2,4H,1,3H2",
                   "InChI=1S/C3H5F/c1-2-3-4/h2H,1,3H2", "InChI=1S/C3H6/c1-3-2/h3H,1H2,2H3"]
        for inchi in tinchis:
            print(inchi, len(search_for_inchi(inchi, args.database)))

    if args.lkey2rinchi:
        print(sql_key_to_rinchi(args.input, args.database))
    if args.lkey2rxninfo:
        print(sql_key_to_rxninfo(args.input, args.database))
    if args.inchisearch:
        print("start")
        search_for_inchi(args.input, args.database)
    if args.conv0203:
        # Names hardcoded because significant modification of the arparse system would be needed and would be complex
        v02_column_names = ["rinchi","rauxinfo"]
        v03_column_names = ["rinchi","rauxinfo","longkey","shortkey","webkey"]
        column_names = v02_column_names + v03_column_names
        convert_v02_v03(args.database, args.input,*column_names)
