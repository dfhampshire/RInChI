"""
RInChI conversion module.

This module provides a variety of functions for the interconversion of RInChIS, Molfiles, RXNfiles and more.

    C.H.G. Allen 2012

    N.A. Parker 2013: minor additional material added (specifically, .rxn to mol file agent conversion and
        subsequent amendments for agents in the .rxn to RInChI converter). added support to the rxn2rinchi function
        for non standard .rxn files containing reaction agents specified separately from the reactants and products.
    B. Hammond 2014: extended support for non standard .rxn files to the rdf parsing functions. Modified all .rxn
        handling functions to no longer discard reaction data in the $DTYPE/$DATUM  format, instead optionally returns
        them.
    D.F. Hampshire 2016: Removed functions now included in source v0.03 software (commands that interface with
        RInChI).  Similar python functionality can be found from the rinchi_lib.py interfacing file.  Some functions
        are now modified to use this rinchi_lib.py interface.

"""
import csv
import os

from rinchi_tools import _rxn_rdf_patch, tools, utils
from rinchi_tools.rinchi_lib import RInChI as RInChI_Handle


def rdf_to_rinchis(rdf, start=0, stop=0, force_equilibrium=False, return_rauxinfos=False, return_longkeys=False,
                   return_shortkeys=False, return_webkeys=False, return_rxndata=False, return_rinchis=True,
                   columns=None):
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
        return_rxndata: If True, returns a list of the &DTYPE/$DATUM data stored in the rxnfiles
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
    for rinchi, rauxinfo in _rxn_rdf_patch.rdf_to_rinchi(rdf,start,stop,force_equilibrium):
        if rinchi not in rinchis and not (rauxinfo in rauxinfos or return_rauxinfos):  # Force unique entries
            data = {}
            if return_rinchis:
                data['rinchi'] = rinchi
                rinchis.append(rinchi)
            if return_rauxinfos:
                data['rauxinfo'] = rauxinfo
                rauxinfos.append(rauxinfo)
            if return_longkeys:
                longkey = RInChI_Handle().rinchikey_from_rinchi(rinchi, "L")
                data['longkey'] = longkey
            if return_shortkeys:
                shortkey = RInChI_Handle().rinchikey_from_rinchi(rinchi, "S")
                data['shortkey'] = shortkey
            if return_webkeys:
                webkey = RInChI_Handle().rinchikey_from_rinchi(rinchi, "W")
                data['webkey'] = webkey
            data_list.append(data)
    return data_list


def rxn_to_rinchi(rxn_text, ret_rauxinfo=False, longkey=False, shortkey=False, webkey=False, force_equilibrium=False):
    """

    Args:
        rxn_text:
        ret_rauxinfo:
        longkey:
        shortkey:
        webkey:
        force_equilibrium:

    Returns:
        a dictionary of data
    """

    # Generate the requested data.
    # Uses the python version as the C++ library version produces erroneous results
    rinchi, rauxinfo = _rxn_rdf_patch.rxn_to_rinchi(rxn_text, force_equilibrium)
    data = {'rinchi': rinchi}
    if ret_rauxinfo:
        data['rauxinfo'] = rauxinfo
    if longkey:
        data['longkey'] = RInChI_Handle().rinchikey_from_rinchi(rinchi, "L") + '\n'
    if shortkey:
        data['shortkey'] = RInChI_Handle().rinchikey_from_rinchi(rinchi, "S") + '\n'
    if webkey:
        data['webkey'] = RInChI_Handle().rinchikey_from_rinchi(rinchi, "W") + '\n'
    return data


def rinchi_to_file(data, rxnout=True):
    """
    Takes a file object or a multi-line string and returns a list of output file text blocks (RXN or RDF)

    Args:
        data:
        rxnout:

    Returns:
        A list of rxn of rd file text blocks

    """
    rinchi_data = tools.rinchi_to_dict_list(data)

    # Generate RXN file.
    list_files = []
    for entry in rinchi_data:
        assert isinstance(entry, dict)
        if rxnout:
            file_text = RInChI_Handle().file_text_from_rinchi(entry['rinchi'], entry.get('rauxinfo', ''), "RXN")
        else:
            file_text = RInChI_Handle().file_text_from_rinchi(entry['rinchi'], entry.get('rauxinfo', ''), "RD")
        list_files.append(file_text)

    return list_files


def rinchis_to_keys(data, longkey=False, shortkey=False, webkey=False, inc_rinchi=False):
    """
    Converts a list of rinchis in a flat file into a dictionary of RInChIs and keys

    Args:
        data: The data string or file object to parse
        longkey: Whether to include the longkey
        shortkey: Whether to include the shortkey
        webkey: Whether to include the webkey
        inc_rinchi: Whether to include the original rinchi

    Returns:
        list of dictionaries containing the data produced.
    """
    data_list = tools.rinchi_to_dict_list(data)
    for entry in data_list:
        assert isinstance(entry, dict)
        del entry['rauxinfo']
        # Calculate keys
        if longkey:
            entry['longkey'] = RInChI_Handle().rinchikey_from_rinchi(entry['rinchi'], "L") + '\n'
        if shortkey:
            entry['shortkey'] += RInChI_Handle().rinchikey_from_rinchi(entry['rinchi'], "S") + '\n'
        if webkey:
            entry['webkey'] += RInChI_Handle().rinchikey_from_rinchi(entry['rinchi'], "W") + '\n'
        if not inc_rinchi:  # Remove rinchi if not needed
            del entry['rinchi']
    return data_list


###########
# CSV Tools
###########


def rdf_to_csv(rdf, outfile="rinchi", return_rauxinfo=False, return_longkey=False, return_shortkey=False,
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

    data = rdf_to_rinchis(rdf, force_equilibrium=False, return_rauxinfos=return_rauxinfo,
                          return_longkeys=return_longkey, return_shortkeys=return_shortkey,
                          return_webkeys=return_webkey, return_rxndata=return_rxninfo)

    print(data)
    # Write new database file as .csv
    f = utils.create_output_file(outfile, csv)
    writer = csv.writer(f, delimiter='$')
    writer.writerow(header)
    writer.writerows(data)
    return f.name


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
    data = rdf_to_rinchis(rdf, force_equilibrium=False, return_rauxinfos=return_rauxinfo,
                          return_longkeys=return_longkey, return_shortkeys=return_shortkey,
                          return_webkeys=return_webkey, return_rxndata=return_rxninfo)

    print(data)
    # Convert both lists of rinchis into sets - unique, does not preserve order
    assert all(isinstance(i, dict) for i in data)
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
    db_name = ''

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
