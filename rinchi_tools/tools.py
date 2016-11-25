"""
RInChI tools module.

    Copyright 2012 C.H.G. Allen, 2016 D.F. Hampshire

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

This module provides functions defining how RInChIs and RAuxInfos are
constructed from InChIs and reaction data.  It also interfaces with the RInChI
v0.03 software as provided by the InChI trust.

The RInChI library and programs are free software developed under the
auspices of the International Union of Pure and Applied Chemistry (IUPAC).

"""

from rinchi_tools import rinchi_lib, inchi_tools, utils

rinchi_interface = rinchi_lib.RInChI()

# The following variable defines the version number of RInChIs created by this
# module.
RINCHI_VERSION = '0.03'


# Define exceptions for the module to use.
class Error(Exception):
    pass


class VersionError(Error):
    pass


def build_rinchi(l2_inchis=None, l3_inchis=None, l4_inchis=None, direction='', u_struct=''):
    """
    Build a RInChI from the specified InChIs and reaction data.

    RInChI Builder takes three groups of InChIs, and additional reaction data
    (currently limited to directionality information), and returns a RInChI.

    Args:
        The first three arguments are groups of InChIs saved as strings within an iterable (e.g. a list, set, tuple).
        Any or all of these may be omitted.  All InChIs must be of the same version number. If a chemical which cannot
        be described by an InChI is desired within the RInChI, it should be added to the u_struct argument detailed
        below.
        l2_inchis:  Chemicals in the second layer of the RInChI
        l3_inchis:  Chemicals in the third layer of the RInChI
        l4_inchis:  Chemicals in the fourth layer of a RInChI. It refers to the substances present at the start
        and end of the reaction (e.g. catalysts, solvents), only referred to as "agents".
        direction: This must be "+", "-" or "=".  "+" means that l2_inchis_input are the reactants, and the
        l3_inchis the products; "-" means the opposite; and "=" means the l2_inchis and l3_inchis are in equilibrium.
        u_struct: Defines the number of unknown structures in each layer. This must be a list of the form [#2,#3,#4]
        where #2 is the number of unknown reactants in layer 2, #3 is number in layer 3 etc.

    Returns:
        The RinChI made from the input InChIs and reaction data.

    Raises:
        VersionError: The input InChIs are not of the same version.
    """
    # Convert the InChI layers to sets.
    if l4_inchis is None:
        l4_inchis = []
    if l3_inchis is None:
        l3_inchis = []
    if l2_inchis is None:
        l2_inchis = []
    l2_inchis = set(l2_inchis)
    l3_inchis = set(l3_inchis)
    l4_inchis = set(l4_inchis)
    # Ensure that all InChIs are in the right set, and not duplicated anywhere, and filtered accordingly.
    # If the InChI is in layer 2 and 3 then it is removed from those layers
    # and added to layer 4 (agents)
    l2_inchis_filtered = l2_inchis.difference(l3_inchis)
    l3_inchis_filtered = l3_inchis.difference(l2_inchis)
    l2_l3_overlap = l2_inchis.intersection(l3_inchis)
    l4_inchis_filtered = sorted(l4_inchis.union(l2_l3_overlap))
    # RInChIfy the InChIs
    l2_versions, l2_rinchi_layer = process_layer(l2_inchis_filtered)
    l3_versions, l3_rinchi_layer = process_layer(l3_inchis_filtered)
    l4_versions, l4_rinchi_layer = process_layer(l4_inchis_filtered)
    # Check that the input layers have the same version info.
    try:
        inchi_version = utils.consolidate(l2_versions + l3_versions + l4_versions)
    except Error:
        raise VersionError("RInChI can only be made from same-version InChIs.")
    # Decide in which order the RInChI layers should be displayed. Amend no structure flag accordingly.
    if l2_rinchi_layer > l3_rinchi_layer:
        reverse_direction = True
        rinchi_layer2 = l3_rinchi_layer
        rinchi_layer3 = l2_rinchi_layer
        if u_struct != '':
            u_struct[0], u_struct[1] = u_struct[1], u_struct[0]
    else:
        reverse_direction = False
        rinchi_layer2 = l2_rinchi_layer
        rinchi_layer3 = l3_rinchi_layer
    if l4_rinchi_layer:
        rinchi_layer4 = '<>' + l4_rinchi_layer
    else:
        rinchi_layer4 = ''
    # Create the appropriate direction layer.
    if direction:
        if direction == '+':
            if reverse_direction:
                dir_layer = '/d-'
            else:
                dir_layer = '/d+'
        elif direction == '-':
            if reverse_direction:
                dir_layer = '/d+'
            else:
                dir_layer = '/d-'
        elif direction == '=':
            dir_layer = '/d='
        else:
            dir_layer = ''
    else:
        dir_layer = ''
    # Recreate no structure flag
    ns_flag = ""
    if u_struct != '' and all([v != 0 for v in u_struct]):
        ns_flag = "/u" + '-'.join(map(str, u_struct))
    # Construct the RInChI.
    rinchi = 'RInChI=%s.%s/%s<>%s%s%s%s' % (
        RINCHI_VERSION, inchi_version, rinchi_layer2, rinchi_layer3, rinchi_layer4, dir_layer, ns_flag)
    return rinchi


