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

from rinchi_tools import _external, conversion, v02_tools
from rinchi_tools.reaction import Reaction
from rinchi_tools.rinchi_lib import RInChI as RInChI_Handle


###########
# SQL tools
###########

# Regularly used command wrappers. Not for external use
#################################

def _pragma_sql_env(cursor):
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


def _create_sql_table(cursor, table_name, columns):
    """
    Create an SQL table

    Args:
        cursor: The SQLite database cursor object
        table_name: The name of the table to create
        columns: A list of column names to create
    """
    column_string = " TEXT, ".join(columns)
    cursor.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(table_name, column_string))


def _get_sql_columns(cursor, table_name):
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


def _sql_insert(cursor, table_name, data, columns=None, exec_many=False):
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
        _get_sql_columns(cursor, table_name)

    command = (
        "INSERT INTO {}({}) VALUES (".format(table_name, ", ".join(columns)) + ", ".join(["?"] * len(columns)) + ")")

    if exec_many:
        cursor.executemany(command, data)
    else:
        cursor.execute(command, data)


def _check_table_exists(table_name, cursor):
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


def _drop_table_if_needed(table_name, cursor):
    """
    Checks if table exists and drops the table if it does

    Args:
        table_name: The table to drop
        cursor: The SQLite database cursor object
    """
    if _check_table_exists(table_name, cursor):
        approved = input("Table {} will be deleted and recreated. Continue? (type 'yes') :".format(table_name))
        if approved == "yes":
            cursor.execute('drop table if exists {}'.format(table_name))
            logging.info("dropping table")
        else:
            logging.info("exiting operation")
            sys.exit("Operation Aborted")
    return


def _sql_search(cursor, table_name, columns=None, lookup_value=None, field=None, use_like=False, limit=None):
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
    if limit is not None and limit != 0:
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

    if lookup_value is not None:
        cursor.execute(command, (lookup_value,))
    else:
        cursor.execute(command)
    return cursor


def _transfer_table(db_source, db_destination, table_name, drop_source=True):
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


def _flat_file_to_search_db(path, delim="$"):
    """
    Creates and populates a temporary SQLite database for searching or analysis

    Args:
        path: The path of the file with which to populate the table
        delim: The delimiter of the flat file

    Returns:
        A cursor object pointing to the opened database.

    """
    search_db = sqlite3.connect("")  # Create temporary database
    cursor = search_db.cursor()
    _create_sql_table(cursor, "temp", ['rinchi'])

    def read_flat_file_lines(path, delim):
        with open(path, 'r') as f:
            for line in f:
                yield tuple(line.split(delim))

    cursor.executemany("INSERT INTO temp VALUES (?)", read_flat_file_lines(path, delim))
    return cursor


def _string_finder(string, cursor, table_name, limit, field='rinchi'):
    """
    Search for a string in a database field

    Args:
        string:
        cursor:
        table_name:
        limit:

    Returns:
        A generator object of rinchis
    """

    # Remove header part of inchi
    if string.startswith("InChI="):
        string = string.split("/", 1)[1]
    query = "%" + string + "%"
    cursor = _sql_search(cursor, table_name, ["rinchi"], query, field, True, limit)

    return (i[0] for i in cursor.fetchall())


# Searching SQL databases
#########################


def sql_key_to_rinchi(key, db_filename, table_name, keytype="L", column=None):
    """
    Returns the RInChI matching the given Long RInChI key for a given database

    Args:
        key: The key to search for
        db_filename: The database in which to search
        table_name: The table in which to search for the key
        keytype: The key type to seach for.  Defaults to the long key
        column: Optional column to look for the key in.

    Raises:
        ValueError: The keytype argument must be one of "L" , "S" or "W"

    Returns:
        the corresponding RInChI
    """

    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    if keytype == "L":
        field = "longkey"
    elif keytype == "S":
        field = "shortkey"
    elif keytype == "W":
        field = "webkey"
    elif column is not None:
        field = column
    else:
        raise ValueError('The keytype argument must be one of "L" , "S" or "W" or the column parameter must be given')
    cursor = _sql_search(cursor, table_name, ["rinchi"], key, field)
    rinchi = cursor.fetchone()[0]
    db.close()
    return rinchi


