"""
Databasing tools. Many are simply Python 3 restructured versions of Ben Hammond 2014. Other work by D. Hampshire 2017
"""
import csv
import logging
import os
import pickle
import queue
import sqlite3
import sys
import threading
import time
from heapq import nsmallest

from scipy.spatial import distance

from rinchi_tools import v02_convert, analysis
from rinchi_tools.reaction import Reaction
from rinchi_tools.rinchi_lib import RInChI as RInChI_Handle


###########
# CSV Tools
###########

def rdf_to_csv(rdf, outfile=None, return_rauxinfo=False, return_longkey=False, return_shortkey=False,
               return_webkey=False, return_rxninfo=False):
    """
    Convert an RD file to a CSV file containing RInChIs and other optional parameters
    Args:
        rdf: The RD file as a text block
        outfile: Optional output file name parameter
        return_rauxinfo: Include RAuxInfo in the result
        return_longkey: Include Long key in the result
        return_shortkey: Include the Short key in the result
        return_webkey: Include the Web key in the result
        return_rxninfo: Include RXN info in the result

    Returns: The name of the CSV file created with the requested fields
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

    data_dict = analysis.convert_rdf_to_dict(rdf, header)

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


def rdf_to_csv_append(rdf, csv_file):
    """
    Append an existing CSV file with values from an RD file

    Args:
        rdf: The RD file as a text block
        csv_file: the CSV file path
    """

    # Initialise a list that will contain all the RInChIs currently in the
    # csv_file
    old_rinchis = []

    # Open the existing csv_file and read the header defining which fields are
    # present
    with open(csv_file) as db:
        reader = csv.reader(db, delimiter="$")
        # Add all rinchis in the existing csv_file to a list
        header = reader.next()
        for row in reader:
            old_rinchis.append(row[0])

    # Construct a dictionary of RInChIs and RInChI data from the supplied rd
    # file
    new_data_dict = analysis.convert_rdf_to_dict(rdf, header)

    # Convert both lists of rinchis into sets - unique, does not preserve order
    old_rinchis = set(old_rinchis)
    new_rinchis = set(new_data_dict.keys())

    # The rinchis that need to be added to the csv_file are the complement of
    # the new rinchis in the old
    rinchis_to_add = list(new_rinchis - old_rinchis)

    # Add all new, unique rinchis to the csv_file
    with open(csv_file, "a") as db:
        writer = csv.writer(db, delimiter='$')
        writer.writerows([[i] + new_data_dict[i] for i in rinchis_to_add])


def create_csv_from_directory(root_dir, outname, return_rauxinfo=False, return_longkey=False, return_shortkey=False,
                              return_webkey=False, return_rxninfo=False):
    """
    Iterate recursively over all rdf files in the given folder and combine them into a single .csv database.

    Args:
        root_dir: The directory to search
        outname: Output file name parameter
        return_rauxinfo: Include RAuxInfo in the result
        return_longkey: Include Long key in the result
        return_shortkey: Include the Short key in the result
        return_webkey: Include the Web key in the result
        return_rxninfo: Include RXN info in the result

    Raises:
        IndexError: File failed to be recognised for importing
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


###########
# SQL tools
###########

# Regularly used command wrappers
#################################

def pragma_sql_env(cursor):
    """
    Sets various environmental variables and state flags within the SQLite environment.

    Args:
        cursor: The SQLite database cursor object
    """
    cursor.execute(''' PRAGMA main.page_size = 4096 ''')
    cursor.execute(''' PRAGMA main.cache_size=10000''')
    cursor.execute(''' PRAGMA main.locking_mode=EXCLUSIVE''')
    cursor.execute(''' PRAGMA main.synchronous=NORMAL''')
    cursor.execute(''' PRAGMA main.cache_size=5000''')


