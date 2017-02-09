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
import re
from time import strftime

from rinchi_tools import tools, utils
from rinchi_tools.rinchi_lib import RInChI as RInChI_Handle


def _rxn_to_molfs(rxn):
    """
    Accept an RXNfile and return lists of reactant and product molfiles.

    The function takes a RXNfile, and returns three lists: the first is a list of the reactants' molfiles,
    the second a list of the products' molfiles and the third is a list of agents e.g.  solvents or catalysts.

    Args:
        rxn: The contents of an RXN file in the form of a string.

    Returns:
        A tuple of three lists; the first a list of the reactants' molfiles, the second a list of the products' and
        the third a list of the agents'. These molfiles are also in the form of strings.
    """

    # Count the stated number of reactants and products in the RXN file.
    rxnts_prods_line = rxn.splitlines()[4]
    num_reactants = int(rxnts_prods_line[0:3])
    num_products = int(rxnts_prods_line[3:6])

    # Count the number of agents if present; else count zero
    if len(rxnts_prods_line) > 6:
        num_agents = int(rxnts_prods_line[6:9])
    else:
        num_agents = 0

    # Split all entries
    mol_entries = rxn.split('M  END')
    for index, item in enumerate(mol_entries):
        mol_entries[index] = item.lstrip() + 'M  END'

    # Delete data before the first "$MOL".
    mol_entries[0] = '$MOL' + mol_entries[0].split('$MOL')[1]

    # Remove data after the final "M  END" and store it.
    rdata = mol_entries.pop(-1)[:-7]

    # Loop through these sections collecting up the reactants, products and agents.
    reactants = []
    for rr in range(0, num_reactants):
        rxnt = mol_entries[rr].replace('\n', '', 1)
        reactants.append(rxnt)
    products = []
    for pp in range(0, num_products):
        prod = mol_entries[num_reactants + pp].replace('\n', '', 1)
        products.append(prod)
    agents = []
    for aa in range(0, num_agents):
        agnt = mol_entries[num_reactants + num_products + aa].replace('\n', '', 1)
        agents.append(agnt)
    return reactants, products, agents, rdata


def _molfs_to_rxn(rxnt_molfs=None, prod_molfs=None, agnt_molfs=None, name=''):
    """
    Convert a list of reactant and product Molfiles into a RXN file.

    Args:
        rxnt_molfs: A list of reactant molfiles.
        prod_molfs: A list of product molfiles.
        agnt_molfs: An optional list of non-standard agent molfiles
        name: Optional name to add to molfile header

    Returns:
        rxn: An RXN file made up of the product and reactant molfiles.
    """

    if agnt_molfs is None:
        agnt_molfs = []
    if prod_molfs is None:
        prod_molfs = []
    if rxnt_molfs is None:
        rxnt_molfs = []

    def remove_mol(molfs):
        """
        Remove $MOL header if it exists.  So that the function accepts both with and without headers
        """
        for idx, molf in enumerate(molfs):
            if "$MOL" in molf:
                molfs[idx] = molf.split("$MOL", 1)[1]
        return molfs

    num_rxnts = len(rxnt_molfs)
    num_prods = len(prod_molfs)
    line_3 = '      RInChI0.03'
    header = '$RXN\n' + name + '\n' + line_3 + '\n\n'

    def nnn_maker(num):
        num = str(num)
        whitespace_length = 3 - len(num)
        return ' ' * whitespace_length + num

    rrrppp = nnn_maker(num_rxnts) + nnn_maker(num_prods) + '\n'
    rxnts = '$MOL\n' + '\n$MOL\n'.join(remove_mol(rxnt_molfs)) + '\n'
    prods = '$MOL\n' + '\n$MOL\n'.join(remove_mol(prod_molfs)) + '\n'
    agnts = '$MOL\n' + '\n$MOL\n'.join(remove_mol(agnt_molfs))
    rxnfile = header + rrrppp + rxnts + prods + agnts
    return rxnfile


