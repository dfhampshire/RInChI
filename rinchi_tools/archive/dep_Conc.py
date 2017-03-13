from time import strftime


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