def build_rinchi_rauxinfo(l2_input=None, l3_input=None, l4_input=None, direction='', u_struct=''):
    """
    Build a RInChI and RAuxInfo from the specified InChIs and reaction data.

    RInChI Builder takes three groups of InChIs, and additional reaction data, and returns a RInChI.

    Args:
        The first three arguments are tuples of InChI and RAuxInfo pairs within an iterable (e.g. a list, set, tuple).
        Any or all of these may be omitted.  All InChIs must be of the same version number. If a chemical which cannot
        be described by an InChI is desired within the RInChI, it should be added to the u_struct argument detailed
        below.
        l2_input:  Chemicals in the second layer of the RInChI
        l3_input:  Chemicals in the third layer of the RInChI
        l4_input:  Chemicals in the fourth layer of a RInChI. It refers to the substances present at the start
        and end of the reaction (e.g. catalysts, solvents), only referred to as "agents".
        direction: This must be "+", "-" or "=".  "+" means that the LHS are the reactants, and the RHS the products;
        "-" means the opposite; and "=" means the LHS and RHS are in equilibrium.
        u_struct: Defines the number of unknown structures in each layer. This must be a list of the form [#2,#3,#4]
        where #2 is the number of unknown reactants in layer 2, #3 is number in layer 3 etc.

    Returns:
        rinchi: The RinChI made from the input InChIs and reaction data.
        rauxinfo: The corresponding rauxinfo

    Raises:
        VersionError: The input InChIs are not of the same version.
    """
    # Convert the InChI layers to sets. Ignore the AuxInfos for now
    if l4_input is None:
        l4_input = []
    if l3_input is None:
        l3_input = []
    if l2_input is None:
        l2_input = []
    l2_inchis = set([el[0] for el in l2_input])
    l3_inchis = set([el[0] for el in l3_input])
    l4_inchis = set([el[0] for el in l4_input])
    auxinfo_lookup = dict(l2_input + l3_input + l4_input)
    # Ensure that all InChIs are in the right set, and not duplicated anywhere, and filtered accordingly.
    # If the InChI is in layer 2 and 3 then it is removed from those layers
    # and added to layer 4 (agents)
    l2_inchis_filtered = l2_inchis.difference(l3_inchis)
    l3_inchis_filtered = l3_inchis.difference(l2_inchis)
    l2_l3_overlap = l2_inchis.intersection(l3_inchis)
    l4_inchis_filtered = sorted(l4_inchis.union(l2_l3_overlap))
    # RInChIfy the InChIs
    l2_versions, l2_rinchi_layer, l2_rauxinfo = process_layer(l2_inchis_filtered, auxinfo_lookup)
    l3_versions, l3_rinchi_layer, l3_rauxinfo = process_layer(l3_inchis_filtered, auxinfo_lookup)
    l4_versions, l4_rinchi_layer, l4_rauxinfo = process_layer(l4_inchis_filtered, auxinfo_lookup)
    # Check that the input layers have the same version info.
    try:
        inchi_version = utils.consolidate(l2_versions + l3_versions + l4_versions)
    except Error:
        raise VersionError("RInChI can only be made from same-version InChIs.")
    # Decide in which order the RInChI layers should be displayed. Amend no structure flag accordingly.
    if l2_rinchi_layer > l3_rinchi_layer:
        reverse_direction = True
        rinchi_layer2 = l3_rinchi_layer
        rinchi_layer3 = l2_rinchi_layer
        raux_l2 = l3_rauxinfo
        raux_l3 = l2_rauxinfo
        # Reverse the no structure flag
        if u_struct != '':
            u_struct[0], u_struct[1] = u_struct[1], u_struct[0]
    else:
        reverse_direction = False
        rinchi_layer2 = l2_rinchi_layer
        rinchi_layer3 = l3_rinchi_layer
        raux_l2 = l2_rauxinfo
        raux_l3 = l3_rauxinfo
    if l4_rinchi_layer:
        rinchi_layer4 = '<>' + l4_rinchi_layer
        raux_l4 = '<>' + l4_rauxinfo
    else:
        rinchi_layer4 = ''
        raux_l4 = ''
    # Create the appropriate direction layer.
    if direction:
        if direction == '+':
            if reverse_direction:
                dir_layer = '/d-'
            else:
                dir_layer = '/d+'
        elif direction == '-':
            if reverse_direction:
                dir_layer = '/d+'
            else:
                dir_layer = '/d-'
        elif direction == '=':
            dir_layer = '/d='
        else:
            dir_layer = ''
    else:
        dir_layer = ''
    # Recreate no structure flag
    ns_flag = ""
    if u_struct != '' and all([v != 0 for v in u_struct]):
        ns_flag = "/u" + '-'.join(map(str, u_struct))
    # Construct the RInChI.
    rinchi = 'RInChI=%s.%s/%s<>%s%s%s%s' % (
        RINCHI_VERSION, inchi_version, rinchi_layer2, rinchi_layer3, rinchi_layer4, dir_layer, ns_flag)
    # Construct RAuxInfo
    rauxinfo = 'RAuxInfo=%s.%s/%s<>%s%s' % (RINCHI_VERSION, inchi_version, raux_l2, raux_l3, raux_l4)
    if rauxinfo == "RAuxInfo={}.{}/<>".format(RINCHI_VERSION, inchi_version):
        rauxinfo = ""
    return rinchi.strip(), rauxinfo.strip()