def create_sql_table(cursor,table_name,columns):
    """
    Create an SQL table

    Args:
        cursor: The SQLite database cursor object
        table_name: The name of the table to create
        columns: A list of column names to create
    """
    column_string = " TEXT, ".join(columns)
    cursor.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(table_name,column_string))


def get_sql_columns(cursor,table_name):
    """
    Get list of column names quickly

    Args:
        cursor: The SQLite database cursor object
        table_name: The name of the table

    Returns: A list of column names in order
    """
    cursor.execute('select * from {}'.format(table_name))
    names = [description[0] for description in cursor.description]
    return names


def sql_insert(cursor, table_name, data, columns=None, exec_many=False):
    """
    Insert data into a table quickly

    Args:
        cursor: The SQLite database cursor object
        table_name: The name of the table
        data: tha data to insert into the database.
        columns: A list of the columns in the table. If not found, an attempt is made to get these automatically.
        exec_many: Whether to use cursor.execute() or cursor.executemany()
    """
    if columns is None:
        get_sql_columns(cursor,table_name)

    command = ("INSERT INTO {}({}) VALUES (".format(table_name,", ".join(columns))
               + ", ".join(["?"] * len(columns) ) + ")")

    if exec_many:
        cursor.executemany(command,data)
    else:
        cursor.execute(command,data)

def checkTableExists(table_name, cursor):
    """
    Checks if a table exists within a database

    Args:
        table_name: The table name to check for
        cursor: The SQLite database cursor object

    Returns: True if present, False if Not.
    """
    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name= ?"
    if not cursor.execute(tb_exists, (table_name,)).fetchone():
        return False
    return True


def drop_table_if_needed(table_name, cursor):
    if checkTableExists(table_name, cursor):
        approved = input("Table {} will be deleted and recreated. Continue? (type 'yes') :".format(table_name))
        if approved == "yes":
            cursor.execute('drop table if exists {}'.format(table_name))
            logging.info("dropping table")
        else:
            logging.info("exiting operation")
            sys.exit("Operation Aborted")
    return


# Searching SQL databases
#########################

def sql_search(cursor,table_name, columns=None, lookup_value=None,field=None,use_like=False,limit=False):
    """
    Search for a value in an SQL database

    Args:
        cursor: The SQLite database cursor object
        table_name: The table to search
        lookup_value: The value to search for
        field: the field to search
        columns: list of columns to return
        use_like: use Like syntax
        limit: Limit the output to a certain number of results

    Returns: Cursor object which points to the result

    """
    if columns is None:
        columns = ["*"]

    # Set comparison method
    if use_like:
        comparator = "LIKE"
    else:
        comparator = "="

    # impose limit if required
    if limit:
        limiter = " LIMIT {}".format(limit)
    else:
        limiter = ""

    # formulate the query
    part1 = 'SELECT {} FROM {}'.format(' ,'.join(columns),table_name)
    part2 = ' WHERE {} {} ?'.format(field,comparator)
    if lookup_value is None:
        command = part1 + limiter
    else:
        command = part1 + part2 + limiter

    cursor.execute(command, (lookup_value,))
    return cursor


def sql_key_to_rinchi(key, db_filename, table_name, keytype ="L"):
    """
    Returns the RInChI matching the given Long RInChI key for a given database

    Args:
        key: The key to search for
        db_filename: The database in which to search
        table_name: The table in which to search for the key
        keytype: The key type to seach for. Defaults to the long key

    Raises:
        ValueError: The keytype argument must be one of "L" , "S" or "W"

    Returns: the corresponding RInChI
    """

    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    if keytype == "L":
        field = "key"
    elif keytype == "S":
        field = "shortkey"
    elif keytype == "W":
        field = "webkey"
    else:
        raise ValueError('The keytype argument must be one of "L" , "S" or "W"')
    cursor = sql_search(cursor, table_name,["rinchi"], key, field,)
    rinchi = cursor.fetchone()[0]
    db.close()
    return rinchi


