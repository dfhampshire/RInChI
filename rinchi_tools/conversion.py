"""
RInChI conversion module
------------------------

This module provides a variety of functions for the interconversion of RInChIS, Molfiles, RXNfiles and more.

Modifications:
 - C.H.G. Allen 2012
 - N.A. Parker 2013
    minor additional material added (specifically, .rxn to mol file agent conversion and
    subsequent amendments for agents in the .rxn to RInChI converter). added support to the rxn2rinchi function
    for non standard .rxn files containing reaction agents specified separately from the reactants and products.
 - B. Hammond 2014
    extended support for non standard .rxn files to the rdf parsing functions. Modified all .rxn
    handling functions to no longer discard reaction data in the $DTYPE/$DATUM  format, instead optionally returns
    them.
 - D.F. Hampshire 2016
    Removed functions now included in source v0.03 software (commands that interface with
    RInChI).  Similar python functionality can be found from the rinchi_lib.py interfacing file.  Some functions
    are now modified to use this rinchi_lib.py interface. Major restructuring across library means functions have
    been extensively moved to / from elsewhere.

"""
import csv
import os

from . import _rxn_rdf_patch, tools, utils
from .rinchi_lib import RInChI


def rdf_to_rinchis(rdf, start=0, stop=0, force_equilibrium=False, return_rauxinfos=False, return_longkeys=False,
                   return_shortkeys=False, return_webkeys=False, return_rinchis=True, columns=None):
    """
    Convert an RDFile to a list of RInChIs.

    Args:
        rdf: The contents of an RDFile as a string.
        start: The index of the RXN entry within the RDFile at which to start converting.  If set at default value (0),
            conversion begins from the first RXN entry.
        stop: The index of the RXN entry within the RDFile at which to stop converting.  If set at default value (0),
            conversion does not stop until the end of the file is reached.
        force_equilibrium: Whether to set the direction flags explicitly to equilibrium
        return_rauxinfos: If True, generates and returns RAuxInfo each generated RInChI.
        return_longkeys: If True, generates and returns Long-RInChIKeys for each generated RInChI.
        return_shortkeys: If True, generates and returns Short-RInChIKeys for each generated RInChI.
        return_webkeys: If True, generates and returns Web-RInChIKeys for each generated RInChI.
        return_rinchis: Return the rinchi. Defaults to True
        columns: the data to return may be given as list of headers instead.

    Returns:
        List of dicts of reaction data as defined above. The data types are the keys for each dict
    """
    # Split the RDFile into a list of RD files.

    if columns:
        if "rinchi" not in columns:
            return_rinchis = False
        if "rauxinfo" in columns:
            return_rauxinfos = True
        if "longkey" in columns:
            return_longkeys = True
        if "shortkey" in columns:
            return_shortkeys = True
        if "webkey" in columns:
            return_webkeys = True

    # Looping over the RD files, convert each to a RInChI.
    data_list = []
    rinchis = []
    rauxinfos = []

    for pair in _rxn_rdf_patch.rdf_to_rinchi(rdf, start, stop, force_equilibrium):
        rinchi, rauxinfo = pair
        if rinchi not in rinchis:  # Force unique entries
            data = {}
            if return_rinchis:
                data['rinchi'] = rinchi
                rinchis.append(rinchi)
            if return_rauxinfos:
                data['rauxinfo'] = rauxinfo
                rauxinfos.append(rauxinfo)
            if return_longkeys:
                longkey = RInChI().rinchikey_from_rinchi(rinchi, "L")
                data['longkey'] = longkey
            if return_shortkeys:
                shortkey = RInChI().rinchikey_from_rinchi(rinchi, "S")
                data['shortkey'] = shortkey
            if return_webkeys:
                webkey = RInChI().rinchikey_from_rinchi(rinchi, "W")
                data['webkey'] = webkey
            data_list.append(data)
    return data_list


