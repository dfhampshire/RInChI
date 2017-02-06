"""
RInChI Database Module

Provides tools for converting, creating, and removing from SQL databases

    Ben Hammond 2014
    D. Hampshire 2017 - Python 3 restructuring and new function addition.
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

from rinchi_tools import conversion, utils, v02_convert
from rinchi_tools.reaction import Reaction
from rinchi_tools.rinchi_lib import RInChI as RInChI_Handle


###########
# CSV Tools
###########

def rdf_to_csv(rdf, outfile="File", return_rauxinfo=False, return_longkey=False, return_shortkey=False,
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

    Returns:
        The name of the CSV file created with the requested fields
    """

    # Generate header line
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

    data = conversion.rdf_to_rinchis(rdf, force_equilibrium=False, return_rauxinfos=return_rauxinfo,
                                     return_longkeys=return_longkey, return_shortkeys=return_shortkey,
                                     return_webkeys=return_webkey, return_rxndata=return_rxninfo)

    # Write new database file as .csv
    output_file, output_name = utils.create_output_file(outfile,csv)
    writer = csv.writer(output_file, delimiter='$')
    writer.writerow(header)
    writer.writerows(data)
    return output_name


def rdf_to_csv_append(rdf, csv_file):
    """
    Append an existing CSV file with values from an RD file

    Args:
        rdf: The RD file as a text block
        csv_file: the CSV file path
    """

    # Initialise a list that will contain all the RInChIs currently in the csv_file
    old_rinchis = []

    # Open the existing csv_file and read the header defining which fields are present
    with open(csv_file) as db:
        reader = csv.reader(db, delimiter="$")

        # Add all rinchis in the existing csv_file to a list
        header = reader.next()
        for row in reader:
            old_rinchis.append(row[0])

    return_rauxinfo = "RAuxInfo" in header
    return_longkey = "LongKey" in header
    return_shortkey = "ShortKey" in header
    return_webkey = "WebKey" in header
    return_rxninfo = "RXNInfo" in header

    # Construct a dict of RInChIs and RInChI data from the supplied rd file
    data = conversion.rdf_to_rinchis(rdf, force_equilibrium=False, return_rauxinfos=return_rauxinfo,
                                     return_longkeys=return_longkey, return_shortkeys=return_shortkey,
                                     return_webkeys=return_webkey, return_rxndata=return_rxninfo)

    # Convert both lists of rinchis into sets - unique, does not preserve order
    old_rinchis = set(old_rinchis)
    new_rinchis = set(entry['rinchi'] for entry in data)

    # The rinchis that need to be added to the csv_file are the complement of the new rinchis in the old
    rinchis_to_add = list(new_rinchis - old_rinchis)

    # Add all new, unique rinchis to the csv_file
    with open(csv_file, "a") as db:
        writer = csv.writer(db, delimiter='$')
        # Add rows determined
        writer.writerows(entry if entry['rinchi'] in rinchis_to_add else None for entry in data)


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

                # Send the names of any files that failed to be recognised to STDOUT
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


def create_sql_table(cursor, table_name, columns):
    """
    Create an SQL table

    Args:
        cursor: The SQLite database cursor object
        table_name: The name of the table to create
        columns: A list of column names to create
    """
    column_string = " TEXT, ".join(columns)
    cursor.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(table_name, column_string))


def get_sql_columns(cursor, table_name):
    """
    Get list of column names quickly

    Args:
        cursor: The SQLite database cursor object
        table_name: The name of the table

    Returns:
        A list of column names in order
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
        columns: A list of the columns in the table.  If not found, an attempt is made to get these automatically.
        exec_many: Whether to use cursor.execute() or cursor.executemany()
    """
    if columns is None:
        get_sql_columns(cursor, table_name)

    command = (
        "INSERT INTO {}({}) VALUES (".format(table_name, ", ".join(columns)) + ", ".join(["?"] * len(columns)) + ")")

    if exec_many:
        cursor.executemany(command, data)
    else:
        cursor.execute(command, data)


def check_table_exists(table_name, cursor):
    """
    Checks if a table exists within a database

    Args:
        table_name: The table name to check for
        cursor: The SQLite database cursor object

    Returns:
        True if present, False if Not.
    """
    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name= ?"
    if not cursor.execute(tb_exists, (table_name,)).fetchone():
        return False
    return True


def drop_table_if_needed(table_name, cursor):
    """
    Checks if table exists and drops the table if it does

    Args:
        table_name: The table to drop
        cursor: The SQLite database cursor object
    """
    if check_table_exists(table_name, cursor):
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