def search_for_inchi(inchi, db_filename, table_name):
    """
    Searches for an inchi within a rinchi database.
    Approx. 20x faster than the version in rinchi_tools.analyse

    Args:
        inchi: The InChI to search for
        db_filename: the database to search within
        table_name: the database to search in
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    query = "%" + "/".join(inchi.split("/")[1:]) + "%"
    cursor = sql_search(cursor,table_name,["rinchi"],inchi,"rinchi",True)
    for r in cursor:
        print((r[0]))

    return [i[0] for i in cursor.fetchall()]


def advanced_search(inchi, db_filename, table_name, hyb=None, val=None, rings=None, formula=None):
    """
    Search for an Inchi within a RInChi database with advanced options. Output is to stdout.

    Args:
        inchi: The InChI to search for
        db_filename: the database to search within
        table_name: the datable to search in

        All args following are dictionaries of the format {property:count,property2:count2,...}
        hyb: The hybridisation changes(s) desired
        val: The valence change(s) desired
        rings: The ring change(s) desired
        formula: The formula change(s) desired
    """
    if hyb is None:
        hyb = {}
    if val is None:
        val = {}
    if rings is None:
        rings = {}
    if formula is None:
        formula = {}
    rinchis = search_for_inchi(inchi, db_filename, table_name)
    print((len(rinchis), "inchi matches found"))

    counter = 0
    for rin in rinchis:
        r = Reaction(rin)
        if r.detect_reaction(hyb_i=hyb, val_i=val, rings_i=rings, formula_i=formula):
            counter += 1
            print(r.rinchi)

    print(counter, "exact matches found")


# Converting to SQL databases
#############################

def rdf_to_sql(rdfile, db_filename, table_name, columns = None):
    """
    Creates or adds to an SQLite database the contents of a given RDFile.

    Args:
        rdfile: The RD file to add to the database
        db_filename: The file name of the SQLite database
        table_name: The name of the table to create or append
        columns: The columns to add. If None, the default is [rinchi,rauxinfo,longkey,shortkey,webkey]
    """
    if columns is None:
        columns = ["rinchi","rauxinfo","longkey","shortkey","webkey"]

    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    create_sql_table(cursor,table_name,columns)

    # Repopulate columns variable. Useful for pre-exisiting table
    columns = get_sql_columns(cursor,table_name)

    pragma_sql_env(cursor)

    # Open the rdfile and convert its contents to a dict of rinchis and rinchi
    # data
    rdf_data = analysis.convert_rdf_to_dict(rdfile, columns)

    # Transform in place the dicts storing rxn info to their string
    # representations
    for i in rdf_data.keys():
        rdf_data[i][1] = repr(rdf_data[i][1])

    rdf_data_tuple = [tuple([i] + rdf_data[i]) for i in rdf_data.keys()]

    # Add the rdf data to the dictionary
    sql_insert(cursor,table_name,rdf_data_tuple,columns,True)
    db.commit()
    db.close()


def csv_to_sql(csv_name, db_filename, table_name):
    """
    Creates or appends an SQL database with values from a CSV file

    Args:
        csv_name: The CSV filename
        db_filename: The SQLite3 database
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    pragma_sql_env(cursor)

    with open(csv_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter="$")
        columns = reader.next()
        create_sql_table(cursor, table_name, columns)
        for row in reader:
            sql_insert(cursor,table_name,row)

    db.commit()
    db.close()