def build_rauxinfo(l2_auxinfo, l3_auxinfo, l4_auxinfo):
    """
    Takes 3 sets of AuxInfos and converts them into a RAuxInfo. n.b. The order of Inchis in each list is presumed to be
    corresponding to that in
    :param l2_auxinfo: List of layer 2 AuxInfos
    :param l3_auxinfo: List of layer 3 AuxInfos
    :param l4_auxinfo: List of layer 4 AuxInfos
    :return: An RAuxInfo
    """
    # Format the AuxInfos for inclusion in the RAuxInfo.
    l2_auxinfo_versions, auxinfo_l2 = process_layer(l2_auxinfo, None, False)
    l3_auxinfo_versions, auxinfo_l3 = process_layer(l3_auxinfo, None, False)
    l4_auxinfo_versions, auxinfo_l4 = process_layer(l4_auxinfo, None, False)
    # Check that all the auxinfo layers have the same version info.
    try:
        auxinfo_version = utils.consolidate(l2_auxinfo_versions + l3_auxinfo_versions + l4_auxinfo_versions)
    except Error:
        raise VersionError("RAuxInfo can only be made from same-version AuxInfos")
    # Construct and return the RAuxInfo
    if auxinfo_l4:
        auxinfo_l4 = '<>' + auxinfo_l4
    rauxinfo = 'RAuxInfo=%s.%s/%s<>%s%s' % (RINCHI_VERSION, auxinfo_version, auxinfo_l2, auxinfo_l3, auxinfo_l4)
    return rauxinfo


def split_rinchi_inc_auxinfo(rinchi, rinchi_auxinfo):
    """ Returns the inchi and auxinfo pairs, each in lists, the direction character, and a list of unknown structures.

        Args:
            rinchi: A RInChI String
            rinchi_auxinfo: The corresponding RAuxInfo

        Returns:
            rct_inchis: List of reactant inchi and auxinfo pairs
            pdt_inchis: List of product inchi and auxinfo pairs
            agt_inchis: List of agent inchi and auxinfo pairs
            direction: returns the direction character
            no_structs: returns a list of the numbers of unknown structures in each layer
    """
    inchi_components = rinchi_interface.inchis_from_rinchi(rinchi, rinchi_auxinfo)
    direction = inchi_components['Direction']
    reactants = inchi_components['Reactants']
    products = inchi_components['Products']
    agents = inchi_components['Agents']
    no_structs = inchi_components['No-Structures']
    return reactants, products, agents, direction, no_structs


def split_rinchi(rinchi):
    """ Returns the inchis without RAuxInfo, each in lists, and the direct and no_structs lists

        Args:
            rinchi: A RInChI String

        Returns:
            rct_inchis: List of reactant inchis
            pdt_inchis: List of product inchis
            agt_inchis: List of agent inchis
            direction: returns the direction character
            no_structs: returns a list of the numbers of unknown structures in each layer
    """
    inchi_components = rinchi_interface.inchis_from_rinchi(rinchi, "")
    direction = inchi_components['Direction']
    reactants = inchi_components['Reactants']
    products = inchi_components['Products']
    agents = inchi_components['Agents']
    no_structs = inchi_components['No-Structures']
    rct_inchis = [el[0] for el in reactants]
    pdt_inchis = [el[0] for el in products]
    agt_inchis = [el[0] for el in agents]
    return rct_inchis, pdt_inchis, agt_inchis, direction, no_structs