def search_rinchis(search_term, db=None, table_name=None, is_sql_db=False, hyb=None, val=None, rings=None, formula=None,
                   ringelements=None, isotopic=None, reactant=False, product=False, agent=False, number=1000):
    """
    Search for an Inchi within a RInChi database. Includes all options

    Args:
        db:
        is_sql_db:
        number:
        search_term: The term to search for
        table_name: the table to search in

        All args following are dicts of the format {property:count,property2:count2,...}
        hyb: The hybridisation changes(s) desired
        val: The valence change(s) desired
        rings: The ring change(s) desired
        formula: The formula change(s) desired
        reactant: Search for InChIs in the products
        product: Search for InChIs in the reactants
        agent: Search for InChIs in the agents
        ringelements:
        isotopic:

    Returns:
        A dictionary of lists where an inchi was found
    """
    if hyb is None:
        hyb = {}
    if val is None:
        val = {}
    if rings is None:
        rings = {}
    if formula is None:
        formula = {}
    if not any((hyb, rings, val, formula, True if isotopic is not None else False,
                True if ringelements is not None else False)):
        # Skip detection if not required
        skip = True
    else:
        skip = False

    if table_name is None:
        table_name = "rinchis03"
    if not (reactant or product or agent):
        reactant = True
        product = True
        agent = True

    if is_sql_db:
        # Search existing db
        db = sqlite3.connect(db)
        cursor = db.cursor()
        results = _string_finder(search_term, cursor, table_name, number)
    else:
        # Create a temporary db from a flat file
        cursor = _flat_file_to_search_db(db)
        results = _string_finder(search_term, cursor, table_name, number)

    result_dict = {'as_reactant': [], 'as_product': [], 'as_agent': []}

    # Linear
    for rinchi in results:
        r = Reaction(rinchi)
        if r.detect_reaction(hyb_i=hyb, val_i=val, rings_i=rings, formula_i=formula, isotopic=isotopic,
                             ring_present=ringelements) or skip:
            if reactant:
                if any(search_term in s for s in r.reactant_inchis):
                    result_dict['as_reactant'].append(rinchi)
            if product:
                if any(search_term in s for s in r.product_inchis):
                    result_dict['as_product'].append(rinchi)
            if agent:
                if any(search_term in s for s in r.agent_inchis):
                    result_dict['as_agent'].append(rinchi)

    return result_dict


def search_master(search_term, db=None, table_name=None, is_sql_db=False, hyb=None, val=None, rings=None, formula=None,
                  reactant=False, product=False, agent=False, number=1000, keytype=None, ring_type=None, isotopic=None):
    """
    Search for an string within a RInChi database. Includes all options.

    Args:
        ring_type:
        isotopic:
        db:
        is_sql_db:
        number: Maximum number of initial results
        search_term: The term to search for
        table_name: the table to search in
        reactant: Search for InChIs in the products
        product: Search for InChIs in the reactants
        agent: Search for InChIs in the agents
        keytype: The type of key to look for. If not found, then the function will check if the search term is a key,
        and try to parse the Key regardless. Otherwise, it assumes to look in the RInChIs

        All args following are dicts of the format {property:count,property2:count2,...}
        hyb: The hybridisation changes(s) desired
        val: The valence change(s) desired
        rings: The ring change(s) desired
        formula: The formula change(s) desired

    Returns:
        A dictionary of lists where an inchi was found
    """
    search_term = str(search_term)
    if keytype is None:
        if search_term.startswith(('Short-RInChIKey', 'Long-RInChIKey', 'Web-RInChIKey')):
            keytype = search_term[0]
    if keytype is not None:
        result_dict = {'rinchi': [sql_key_to_rinchi(search_term, db, table_name, keytype)]}
    else:
        result_dict = search_rinchis(search_term, db=db, table_name=table_name, isotopic=isotopic, is_sql_db=is_sql_db,
                                     hyb=hyb, val=val, rings=rings, ringelements=ring_type, formula=formula,
                                     reactant=reactant, product=product, agent=agent, number=number)
    return result_dict







