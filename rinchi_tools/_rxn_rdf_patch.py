"""
Patch for the v0.03 C++ release to import non standard RXN and RD files.

Modifications:

 - C. Allen 2012

 - D.F. Hampshire 2017
"""

import os
import re
import tempfile

from . import _external, tools, utils


def rxn_to_molfs(rxn):
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

    while not rxn.startswith('$RXN'):
        rxn = rxn[1:]
    rxnts_prods_line = rxn.splitlines()[4]
    num_reactants = int(rxnts_prods_line[0:3])
    num_products = int(rxnts_prods_line[3:6])

    # Count the number of agents if present; else count zero
    if len(rxnts_prods_line) > 6:
        num_agents = int(rxnts_prods_line[6:9])
    else:
        num_agents = 0

    # Split all entries
    mol_entries = [item.strip() for item in rxn.split('M  END')]

    # Delete data before the first "$MOL".
    mol_entries[0] = '$MOL' + mol_entries[0].split('$MOL')[1]

    # Remove data after the final "M  END" and store it.

    # Loop through these sections collecting up the reactants, products and agents.
    reactants = []
    for rr in range(0, num_reactants):
        rxnt = mol_entries.pop(0)[5:] + '\nM  END'
        reactants.append(rxnt)
    products = []
    for pp in range(0, num_products):
        prod = mol_entries.pop(0)[5:] + '\nM  END'
        products.append(prod)
    agents = []
    for aa in range(0, num_agents):
        agnt = mol_entries.pop(0)[5:] + '\nM  END'
        agents.append(agnt)
    return reactants, products, agents, mol_entries