def split_rinchi_only_auxinfo(rinchi, rinchi_auxinfo):
    """ Returns the RAuxInfo"
        Args:
            rinchi: A RInChI String
            rinchi_auxinfo: The corresponding RAuxInfo

        Returns:
            rct_inchis_auxinfo: List of reactant AuxInfos
            pdt_inchis_auxinfo: List of product AuxInfos
            agt_inchis_auxinfo: List of agent AuxInfos
    """
    inchi_components = rinchi_interface.inchis_from_rinchi(rinchi, rinchi_auxinfo)
    reactants = inchi_components['Reactants']
    products = inchi_components['Products']
    agents = inchi_components['Agents']
    rct_inchis_auxinfo = [el[1] for el in reactants]
    pdt_inchis_auxinfo = [el[1] for el in products]
    agt_inchis_auxinfo = [el[1] for el in agents]
    return rct_inchis_auxinfo, pdt_inchis_auxinfo, agt_inchis_auxinfo


def deduper(rinchi, rauxinfo=""):
    """
    Removes duplicate InChI entries from the RInChI

    Args:
        rinchi: A RInChI string
        rauxinfo: Optional RAuxInfo
    """
    reactants, products, agents, direction, no_structs = split_rinchi_inc_auxinfo(rinchi, rauxinfo)
    reactants_s = set(reactants)
    products_s = set(products)
    agents_s = set(agents)
    for reactant in set(reactants):
        if reactant in products:
            agents_s.add(reactant)
            reactants_s.remove(reactant)
        if reactant in agents:
            reactants_s.remove(reactant)
    for product in set(products):
        if product in reactants:
            agents_s.add(product)
            products_s.remove(product)
        if product in agents:
            products_s.remove(product)
    # Because split rinchi returns the reactants and products, the direction to be sent to build_rinchi
    # should never be "-", as the build function is agnostic of reactants and products order as entered.
    if direction == "-":
        direction = "+"
    rinchi, rauxinfo = build_rinchi_rauxinfo(list(reactants_s), list(products_s), list(agents_s), direction, no_structs)
    if rauxinfo == "":
        return rinchi
    else:
        return rinchi, rauxinfo


def gen_rauxinfo(rinchi):
    """Create RAuxInfo for a RInChI using the InChI conversion function.

    Args:
        rinchi: The RInChI of which to create the RAuxInfo.

    Returns:
        The RAuxInfo of the RinChI.

    Raises:
        VersionError: If the generated AuxInfos are not of the same version.
    """
    # Split the RInChI into constituent InChIs
    reactants, products, agents, direction, u_s = split_rinchi(rinchi)

    # Need to "Re-reverse" to gain order as appeared in RInChI
    if direction == '-':
        l3_inchis, l2_inchis = reactants, products
    else:
        l2_inchis, l3_inchis = reactants, products

    # Look up the AuxInfo for the InChIs.

    def auxinfo_convert(inchis):
        auxinfos = []
        for inchi in inchis:
            auxinfo = inchi_tools.inchi_2_auxinfo(inchi)
            auxinfos.append(auxinfo)
        return auxinfos

    l2_auxinfo = auxinfo_convert(l2_inchis)
    l3_auxinfo = auxinfo_convert(l3_inchis)
    l4_auxinfo = auxinfo_convert(agents)
    rauxinfo = build_rauxinfo(l2_auxinfo, l3_auxinfo, l4_auxinfo)
    return rauxinfo


def process_layer(items, rauxinfodict=None, sort_layer=True, ):
    """ Processes a layer of InChIs or InChi-AuxInfos for outputting as a layer

        Args:
            items: A list of items to insert into the layer
            rauxinfodict: A dictionary of inchis as the keys and Auxinfos as the items
            sort_layer: Whether to sort the items in each layer. Defaults to True

        Returns:
            versions: A list of the version identifiers
            layer: A string of bodies delimited by an exclamation mark ("!") ready for inclusion as a layer.
    """
    versions = []
    bodies = []
    rauxinfo_layer = None
    for item in items:
        # Isolate the InChI / RInChI text body
        if item:
            split_inchi = item.split('=')[1].split('/', 1)
            version = split_inchi[0]
            versions.append(version)
            body = split_inchi[1]
        bodies.append(body)
        # Rename key in the dictionary to just body text
        if rauxinfodict is not None:
            rauxinfodict[body] = rauxinfodict.pop(item).split('=')[1].split('/', 1)[1]
    if sort_layer:
        sort_bod = sorted(bodies)
        # Make the RAuxInfo layer
        if rauxinfodict is not None:
            rauxinfos = []
            for inchi in sort_bod:
                rauxinfo = rauxinfodict.get(inchi, "")
                if rauxinfo != "":
                    rauxinfos.append(rauxinfo)
            rauxinfo_layer = '!'.join(rauxinfos)
        layer = '!'.join(sort_bod)
    else:
        layer = '!'.join(bodies)
    if rauxinfodict is None:
        return versions, layer
    else:
        return versions, layer, rauxinfo_layer