def sql_search(cursor, table_name, columns=None, lookup_value=None, field=None, use_like=False, limit=None):
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

    Returns:
        Cursor object which points to the result

    """
    if columns is None:
        columns = ["*"]

    # Set comparison method
    if use_like:
        comparator = "LIKE"
    else:
        comparator = "="

    # impose limit if required
    if limit is not None:
        limiter = " LIMIT {}".format(limit)
    else:
        limiter = ""

    # formulate the query
    part1 = 'SELECT {} FROM {}'.format(' ,'.join(columns), table_name)
    part2 = ' WHERE {} {} ?'.format(field, comparator)
    if lookup_value is None:
        command = part1 + limiter
    else:
        command = part1 + part2 + limiter

    cursor.execute(command, (lookup_value,))
    return cursor


def sql_key_to_rinchi(key, db_filename, table_name, keytype="L"):
    """
    Returns the RInChI matching the given Long RInChI key for a given database

    Args:
        key: The key to search for
        db_filename: The database in which to search
        table_name: The table in which to search for the key
        keytype: The key type to seach for.  Defaults to the long key

    Raises:
        ValueError: The keytype argument must be one of "L" , "S" or "W"

    Returns:
        the corresponding RInChI
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
    cursor = sql_search(cursor, table_name, ["rinchi"], key, field, )
    rinchi = cursor.fetchone()[0]
    db.close()
    return rinchi


def search_for_inchi(inchi, db_filename, table_name):
    """
    Searches for an inchi within a rinchi database.
    Approx.  20x faster than the version in rinchi_tools.analyse

    Args:
        inchi: The InChI to search for
        db_filename: the database to search within
        table_name: the database to search in
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    query = "%" + "/".join(inchi.split("/")[1:]) + "%"
    cursor = sql_search(cursor, table_name, ["rinchi"], query, "rinchi", True)
    for r in cursor:
        print((r[0]))

    return [i[0] for i in cursor.fetchall()]


def advanced_search(inchi, db_filename, table_name, hyb=None, val=None, rings=None, formula=None):
    """
    Search for an Inchi within a RInChi database with advanced options.  Output is to stdout.

    Args:
        inchi: The InChI to search for
        db_filename: the database to search within
        table_name: the datable to search in

        All args following are dicts of the format {property:count,property2:count2,...}
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

def rdf_to_sql(rdfile, db_filename, table_name, columns=None):
    """
    Creates or adds to an SQLite database the contents of a given RDFile.

    Args:
        rdfile: The RD file to add to the database
        db_filename: The file name of the SQLite database
        table_name: The name of the table to create or append
        columns: The columns to add.  If None, the default is [rinchi,rauxinfo,longkey,shortkey,webkey]
    """
    if columns is None:
        columns = ["rinchi", "rauxinfo", "longkey", "shortkey", "webkey"]

    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    create_sql_table(cursor, table_name, columns)

    # Repopulate columns variable.  Useful for pre-existing table
    columns = get_sql_columns(cursor, table_name)

    pragma_sql_env(cursor)

    # Open the rdfile and convert its contents to a dict of rinchis and rinchi data
    rdf_data = rinchi_tools.conversion.convert_rdf_to_dict(rdfile, columns)

    # Transform in place the dicts storing rxn info to their string representations
    for i in rdf_data.keys():
        rdf_data[i][1] = repr(rdf_data[i][1])

    rdf_data_tuple = [tuple([i] + rdf_data[i]) for i in rdf_data.keys()]

    # Add the rdf data to the dict
    sql_insert(cursor, table_name, rdf_data_tuple, columns, True)
    db.commit()
    db.close()