def rxn_to_rinchi(rxn_text, ret_rauxinfo=False, longkey=False, shortkey=False, webkey=False, force_equilibrium=False):
    """
    Convert a RXN to a dictionary of calculated data.

    Args:
        rxn_text: The RXN text as a string
        ret_rauxinfo: Return RAuxInfo
        longkey: Return the Long Key
        shortkey: Return the Short Key
        webkey: Return the Web Key
        force_equilibrium: Force the output direction to be an equilibrium

    Returns:
        A dictionary of data with the key as the property name like so::

            {'rinchi': '[DATA], 'rauxinfo': [DATA, ... }

    """

    # Generate the requested data.
    # Uses the python version as the C++ library version produces erroneous results
    rinchi, rauxinfo = _rxn_rdf_patch.rxn_to_rinchi(rxn_text, force_equilibrium)
    data = {'rinchi': rinchi}
    if ret_rauxinfo:
        data['rauxinfo'] = rauxinfo
    if longkey:
        data['longkey'] = RInChI().rinchikey_from_rinchi(rinchi, "L")
    if shortkey:
        data['shortkey'] = RInChI().rinchikey_from_rinchi(rinchi, "S")
    if webkey:
        data['webkey'] = RInChI().rinchikey_from_rinchi(rinchi, "W")
    return data


def rinchi_to_file(data, rxnout=True):
    """
    Takes a file object or a multi-line string and returns a list of output file text blocks (RXN or RDF)

    Args:
        data: The string of a file input or a file object.
        rxnout: Return a reaction file. Otherwise, return an RD file

    Returns:
        A list of RXN of RD file text blocks

    """
    rinchi_data = tools.rinchi_to_dict_list(data)
    print(rinchi_data)

    # Generate RXN file.
    list_files = []
    for entry in rinchi_data:
        assert isinstance(entry, dict)
        if rxnout:
            file_text = RInChI().file_text_from_rinchi(entry['rinchi'], entry.get('rauxinfo', ''), "RXN")
        else:
            file_text = RInChI().file_text_from_rinchi(entry['rinchi'], entry.get('rauxinfo', ''), "RD")
        list_files.append(file_text)

    return list_files


def rinchis_to_keys(data, longkey=False, shortkey=False, webkey=False, inc_rinchi=False, inc_rauxinfo=False):
    """
    Converts a list of rinchis in a flat file into a dictionary of RInChIs and keys

    Args:
        inc_rauxinfo: Include the RAuxInfo in the result
        data: The data string or file object to parse
        longkey: Whether to include the longkey
        shortkey: Whether to include the shortkey
        webkey: Whether to include the webkey
        inc_rinchi: Whether to include the original rinchi

    Returns:
        list of dictionaries containing the data produced data with the key as the property name like so::

            {'rinchi': '[DATA], 'rauxinfo': [DATA, ... }
    """
    data_list = tools.rinchi_to_dict_list(data)
    for entry in data_list:
        assert isinstance(entry, dict)
        if 'rauxinfo' not in entry and inc_rauxinfo:
            # Generate rauxinfo
            entry['rauxinfo'] = tools.generate_rauxinfo(entry['rinchi'])
        if not inc_rauxinfo:
            try:
                del entry['rauxinfo']
            except KeyError:
                pass
        # Calculate keys
        if longkey:
            entry['longkey'] = RInChI().rinchikey_from_rinchi(entry['rinchi'], "L")
        if shortkey:
            entry['shortkey'] = RInChI().rinchikey_from_rinchi(entry['rinchi'], "S")
        if webkey:
            entry['webkey'] = RInChI().rinchikey_from_rinchi(entry['rinchi'], "W")
        if not inc_rinchi:
            # Remove RInChI if not needed
            del entry['rinchi']
    return data_list


###########
# CSV Tools
###########