def convert_v02_v03(db_filename, table_name, v02_rinchi=False, v02_rauxinfo=False, v03_rinchi=False,
                    v03_rauxinfo=False, v03_longkey=False, v03_shortkey=False, v03_webkey=False):
    """
    Converts a database of v02 rinchis into a database of v03 rinchis and associated information. N.B keys for v02 are
    not required as new keys must be generated for the database. Because of the nature of this problem, this is achieved
    by creating a new database for the processed data and then transferring back to the original

    Args:
         db_filename: The database filename to which the changes should be made. The new database is added as a new table
         table_name: the name for the new v03 rinchi table.
         v02_rinchi: The name of the v02 rinchi column. Defaults to False (No rinchi in database).
         v02_rauxinfo: The name of the v02 rauxinfo column. Defaults to False (No rauxinfos in database).
         v03_rinchi: The name of the v03 new rinchi column. Defaults to False (No rinchi column will be created).
         v03_rauxinfo: The name of the v03 new rinchi column. Defaults to False (No rauxinfo column will be created).
         v03_longkey: The name of the v03 new rinchi column. Defaults to False (No longkey column will be created).
         v03_shortkey: The name of the v03 new rinchi column. Defaults to False (No shortkey column will be created).
         v03_webkey: The name of the v03 new webkey column. Defaults to False (No webkey column will be created).

    """

    # Create database connections including for a temporary database
    os.remove("conv0203.log")
    logging.basicConfig(filename='conv0203.log', level=logging.DEBUG)
    logging.info("\n========\nStarting Conversion Process\n========")
    starttime = time.time()
    # Construct SQL strings
    col_list = [v03_rinchi, v03_rauxinfo, v03_longkey, v03_shortkey, v03_webkey]
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

    # Define base commands
    select_command = "SELECT {}, {} FROM rinchis02".format(v02_rinchi, v02_rauxinfo)
    create_command = "CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, cols_to_create)
    insert_command = "INSERT INTO {} VALUES (".format(table_name) + ", ".join(["?"] * colcount) + ")"

    logging.info("Check for original table")  # Doing this now to prevent delays later
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    drop_table_if_needed(table_name, cursor)
    db.close()

    q = queue.Queue(1000)
    popul8 = threading.Thread(target=populate_queue, args=(
    q, db_filename, select_command, v03_rinchi, v03_rauxinfo, v03_longkey, v03_shortkey, v03_webkey))
    depopul8 = threading.Thread(target=depopulate_queue, args=(q, create_command, insert_command))
    depopul8.start()
    popul8.start()
    depopul8.join()
    popul8.join()
    logging.info("transfering temporary database...")
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute("ATTACH DATABASE ? AS db2", ("rinchi_temp.db",))
    cursor.execute("SELECT sql FROM db2.sqlite_master WHERE type='table' AND name=?", (table_name,))
    newsql = cursor.fetchone()[0]
    cursor.execute(newsql)
    cursor.execute("INSERT INTO {0} SELECT * FROM db2.{0}".format(table_name))
    db.commit()
    db.close()
    os.remove("rinchi_temp.db")
    logging.info("Finished conversion in {} seconds".format(time.time() - starttime))
    return

    ##########################################################
    # Fingerprinting
    ##########################################################


def compare_fingerprints(search_term, db_filename, table_name):
    """
    Search database for top 10 closest matches to a RInChI by fingerprinting method. Sent to stdout.

    Args:
        search_term: A RInChi or Long-RInChIKey to search with
        db_filename: the database containing the fingerprints
        table_name: The table containing the RInChI fingerprints

    """
    db_size = 830000
    counter = 1

    if search_term.startswith("Long-RInChIKey"):
        fp1 = recall_fingerprints(search_term, db_filename, table_name)
    elif search_term.startswith("RInChI"):
        r = Reaction(search_term)
        r.calculate_reaction_fingerprint()
        fp1 = r.reaction_fingerprint.toarray()
    else:
        print("Invalid input")
        return

    db = sqlite3.connect(db_filename)

    res = []
    cursor = db.cursor()
    cursor = sql_search(cursor,table_name,["longkey","fingerprint"],limit=-1)
    for r in cursor:
        counter += 1
        res.append((r[0], distance.euclidean(fp1, pickle.loads(str(r[1])).toarray()[0])))
        if counter % 10000 == 0:
            per = int(float(100 * counter) / db_size)
            sys.stdout.write("\r {0}% complete".format(per))
            sys.stdout.flush()

    out = nsmallest(10, res, key=lambda s: s[1])
    print("\n", out)