def csv_to_sql(csv_name, db_filename, table_name):
    """
    Creates or appends an SQL database with values from a CSV file

    Args:
        csv_name: The CSV filename
        db_filename: The SQLite3 database
        table_name: The name of the table to create or append
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    pragma_sql_env(cursor)

    with open(csv_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter="$")
        columns = reader.next()
        create_sql_table(cursor, table_name, columns)
        for row in reader:
            sql_insert(cursor, table_name, row)

    db.commit()
    db.close()


def convert_v02_v03(db_filename, table_name, v02_rinchi=False, v02_rauxinfo=False, v03_rinchi=False, v03_rauxinfo=False,
                    v03_longkey=False, v03_shortkey=False, v03_webkey=False):
    """
    Converts a database of v02 rinchis into a database of v03 rinchis and associated information.  N.B keys for v02
    are not required as new keys must be generated for the database.  Because of the nature of this problem,
    this is achieved by creating a new database for the processed data and then transferring back to the original

    Args:
         db_filename: The database filename to which the changes should be made.  The new database is added as a table.
         table_name: the name for the new v03 rinchi table.
         v02_rinchi: The name of the v02 rinchi column.  Defaults to False (No rinchi in database).
         v02_rauxinfo: The name of the v02 rauxinfo column.  Defaults to False (No rauxinfos in database).
         v03_rinchi: The name of the v03 new rinchi column.  Defaults to False (No rinchi column will be created).
         v03_rauxinfo: The name of the v03 new rinchi column.  Defaults to False (No rauxinfo column will be created).
         v03_longkey: The name of the v03 new rinchi column.  Defaults to False (No longkey column will be created).
         v03_shortkey: The name of the v03 new rinchi column.  Defaults to False (No shortkey column will be created).
         v03_webkey: The name of the v03 new webkey column.  Defaults to False (No webkey column will be created).

    """

    # Create database connections including for a temporary database and setup logging
    os.remove("conv0203.log")
    logging.basicConfig(filename='conv0203.log', level=logging.DEBUG)
    logging.info("\n========\nStarting Conversion Process\n========")
    start_time = time.time()

    # Construct SQL strings
    col_list = [v03_rinchi, v03_rauxinfo, v03_longkey, v03_shortkey, v03_webkey]
    columns = [column for column in col_list if column]

    # Check at least one column is desired
    if all(i == False for i in col_list):
        raise ValueError("Cannot create empty table")

    # Define the processing function
    def processing_function(row, args):
        """
        Processes a row of a RInChIs and RAuxInfo input into a tuple for adding to a queue

        Args:
            row: A tuple containing the RInChI and RAuxInfo
            args: Arguments for the function

        Returns:
            The data to add to the queue
        """
        the_rinchi = v02_convert.convert_rinchi(row[0])
        data_to_add = []
        if args[0]:
            data_to_add.append(the_rinchi)
        if args[1]:
            data_to_add.append(v02_convert.convert_rauxinfo(row[1]))
        if args[2]:
            data_to_add.append(RInChI_Handle().rinchikey_from_rinchi(the_rinchi, "L"))
        if args[3]:
            data_to_add.append(RInChI_Handle().rinchikey_from_rinchi(the_rinchi, "S"))
        if args[4]:
            data_to_add.append(RInChI_Handle().rinchikey_from_rinchi(the_rinchi, "W"))
        return tuple(data_to_add)

    # Check for existence of new table
    logging.info("Check for original table")  # Doing this now to prevent delays later
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    drop_table_if_needed(table_name, cursor)
    db.close()

    # Create args and run the queue
    pop_args = [populate_queue,
                [db_filename, "rinchis02", [v02_rinchi, v02_rauxinfo], processing_function, col_list]]
    depop_args = [depopulate_queue, [columns, table_name]]
    run_queue(1000, pop_args, depop_args)

    # Transfer table from temporary database to new database
    transfer_table("rinchi_temp.db", db_filename, table_name)
    logging.info("Finished conversion in {} seconds".format(time.time() - start_time))


def transfer_table(db_source, db_destination, table_name, drop_source=True):
    """
    Transfers a table from one database to another.  Optionally drops the source database

    Args:
        db_source: The name of the database to source the table
        db_destination: The name of the destination database
        table_name: The name of the table to transfer
        drop_source: Whether to drop the source database.  Defaults to True
    """
    logging.info("transferring {} from {} to {}...".format(table_name, db_source, db_destination))

    # Create connection and attach database
    db = sqlite3.connect(db_destination)
    cursor = db.cursor()
    cursor.execute("ATTACH DATABASE ? AS db2", (db_source,))

    # Execute SQL create command for the source table on the new table
    cursor.execute("SELECT sql FROM db2.sqlite_master WHERE type='table' AND name=?", (table_name,))
    cursor.execute(cursor.fetchone()[0])

    # Insert values from source to destination
    cursor.execute("INSERT INTO {0} SELECT * FROM db2.{0}".format(table_name))
    db.commit()
    db.close()

    # Drop the source table
    if drop_source:
        os.remove(db_source)


def gen_rauxinfo(db_filename, table_name):
    """
    Updates a table in a database to give rauxinfos where the column is null

    Args:
        db_filename: Database filename
        table_name: name of table
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    def converter(rinchi):
        """
        Interfaces the rauxinfo converter in v02_convert.py
        """
        rauxinfo = v02_convert.gen_rauxinfo(rinchi)
        return rauxinfo

    # Creating SQL function improves performance
    db.create_function("convert", 1, converter)
    cursor.execute(
        "UPDATE {} SET rauxinfo = convert(rinchi) WHERE rauxinfo IS NULL or rauxinfo = '';".format(table_name))
    db.commit()
    return

    ##########################################################
    # Fingerprinting
    ##########################################################