# Converting to SQL databases
#############################


def rdf_to_sql(rdfile, db_filename, table_name, columns=None):
    """
    Creates or adds to an SQLite db the contents of a given RDFile.

    Args:
        rdfile: The RD file to add to the db
        db_filename: The file name of the SQLite db
        table_name: The name of the table to create or append
        columns: The columns to add.  If None, the default is [rinchi,rauxinfo,longkey,shortkey,webkey]
    """
    if columns is None:
        columns = ["rinchi", "rauxinfo", "longkey", "shortkey", "webkey"]

    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    _create_sql_table(cursor, table_name, columns)

    # Repopulate columns variable.  Useful for pre-existing table
    columns = _get_sql_columns(cursor, table_name)

    _pragma_sql_env(cursor)

    # Open the rdfile and convert its contents to a dict of rinchis and rinchi data
    rdf_data = conversion.rdf_to_rinchis(rdfile, columns=columns)

    # Transform in place the dicts storing rxn info to their string representations
    for i in rdf_data.keys():
        rdf_data[i][1] = repr(rdf_data[i][1])

    rdf_data_tuple = [tuple([i] + rdf_data[i]) for i in rdf_data.keys()]

    # Add the rdf data to the dict
    _sql_insert(cursor, table_name, rdf_data_tuple, columns, True)
    db.commit()
    db.close()