def _molfs_to_rdf(rxnt_molfs=None, prod_molfs=None, agnt_molfs=None, name=''):
    """
    Convert a list of reactant and product Molfiles into a RXN file.

    Args:
        rxnt_molfs: A list of reactant molfiles.
        prod_molfs: A list of product molfiles.
        agnt_molfs: An optional list of non-standard agent molfiles
        name: optional name for molfile header

    Returns:
        rdf: An RXN file made up of the product and reactant molfiles.
    """
    if agnt_molfs is None:
        agnt_molfs = []
    if prod_molfs is None:
        prod_molfs = []
    if rxnt_molfs is None:
        rxnt_molfs = []
    num_rxnts = len(rxnt_molfs)
    num_prods = len(prod_molfs)
    head = "$RDFILE 1\n$DATM {}\n$RFMT\n".format(strftime("%Y-%m-%d %H:%M:%S"))
    line_3 = '      RInChI0.03'
    header = head + '$RXN\n' + name + '\n' + line_3 + '\n\n'

    def wrap(in_list, pre, post):
        text = pre + '\n' + '\n{}\n{}'.format(pre, post).join(in_list) + '\n' + post
        return text

    def nnn_maker(num):
        num = str(num)
        whitespace_length = 3 - len(num)
        return ' ' * whitespace_length + num

    rrrppp = nnn_maker(num_rxnts) + nnn_maker(num_prods) + '\n'
    rxnts = wrap(rxnt_molfs, "$MOL", "")
    prods = wrap(prod_molfs, "$MOL", "")
    agnts = wrap(agnt_molfs, "$DTYPE ID\n$DATUM 1\n$DTYPE AGENT\n$DATUM $MFMT", "")
    rdfile = header + rrrppp + rxnts + prods + agnts
    return rdfile


def _split_rdf(rdfile, start=0, stop=0):
    """
    Convert RDFiles to a list of RInChI-friendly RXN files.

    Function takes an RDFile and converts it into a list of RXN files.

    However, this is not as simple as just splitting the RDFile into its constituent RXN entries, for some RXN
    entries contain additional data specifying variations on the core reaction.  Furthermore, each RXN entry (and
    every variation thereof) may have catalysts and solvents saved as molfiles embedded within the additional data.

    Therefore, in order to export a comprehensive list of RXN files described by the RDFile, each RXN entry is
    scanned for variations, and each variation is scanned for additional substances.

    Args:
        rdfile: The RD file text block
        start: The index of the first RXN entry to process
        stop: The index of the last RXN entry to process

    Returns:
        A list of rxnfiles for conversion to a RInChI
    """
    # First, split the RDfile into its component RXN entries.
    rxn_entries = rdfile.split('$RXN')
    rxn_entries = rxn_entries[1:]
    if stop != 0:
        rxn_entries = rxn_entries[:stop]
    rxn_entries = rxn_entries[start:]

    # Loop through the RDFile, scanning for variations and extra substances and creating a list of reactions.
    reactions = []

    for rxn_entry in rxn_entries:
        rxn_variations, rxn_data = _rdf_rxn_2_molfs(rxn_entry)
        for rxn_variation in rxn_variations:
            reactions.append((rxn_variation, rxn_data))

    # Convert the list of reaction tuples into a list of RXN files.
    rxnfiles = []
    for reaction in reactions:
        rdfile = _molfs_to_rdf(reaction[0][0], reaction[0][1], reaction[0][2])
        rdfile = rdfile.strip() + '\n' + reaction[1].strip()
        rxnfiles.append(rdfile)

    # Return the list of RXN files
    return rxnfiles


def _rdf_rxn_2_molfs(rxn_entry):
    """
    Converts an entry from an RDF to a list of reactions it describes.  Works for entries parsed from an RD file.

    Args:
        rxn_entry: An RXN entry from an RDFile.  This consists of everything following a "$RXN" tag.

    Returns:
        reactions: A list of tuples of lists; each tuple represents a reaction, and consists of a list of reactant
            molfiles and a list of product molfiles.  Catalysts, solvents, etc.  are returned as both a reactant and
            a product (i.e. present on both sides of the reaction).
    """
    # Count the declared number of reactants and products.
    rrrppp_line = rxn_entry.splitlines()[4]
    num_rxnts = int(rrrppp_line[0:3])
    num_prods = int(rrrppp_line[3:6])

    # Count the number of agents if present; else count zero
    if len(rrrppp_line) > 6:
        num_agents = int(rrrppp_line[6:9])
    else:
        num_agents = 0

    # Split the RXN entry at every occurrence of "M  END".
    mend_split = rxn_entry.split('M  END')
    for index, item in enumerate(mend_split):
        mend_split[index] = item.lstrip() + 'M  END'

    # Delete data before the first "$MOL".
    mend_split[0] = '$MOL' + mend_split[0].split('$MOL')[1]

    # Remove data after the final "M  END" and store it.
    additional_data = mend_split.pop(-1)[:-7]

    # Harvest the reactants, products, and agents and save them to lists.
    rxnts = mend_split[0:num_rxnts]
    prods = mend_split[num_rxnts:num_rxnts + num_prods]
    agnts = mend_split[num_rxnts + num_prods:num_rxnts + num_prods + num_agents]

    # Clean up reactants, products, and agents to make true molfiles.
    for sets in [rxnts, prods, agnts]:
        for index, item in enumerate(sets):
            sets[index] = '\n'.join(item.splitlines()[1:]).rstrip()

    # Save the remaining data to another list.
    leftover_data = mend_split[num_rxnts + num_prods + num_agents:]

    # Discard anything before a $DTYPE tag in the leftover data, leaving
    # behind only data sandwiched between a '$DTYPE' and an 'M  END' tag.
    for index, entry in enumerate(leftover_data):
        leftover_data[index] = entry.split('$DTYPE')[-1]

    # Count the number of reaction variations.
    # N.B.  this only works if variations are in "VARIATION(#)" format.
    num_variations = 1
    while "VARIATION(%d)" % (num_variations + 1) in rxn_entry:
        num_variations += 1

    # Extract any "reaction agents" saved as embedded molfiles within the data section of the reaction record,
    # and sort them according to variation.

    agents_by_variation = _agent_harvester(leftover_data, num_variations)

    # Create the final list of reactions
    reactions = []

    def rstriplist(listin):
        ret = [i.rstrip() for i in listin]
        return ret

    output_rxnts = list(set(rstriplist(rxnts)))
    output_prods = list(set(rstriplist(prods)))
    for agents in agents_by_variation:
        output_agents = list(set(agents + agnts))
        reactions.append((output_rxnts, output_prods, output_agents))

    # Return this list, and the additional data_pair
    return reactions, additional_data