def recall_fingerprints(lkey, db_filename,table_name):
    """
    returns a reaction fingerprint as stored in the reaction database
    Args:
        lkey: The long key to search for
        db_filename: The database filename
        table_name: The table name which stores the fingerprints

    Returns: A numpy array the reaction fingerprint as stored in the reaction database

    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor = sql_search(cursor,table_name,["fingerprint"],lkey,"longkey",)

    # Unpickle the binary data, and return a Numpy array containing the
    # reaction fingerprint
    fpt = pickle.loads(str(cursor.fetchone()[0])).toarray()[0]
    db.close()

    return fpt


def update_fingerprints(db_filename, table_name, fingerprint_table_name):
    """
    NOT CURRENTLY WORKING. NEEDS UPDATING TO USE MULTITHREADING FOR USABLE PERFORMANCE

    Calculates the reaction fingerprint as defined in the reaction Reaction class, and stores
    it in the given database in a compressed form

    Args:
        db_filename: the database filename to update
        table_name: The table containing the RInChIs
        fingerprint_table_name: The table to contain the fingerprint
    """
    db = sqlite3.connect(db_filename)

    # Poor method. A database cannot have two cursors pointing at it.
    cursor = db.cursor()
    cursor2 = db.cursor()

    cursor = sql_search(cursor,table_name,[])

    counter = 0
    for lkey in cursor:

        try:
            # cursor.execute('''SELECT rinchi FROM rinchis WHERE longkey LIKE ?''', (lkey,))
            # rinchi = cursor.fetchone()[0]
            r = Reaction(lkey[0])
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

# Updating scripts using threading for performance
#################################################


def populate_queue(main_q, db_filename, s_command, v03_rinchi, v03_rauxinfo, v03_longkey, v03_shortkey, v03_webkey):
    """
    Populates a queue of version 0.03 rinchis with processes version 0.02 rinchis
    
    TODO modularise

    Args:
        main_q: A queue object 
        db_filename: the database to executethe command on
        s_command: the select command to get the data
        v03_rinchi: include the rinchi
        v03_rauxinfo: include the rauxinfo
        v03_longkey: include the longkey
        v03_shortkey: include the shortkey
        v03_webkey: include the webkey
    """

    db = sqlite3.connect(db_filename)
    cursornew = db.cursor()
    logging.info("populating")
    for row in cursornew.execute(s_command):
        the_rinchi = v02_convert.convert_rinchi(row[0])
        data_to_add = []
        if v03_rinchi:
            data_to_add.append(the_rinchi)
        if v03_rauxinfo:
            data_to_add.append(v02_convert.convert_rauxinfo(row[1]))
        if v03_longkey:
            data_to_add.append(RInChI_Handle.rinchikey_from_rinchi(the_rinchi, "L"))
        if v03_shortkey:
            data_to_add.append(RInChI_Handle.rinchikey_from_rinchi(the_rinchi, "S"))
        if v03_webkey:
            data_to_add.append(RInChI_Handle.rinchikey_from_rinchi(the_rinchi, "W"))
        main_q.put(data_to_add)
        while main_q.full():
            time.sleep(0.01)
    logging.info("finished_populating")
    db.close()


def depopulate_queue(q, create_command, i_command):
    """
    Removes items from the queue and processess them
    Args:
        q: The queue to depopulate
        create_command: the create command to make a temporary database
        i_command: the insert command for the temporary database
    """
    db = sqlite3.connect("rinchi_temp.db")
    cursor = db.cursor()
    cursor.execute(create_command)
    logging.info("depopulating")
    while True:
        try:
            cursor.execute(i_command, q.get(True, 2))
            # Waits for 2 seconds, otherwise throws `Queue.Empty`
        except queue.Empty:
            logging.info("Finished depopulating")
            break
    db.commit()
    db.close()