def compare_fingerprints(search_term, db_filename, table_name):
    """
    Search database for top 10 closest matches to a RInChI by fingerprinting method.  Sent to stdout.

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
    cursor = sql_search(cursor, table_name, ["longkey", "fingerprint"], limit=-1)
    for r in cursor:
        counter += 1
        res.append((r[0], distance.euclidean(fp1, pickle.loads(str(r[1])).toarray()[0])))
        if counter % 10000 == 0:
            per = int(float(100 * counter) / db_size)
            sys.stdout.write("\r {0}% complete".format(per))
            sys.stdout.flush()

    out = nsmallest(10, res, key=lambda s: s[1])
    print("\n", out)


def recall_fingerprints(lkey, db_filename, table_name):
    """
    Recall a fingerprint from the database

    Args:
        lkey: The long key to search for
        db_filename: The database filename
        table_name: The table name which stores the fingerprints

    Returns:
        A numpy array the reaction fingerprint as stored in the reaction database
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor = sql_search(cursor, table_name, ["fingerprint"], lkey, "longkey", )

    # Unpickle the binary data, and return a Numpy array containing the reaction fingerprint
    fpt = pickle.loads(str(cursor.fetchone()[0])).toarray()[0]
    db.close()

    return fpt


def update_fingerprints(db_filename, table_name, fingerprint_table_name):
    """
    NOT CURRENTLY WORKING.  NEEDS UPDATING TO USE MULTITHREADING FOR USABLE PERFORMANCE

    Calculates the reaction fingerprint as defined in the reaction Reaction class, and stores it in the given
    database in a compressed form

    Args:
        db_filename: the database filename to update
        table_name: The table containing the RInChIs
        fingerprint_table_name: The table to contain the fingerprint
    """
    db = sqlite3.connect(db_filename)

    # Poor method.  A database cannot have two cursors pointing at it.
    cursor = db.cursor()
    cursor2 = db.cursor()

    cursor = sql_search(cursor, table_name, fingerprint_table_name)

    counter = 0
    for lkey in cursor:

        try:
            # cursor.execute('''SELECT rinchi FROM rinchis WHERE longkey LIKE ?''', (lkey,))
            # rinchi = cursor.fetchone()[0]
            r = Reaction(lkey[0])
            r.calculate_reaction_fingerprint()

            # Pickle the reaction fingerprint - store it as binary data within an SQL BLOB field
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


def populate_queue(q, db_filename, table_name, source_columns, processing_function=None, processing_args=None):
    """
    Populates a queue with items processed from a database using a processing function provided.  If no processing
    function is provided then each row is simply placed into the queue.

    Args:
        q: A queue object instance
        db_filename: The filename of the database from which to populate the queue
        table_name: The name of the table from which to populate the queue
        source_columns: A list of columns to select from the table
        processing_function: A function which takes a row and outputs a row for the new table
        processing_args: List of arguments if needed to pass to the function
    """
    if callable(processing_function) or processing_function is None:
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        logging.info("populating")
        for row in sql_search(cursor, table_name):
            if processing_function is not None:
                row = processing_function(row, processing_args)
            q.put(row)
            while q.full():
                time.sleep(0.01)
        logging.info("finished_populating")
        db.close()
    else:
        raise ValueError("Function not given as argument 'Processing function'")


def depopulate_queue(q, columns, table_name):
    """
    Removes items from the queue and processes them to an output table

    Args:
        q: The queue to depopulate
        columns: the columns to create in the output table
        table_name: the name of the table to create
    """
    db = sqlite3.connect("rinchi_temp.db")
    cursor = db.cursor()
    create_sql_table(cursor, table_name, columns)
    logging.info("depopulating")
    while True:
        try:
            sql_insert(cursor, table_name, q.get(True, 2))
            # Waits for 2 seconds, otherwise throws `Queue.Empty`
        except queue.Empty:
            logging.info("Finished depopulating")
            break
    db.commit()
    db.close()


def run_queue(q_length, *threads):
    """
    Runs a set of functions as threads which perform functions on a queue and ends them together

    Args:
        q_length: The length of the queue to populate for converting the data
        *threads: The threads store as a tuple of the function name, and the arguments for that function, excluding
            the first argument which is the queue object created in this function
    """
    q = queue.Queue(q_length)
    thread_list = []

    # Create a list of thread objects
    for thread in threads:
        args = [q] + thread[1]
        thread_list.append(threading.Thread(target=thread[0], args=args))

    # Start the threads
    for thread in thread_list:
        thread.start()

    # End the threads together
    for thread in thread_list:
        thread.join()
