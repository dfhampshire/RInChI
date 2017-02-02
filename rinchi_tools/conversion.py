"""
RInChI conversion module.

This module provides a variety of functions for the interconversion of RInChIS, Molfiles, RXNfiles and more.

    C.H.G. Allen 2012
    N.A. Parker 2013 - minor additional material added (specifically, .rxn to mol file agent conversion and
        subsequent amendments for agents in the .rxn to RInChI converter). added support to the rxn2rinchi function
        for non standard .rxn files containing reaction agents specified separately from the reactants and products.
    B. Hammond 2014 - extended support for non standard .rxn files to the rdf parsing functions. Modified all .rxn
        handling functions to no longer discard reaction data in the $DTYPE/$DATUM  format, instead optionally returns
        them.
    D.F. Hampshire 2016 - Removed functions now included in source v0.03 software (commands that interface with
        RInChI).  Similar python functionality can be found from the rinchi_lib.py interfacing file.  Some functions
        are now modified to use this rinchi_lib.py interface.

"""

import re
from time import strftime

from rinchi_tools import tools
from rinchi_tools.rinchi_lib import RInChI as RInChI_Handle


def rxn_2_molfs(rxn):
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


def molfs_2_rxn(rxnt_molfs=None, prod_molfs=None, agnt_molfs=None, name=''):
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


def molfs_2_rdf(rxnt_molfs=None, prod_molfs=None, agnt_molfs=None, name=''):
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


def split_rdf(rdfile, start=0, stop=0):
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
        rxn_variations, rxn_data = rdf_rxn_2_molfs(rxn_entry)
        for rxn_variation in rxn_variations:
            reactions.append((rxn_variation, rxn_data))

    # Convert the list of reaction tuples into a list of RXN files.
    rxnfiles = []
    for reaction in reactions:
        rdfile = molfs_2_rdf(reaction[0][0], reaction[0][1], reaction[0][2])
        rdfile = rdfile.strip() + '\n' + reaction[1].strip()
        rxnfiles.append(rdfile)

    # Return the list of RXN files
    return rxnfiles


def rdf_rxn_2_molfs(rxn_entry):
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

    agents_by_variation = agent_harvester(leftover_data, num_variations)

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


def agent_harvester(data, num_variations):
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


def rdf_2_rinchis(rdf, start=0, stop=0, force_equilibrium=False, return_rauxinfos=False, return_longkeys=False,
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
        rinchis: A list of RInChIs generated from the RDFile.
        rauxinfos: A list of the RInChIs' RAuxInfos.
        longkeys: A list of the RInChIs' Long-RInChIKeys.
        shortkeys: A list of the RInChIs' Short-RInChIKeys.
        webkeys: A list of the RInChIs' Web-RInChIKeys.
        rxndata: A list of the &DTYPE/$DATUM data stored in the rxnfiles
    """
    # Split the RDFile into a list of RD files.
    rdfiles = split_rdf(rdf, start, stop)

    # Looping over the RD files, convert each to a RInChI.
    rinchis = []
    rauxinfos = []
    longkeys = []
    shortkeys = []
    webkeys = []
    rxndata = []
    for rdfile in rdfiles:
        rinchi, rauxinfo = tools.deduper(*RInChI_Handle().rinchi_from_file_text("RD", rdfile, force_equilibrium))
        if not (rinchi in rinchis and ((not return_rauxinfos) or rauxinfo in rauxinfos)):  # Force unique entries
            rinchis.append(rinchi)
            if return_rauxinfos:
                rauxinfos.append(rauxinfo)
            if return_longkeys:
                longkey = RInChI_Handle().rinchikey_from_rinchi(rinchi, "L")
                longkeys.append(longkey)
            if return_shortkeys:
                shortkey = RInChI_Handle().rinchikey_from_rinchi(rinchi, "S")
                shortkeys.append(shortkey)
            if return_webkeys:
                webkey = RInChI_Handle().rinchikey_from_rinchi(rinchi, "W")
                webkeys.append(webkey)
            if return_rxndata:
                d = rdfile.replace("\n", "")
                data_pairs = re.findall(r"\$DTYPE ([^$]+)\$DATUM ([^$]+)", d)
                dict_result = {p[0].replace("\r", ""): p[1].replace("\r", "") for p in data_pairs}
                rxndata.append(dict_result)

    # Return everything specified
    output = [rinchis]
    if return_rauxinfos:
        output.append(rauxinfos)
    if return_longkeys:
        output.append(longkeys)
    if return_shortkeys:
        output.append(shortkeys)
    if return_webkeys:
        output.append(webkeys)
    if return_rxndata:
        output.append(rxndata)
    output = tuple(output)
    return output