def _agent_harvester(data, num_variations):
    """
    Parses agent variations from the leftover data at the end of a RD files

    Args:
        data: The leftover data at the end of the RD file
        num_variations: The number of variation in the leftover data section

    Returns:
        A complete list of agent variation stored as a list of lists
    """

    def cleanup_agent(datum):
        return datum.split('\n', 2)[2].rstrip()

    agent_variations = []
    for variation in range(0, num_variations):
        agents = []
        for datum in data:
            if "VARIATION(%d)" % num_variations in datum:
                item = cleanup_agent(datum).rstrip()
                if item not in agents:
                    agents.append(item)
        agent_variations.append(agents)
    return agent_variations


def rdf_to_rinchis(rdf, start=0, stop=0, force_equilibrium=False, return_rauxinfos=False, return_longkeys=False,
                   return_shortkeys=False, return_webkeys=False, return_rxndata=False):
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

    Returns:
        List of dicts of reaction data as defined above. The data types are the keys for each dict
    """
    # Split the RDFile into a list of RD files.
    rdfiles = _split_rdf(rdf, start, stop)

    # Looping over the RD files, convert each to a RInChI.
    data_list = []
    rinchis = []
    rauxinfos = []
    for rdfile in rdfiles:
        rinchi, rauxinfo = tools.dedupe_rinchi(*RInChI_Handle().rinchi_from_file_text("RD", rdfile, force_equilibrium))
        if rinchi not in rinchis and not (rauxinfo in rauxinfos or return_rauxinfos):  # Force unique entries
            data = {'rinchi': rinchi}
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
            if return_rxndata:
                d = rdfile.replace("\n", "")
                data_pairs = re.findall(r"\$DTYPE ([^$]+)\$DATUM ([^$]+)", d)
                dict_result = {p[0].replace("\r", ""): p[1].replace("\r", "") for p in data_pairs}
                data['rxn_data'] = dict_result
            data_list.append(data)

    return data_list


def rxn_to_rinchi(rxn_text, ret_rauxinfo=False, longkey=False, shortkey=False, webkey=False, force_equilibrium=False,
                  file_out=False):
    """

    Args:
        rxn_text:
        ret_rauxinfo:
        longkey:
        shortkey:
        webkey:
        force_equilibrium:
        file_out:

    Returns:

    """

    # Generate the requested data.
    rinchi, rauxinfo = RInChI_Handle().rinchi_from_file_text("RXN", rxn_text, force_equilibrium)
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
    Takes a file object or a multiline string and returns a list of output file text blocks (RXN or RDF)

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


def rinchi_to_keys(data, longkey=False, shortkey=False, webkey=False, inc_rinchi=False):
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
        assert isinstance(entry,dict)
        del entry['rauxinfo']
        # Calculate keys
        if longkey:
            entry['longkey'] = RInChI_Handle().rinchikey_from_rinchi(entry['rinchi'], "L") + '\n'
        if shortkey:
            entry['shortkey'] += RInChI_Handle().rinchikey_from_rinchi(entry['rinchi'], "S") + '\n'
        if webkey:
            entry['webkey'] += RInChI_Handle().rinchikey_from_rinchi(entry['rinchi'], "W") + '\n'
        if not inc_rinchi: # Remove rinchi if not needed
            del entry['rinchi']
    return data_list


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

    data = rdf_to_rinchis(rdf, force_equilibrium=False, return_rauxinfos=return_rauxinfo,
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
    data = rdf_to_rinchis(rdf, force_equilibrium=False, return_rauxinfos=return_rauxinfo,
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