def rdf_to_molfs(rdfile, start=0, stop=0):
    """
    Convert RDFiles to a list of molfiles files.

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
    rxn_entries = rdfile.split('$RFMT')
    rxn_entries = rxn_entries[1:]
    if stop != 0:
        rxn_entries = rxn_entries[:stop]
    rxn_entries = rxn_entries[start:]

    # Loop through the RDFile, scanning for variations and extra substances and creating a list of reactions.
    reactions = []

    for rxn_entry in rxn_entries:
        rxns = _rdf_rxn_2_molfs(rxn_entry)
        reactions.extend(rxns)
    return reactions


def _rdf_rxn_2_molfs(rxn_entry):
    """
    Converts an entry from an RDF to a list of reactions it describes.  Works for entries parsed from an RD file.

    Args:
        rxn_entry: An RXN entry from an RDFile.  This consists of everything following a "$RXN" tag.

    Returns:
        A list of tuples of lists; each tuple represents a reaction, and consists of a list of reactant
        molfiles and a list of product molfiles.  Catalysts, solvents, etc.  are returned as both a reactant and
        a product (i.e. present on both sides of the reaction).
    """
    reactants, products, agents, ldata = rxn_to_molfs(rxn_entry.strip())

    # Discard anything before a $DTYPE tag in the leftover data, leaving
    # behind only data sandwiched between a '$DTYPE' and an 'M  END' tag.
    ldata = [item.split('$DTYPE')[-1] for item in ldata]

    # Extract any "reaction agents" saved as embedded molfiles within the data section of the reaction record,
    # and sort them according to variation.

    agents_by_variation = _agent_harvester(ldata)

    # Create the final list of reactions
    reactions = []

    def rstriplist(listin):
        return (i.rstrip() for i in listin)

    output_rxnts = list(set(rstriplist(reactants)))
    output_prods = list(set(rstriplist(products)))
    reactions.append((output_rxnts, output_prods, list(set(rstriplist(agents)))))
    for agents_set in agents_by_variation:
        output_agents = list(set(agents_set + agents))
        reactions.append((output_rxnts, output_prods, output_agents))
    # Return this list
    return reactions


def _agent_harvester(data):
    """
    Parses agent variations from the leftover data at the end of a RD files

    Args:
        data: The leftover data at the end of the RD file

    Returns:
        A complete list of agent variation stored as a list of lists
    """

    def cleanup_agent(datum):
        return datum.split('\n', 2)[2].rstrip()

    agent_variations = {}

    for datum in data:
        value = re.findall('VARIATION\((\d+)\)', datum)
        if value is not None and value:
            variation = int(value[0])
            item = cleanup_agent(datum).rstrip()
            agent_variations.setdefault(variation, []).append(item)
    return agent_variations.values()


def molf_2_inchi(molf):
    """Run the InChI creation software on a molfile.

    The function works by saving the molfile string to a tempfile, and running
    the inchi-1 program on this tempfile as a subprocess.

    In the future, this funciton might be better implimented without the need
    to write the molfile to a temp directory.  A python implimentation of the
    inchi conversion software would allow this.

    Args:
        molf: The contents of a molfile as a string.

    Returns:
        A tuple containing:
            inchi:
                The InChI.
            auxinfo:
                The InChI's AuxInfo, if required.

        N.B. If the inchi program fails to generate data, an empty string will
        be returned instead.
    """
    # Saves the molfile to a temporary file.
    molf_tempfile = tempfile.NamedTemporaryFile(delete=False)
    molf_tempfile.write(bytes(molf, 'utf-8'))
    molf_tempfile.close()
    # Runs inchi-1 program on this molfile, and stores the output.
    inchi_args = [_external.INCHI_PATH, molf_tempfile.name, '-STDIO', '-NoLabels']
    inchi_out, inchi_log = utils.call_command(inchi_args)
    # Closes the molfile tempfile.
    os.unlink(molf_tempfile.name)
    # Finds and returns the inchi, auxinfo, and inchikey from the output.
    inchi_out_lines = inchi_out.splitlines()
    inchi = ''
    auxinfo = ''
    for line in inchi_out_lines:
        if line.startswith('InChI='):
            inchi = line
        if line.startswith('AuxInfo='):
            auxinfo = line
    # Returns everything requested.
    return inchi, auxinfo


def molfiles_2_rinchi(reactants, products, agents, direction='+', nstructs=''):
    """
    Convert an RXN file to a RInChI.

    Args:
        reactants: list of Reactant molfiles
        products: list of product molfiles
        agents: list of agent molfiles
        direction: The direction of the reaction
        nstructs: The no structure flag

    Returns:
        A tuple containing the rinchi and rauxinfo
    """

    # Run the InChI program on the Molfiles, generating AuxInfo if required.
    def collect_inchidata(molfile_group):
        for molfile in molfile_group:
            yield molf_2_inchi(molfile)

    reactants_i = list(collect_inchidata(reactants))
    products_i = list(collect_inchidata(products))
    agents_i = list(collect_inchidata(agents))
    # Build the RInChI for output.
    rinchi, rauxinfo = tools.build_rinchi_rauxinfo(reactants_i, products_i, agents_i, direction=direction,
                                                   u_struct=nstructs)

    # Return everything requested
    return rinchi, rauxinfo


def rxn_to_rinchi(rxn_entry, force_equilibrium=False):
    """
    Converts a rxn file to a RInChI

    Args:
        rxn_entry: The RXN entry as a string
        force_equilibrium: Whether to force the output RInChI to be an equilibrium reaction

    Returns:
        A tuple of RInChI and RAuxInfo data
    """
    reactants, products, agents, _ = rxn_to_molfs(rxn_entry.strip())
    if force_equilibrium:
        direction = '='
    else:
        direction = '+'
    rinchi, rauxinfo = molfiles_2_rinchi(reactants, products, agents, direction)
    return rinchi, rauxinfo


def rdf_to_rinchi(rdf_entry, start=0, stop=0, force_equilibrium=False):
    """
    Converts an RD file into a list of RInChIs

    Args:
        rdf_entry: The RD file as a string
        start: The index of the entry to start at.
        stop: The index of the entry to end at.
        force_equilibrium: Whether to force the output RInChI to be an equilibrium reaction

    Returns:
        A generator object yielding tuples of RInChI and RAuxInfo data
    """
    reactions = rdf_to_molfs(rdf_entry, start, stop)
    if force_equilibrium:
        direction = '='
    else:
        direction = '+'
    for reaction in reactions:
        reactants, products, agents = reaction
        out = molfiles_2_rinchi(reactants, products, agents, direction)
        yield out