def rdf_to_csv(rdf, outfile="rinchi", return_rauxinfo=False, return_longkey=False, return_shortkey=False,
               return_webkey=False):
    """
    Convert an RD file to a CSV file containing RInChIs and other optional parameters

    Args:
        rdf: The RD file as a text block
        outfile: Optional output file name parameter
        return_rauxinfo: Include RAuxInfo in the result
        return_longkey: Include Long key in the result
        return_shortkey: Include the Short key in the result
        return_webkey: Include the Web key in the result

    Returns:
        The name of the CSV file created with the requested fields
    """

    # Generate header line
    header = ["rinchi"]
    if return_rauxinfo:
        header.append("rauxinfo")
    if return_longkey:
        header.append("longkey")
    if return_shortkey:
        header.append("shortkey")
    if return_webkey:
        header.append("webkey")

    data = rdf_to_rinchis(rdf, force_equilibrium=False, return_rauxinfos=return_rauxinfo,
                          return_longkeys=return_longkey, return_shortkeys=return_shortkey,
                          return_webkeys=return_webkey)

    # Write new database file as .csv
    f, path = utils.create_output_file(outfile, '.csv')
    writer = csv.DictWriter(f, header, delimiter='$')
    writer.writeheader()
    writer.writerows(data)
    return os.path.abspath(path)


def rdf_to_csv_append(rdf, csv_file, existing_keys=None):
    """
    Append an existing CSV file with values from an RD file

    Args:
        rdf: The RD file as a text block
        csv_file: the CSV file path
        existing_keys: The keys already existing in the CSV file
    """

    # Open the existing csv_file and read the header defining which fields are present
    with open(csv_file) as f:
        reader = csv.DictReader(f, delimiter="$")
        header = reader.fieldnames
        if existing_keys is None:
            existing_keys = set(row['longkey'] for row in reader)

    return_rauxinfo = "rauxinfo" in header
    return_longkey = "longkey" in header
    return_shortkey = "shortkey" in header
    return_webkey = "webkey" in header

    # Construct a dict of RInChIs and RInChI data from the supplied rd file
    data = rdf_to_rinchis(rdf, force_equilibrium=False, return_rauxinfos=return_rauxinfo,
                          return_longkeys=return_longkey, return_shortkeys=return_shortkey,
                          return_webkeys=return_webkey)

    # Add all new, unique rinchis to the csv_file
    with open(csv_file, "a") as db:
        writer = csv.DictWriter(db, header, delimiter='$')
        # Add rows determined
        try:
            to_add = []
            for entry in data:
                assert isinstance(entry, dict)
                lkey = entry['longkey']
                if lkey not in existing_keys:
                    to_add.append(entry)
                    existing_keys.add(lkey)
            writer.writerows(to_add)
        except csv.Error:
            pass
    return existing_keys


def create_csv_from_directory(root_dir, outname, return_rauxinfo=False, return_longkey=False, return_shortkey=False,
                              return_webkey=False):
    """
    Iterate recursively over all rdf files in the given folder and combine them into a single .csv database.

    Args:
        root_dir: The directory to search
        outname: Output file name parameter
        return_rauxinfo: Include RAuxInfo in the result
        return_longkey: Include Long key in the result
        return_shortkey: Include the Short key in the result
        return_webkey: Include the Web key in the result

    Raises:
        IndexError: File failed to be recognised for importing
    """

    # Flag for whether the database should be created or appended
    database_has_started = False
    db_path = ''
    existing_keys = None
    # Iterate over all files in the root directory
    for root, folders, filenames in os.walk(root_dir):
        file_number = len(filenames)
        for number, filename in enumerate(filenames):
            print('processing {} of {}'.format((number + 1), file_number))
            filepath = os.path.join(root, filename)
            data = open(filepath).read()
            try:
                # Only try to process files with an .rdf extension
                if os.path.splitext(filename)[1] == ".rdf":
                    if database_has_started:
                        existing_keys = rdf_to_csv_append(data, db_path, existing_keys)
                    else:
                        db_path = rdf_to_csv(data, outname, return_rauxinfo, return_longkey, return_shortkey,
                                             return_webkey)
                        database_has_started = True
            except IndexError as e:
                # Send the names of any files that failed to be recognised to STDOUT
                print(e, ("Failed to recognise {}".format(filename)))
    return db_path