def csv_to_sql(csv_name, db_filename, table_name):
    """
    Creates or appends an SQL db with values from a CSV file

    Args:
        csv_name: The CSV filename
        db_filename: The SQLite3 db
        table_name: The name of the table to create or append
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    _pragma_sql_env(cursor)

    with open(csv_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter="$")
        columns = reader.next()
        _create_sql_table(cursor, table_name, columns)
        for row in reader:
            _sql_insert(cursor, table_name, row)

    db.commit()
    db.close()


def convert_v02_v03(db_filename, table_name, v02_rinchi=False, v02_rauxinfo=False, v03_rinchi=False, v03_rauxinfo=False,
                    v03_longkey=False, v03_shortkey=False, v03_webkey=False):
    """
    Converts a db of v02 rinchis into a db of v03 rinchis and associated information.  N.B keys for v02
    are not required as new keys must be generated for the db.  Because of the nature of this problem,
    this is achieved by creating a new db for the processed data and then transferring back to the original

    Args:
         db_filename: The db filename to which the changes should be made.  The new db is added as a table.
         table_name: the name for the new v03 rinchi table.
         v02_rinchi: The name of the v02 rinchi column.  Defaults to False (No rinchi in db).
         v02_rauxinfo: The name of the v02 rauxinfo column.  Defaults to False (No rauxinfos in db).
         v03_rinchi: The name of the v03 new rinchi column.  Defaults to False (No rinchi column will be created).
         v03_rauxinfo: The name of the v03 new rinchi column.  Defaults to False (No rauxinfo column will be created).
         v03_longkey: The name of the v03 new rinchi column.  Defaults to False (No longkey column will be created).
         v03_shortkey: The name of the v03 new rinchi column.  Defaults to False (No shortkey column will be created).
         v03_webkey: The name of the v03 new webkey column.  Defaults to False (No webkey column will be created).

    """

    # Create db connections including for a temporary db and setup logging
    os.remove("convert0203.log")
    logging.basicConfig(filename='conv0203.log', level=logging.DEBUG)
    logging.info("\n========\nStarting Conversion Process\n========")
    start_time = time.time()

    # Construct SQL strings
    col_list = [v03_rinchi, v03_rauxinfo, v03_longkey, v03_shortkey, v03_webkey]
    columns = [column for column in col_list if column]

    # Check at least one column is desired
    if all(i is False for i in col_list):
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
        the_rinchi = v02_tools.convert_rinchi(row[0])
        data_to_add = []
        if args[0]:
            data_to_add.append(the_rinchi)
        if args[1]:
            data_to_add.append(v02_tools.convert_rauxinfo(row[1]))
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
    _drop_table_if_needed(table_name, cursor)
    db.close()

    # Create args and run the queue
    pop_args = [_populate_queue, [db_filename, "rinchis02", [v02_rinchi, v02_rauxinfo], processing_function, col_list]]
    depop_args = [_depopulate_queue, [columns, table_name]]
    _run_queue(1000, pop_args, depop_args)

    # Transfer table from temporary db to new db
    _transfer_table(_external.RINCHI_TEMP_DATABASE, db_filename, table_name)
    logging.info("Finished conversion in {} seconds".format(time.time() - start_time))


def gen_rauxinfo(db_filename, table_name):
    """
    Updates a table in a db to give rauxinfos where the column is null

    Args:
        db_filename: Database filename
        table_name: name of table
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()

    def converter(rinchi):
        """
        Interfaces the rauxinfo converter in v02_tools.py
        """
        rauxinfo = v02_tools.generate_rauxinfo(rinchi)
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
    Search db for top 10 closest matches to a RInChI by fingerprinting method.  Sent to stdout.

    Args:
        search_term: A RInChi or Long-RInChIKey to search with
        db_filename: the db containing the fingerprints
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
    cursor = _sql_search(cursor, table_name, ["longkey", "fingerprint"], limit=-1)
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
    Recall a fingerprint from the db

    Args:
        lkey: The long key to search for
        db_filename: The db filename
        table_name: The table name which stores the fingerprints

    Returns:
        A numpy array the reaction fingerprint as stored in the reaction db
    """
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor = _sql_search(cursor, table_name, ["fingerprint"], lkey, "longkey", )

    # Unpickle the binary data, and return a Numpy array containing the reaction fingerprint
    fpt = pickle.loads(str(cursor.fetchone()[0])).toarray()[0]
    db.close()

    return fpt


def update_fingerprints(db_filename, table_name, fingerprint_table_name):
    """
    NOT CURRENTLY WORKING.  NEEDS UPDATING TO USE MULTITHREADING FOR USABLE PERFORMANCE

    Calculates the reaction fingerprint as defined in the reaction Reaction class, and stores it in the given
    db in a compressed form

    Args:
        db_filename: the db filename to update
        table_name: The table containing the RInChIs
        fingerprint_table_name: The table to contain the fingerprint
    """
    db = sqlite3.connect(db_filename)

    # Poor method.  A db cannot have two cursors pointing at it.
    cursor = db.cursor()
    cursor2 = db.cursor()

    cursor = _sql_search(cursor, table_name, fingerprint_table_name)

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


def _populate_queue(q, db_filename, table_name, source_columns, processing_function=None, processing_args=None):
    """
    Populates a queue with items processed from a db using a processing function provided.  If no processing
    function is provided then each row is simply placed into the queue.

    Args:
        q: A queue object instance
        db_filename: The filename of the db from which to populate the queue
        table_name: The name of the table from which to populate the queue
        source_columns: A list of columns to select from the table
        processing_function: A function which takes a row and outputs a row for the new table
        processing_args: List of arguments if needed to pass to the function
    """
    if callable(processing_function) or processing_function is None:
        db = sqlite3.connect(db_filename)
        cursor = db.cursor()
        logging.info("populating")
        for row in _sql_search(cursor, table_name, source_columns):
            if processing_function is not None:
                row = processing_function(row, processing_args)
            q.put(row)
            while q.full():
                time.sleep(0.01)
        logging.info("finished_populating")
        db.close()
    else:
        raise ValueError("Function not given as argument 'Processing function'")


def _depopulate_queue(q, columns, table_name):
    """
    Removes items from the queue and processes them to an output table

    Args:
        q: The queue to depopulate
        columns: the columns to create in the output table
        table_name: the name of the table to create
    """
    db = sqlite3.connect(_external.RINCHI_TEMP_DATABASE)
    cursor = db.cursor()
    _create_sql_table(cursor, table_name, columns)
    logging.info("depopulating")
    while True:
        try:
            _sql_insert(cursor, table_name, q.get(True, 2))
            # Waits for 2 seconds, otherwise throws `Queue.Empty`
        except queue.Empty:
            logging.info("Finished depopulating")
            break
    db.commit()
    db.close()


def _run_queue(q_length, *threads):
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
