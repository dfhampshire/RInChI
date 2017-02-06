"""
RInChI v0.02 to 0.03 conversion scripts.

    D.F. Hampshire 2016
"""

from rinchi_tools import _inchi_tools, tools, utils


class VersionError(Exception):
    """
    Define an exception which deals with InChI and RInChI versions
    """
    pass


def convert_rinchi(rinchi):
    """
    Convert a v0.02 RInChI into a v0.03 RInChI.

    Args:
        rinchi: A RInChI of version 0.02.

    Returns:
        rinchi: A RInChI of version 0.03.
    """
    layer2_inchis, layer3_inchis, layer4_inchis, direction, u_structs = _split_rinchi(rinchi)
    rinchi = tools.build_rinchi(layer2_inchis, layer3_inchis, layer4_inchis, direction, u_structs)
    return rinchi


def generate_rauxinfo(rinchi):
    """
    Create RAuxInfo for a RInChI using a conversion function.

    Args:
        rinchi: The RInChI of which to create the RAuxInfo.

    Returns:
        rauxinfo: The RAuxInfo of the RinChI

    Raises:
        VersionError: If the generated AuxInfos are not of the same version.

    """

    # Split the RInChI into constituent InChIs
    gp1_inchis, gp2_inchis, gp3_inchis, direct, u = _split_rinchi(rinchi)

    # Look up the AuxInfo for the InChIs.
    def auxinfo_convert(inchis):
        auxinfos = []
        for inchi in inchis:
            auxinfo = _inchi_tools.inchi_2_auxinfo(inchi)
            auxinfos.append(auxinfo)
        return auxinfos

    gp1_auxinfo = auxinfo_convert(gp1_inchis)
    gp2_auxinfo = auxinfo_convert(gp2_inchis)
    gp3_auxinfo = auxinfo_convert(gp3_inchis)

    # Format the AuxInfos for inclusion in the RAuxInfo.
    def rauxinfofy(auxinfos):
        """
        Process a group of AuxInfos for inclusion in a RAuxInfo.

        Args:
            auxinfos: A list of InChI AuxInfos.  An empty string in this list is
                interpreted as representing the AuxInfo of a structure which
                is unable to be described by an InChI.

        Returns:
            versions: A list of the version identifiers of the AuxInfos.
            auxinfo_group: A string of AuxInfo bodies delimited by double-
                slashes ("//") ready for inclusion in a RAuxInfo.


        """
        versions = []
        bodies = []
        for auxinfo in auxinfos:
            if auxinfo:
                split_auxinfo = auxinfo.split('=')[1].split('/', 1)
                version = split_auxinfo[0]
                versions.append(version)
                body = split_auxinfo[1]
            else:
                body = 'X'
            bodies.append(body)
        auxinfo_group = '//'.join(bodies)
        return versions, auxinfo_group

    auxinfo_gp1_verss, auxinfo_gp1 = rauxinfofy(gp1_auxinfo)
    auxinfo_gp2_verss, auxinfo_gp2 = rauxinfofy(gp2_auxinfo)
    auxinfo_gp3_verss, auxinfo_gp3 = rauxinfofy(gp3_auxinfo)

    # Check that all the auxinfo groups have the same version info.
    try:
        auxinfo_vers = utils.consolidate(auxinfo_gp1_verss + auxinfo_gp2_verss + auxinfo_gp3_verss)
    except ValueError:
        raise VersionError("RAuxInfo can only be made from same-version AuxInfos")

    # Construct and return the RAuxInfo
    if auxinfo_gp3:
        auxinfo_gp3 = '///' + auxinfo_gp3
    rauxinfo = 'RAuxInfo=%s.%s/%s///%s%s' % ("0.02", auxinfo_vers, auxinfo_gp1, auxinfo_gp2, auxinfo_gp3)
    return rauxinfo


def convert_rauxinfo(rauxinfo):
    """
    Convert a v0.02 RAuxInfo into a v0.03 RAuxInfo.

    Args:
        rauxinfo: A RAuxInfo of version 0.02.

    Returns:
        rauxinfo: A RAuxInfo of version 0.03.
    """
    layer2_auxinfos, layer3_auxinfos, layer4_auxinfos = _split_rauxinfo(rauxinfo)
    rauxinfo = tools.build_rauxinfo(layer2_auxinfos, layer3_auxinfos, layer4_auxinfos)
    return rauxinfo


def convert_all(rinchi, rauxinfo):
    """
    Convert a v0.02 RInChI & RAuxInfo into a v0.03 RInChI & RAuxInfo.

    Args:
        rinchi: A RInChI of version 0.02.
        rauxinfo: A RAuxInfo of version 0.02.

    Returns:
        rauxinfo: A RAuxInfo of version 0.03.
        rauxinfo: A RAuxInfo of version 0.03.
    """
    rauxinfo = convert_rauxinfo(rauxinfo)
    rinchi = convert_rauxinfo(rinchi)
    return rinchi, rauxinfo


def _split_rauxinfo(rauxinfo):
    """
    Convert a RAuxInfo to AuxInfos

    Args:
        rauxinfo: An RAuxInfo of version v0.02

    Returns:
        layer2_auxinfos: list of layer 2 auxinfos
        layer3_auxinfos: list of layer 3 auxinfos
        layer4_auxinfos: list of layer 4 auxinfos

    """

    # Separate version information from the RAuxInfo body.
    rauxinfo_version, rauxinfo_body = rauxinfo.split('=')[1].split('/', 1)
    auxinfo_version = rauxinfo_version.split('.', 2)[2]

    # Convert RAuxInfo groups to RAuxInfos
    rauxinfo_groups = rauxinfo_body.split('///')

    def auxinfo_builder(rauxinfo_group, auxinfo_version):
        auxinfo_bodies = rauxinfo_group.split('//')
        auxinfos = []
        for auxinfo_body in auxinfo_bodies:
            auxinfo = 'AuxInfo=' + auxinfo_version + '/' + auxinfo_body
            if auxinfo_body != "X":
                auxinfos.append(auxinfo)
        return auxinfos

    layer2_auxinfos = auxinfo_builder(rauxinfo_groups[0], auxinfo_version)
    layer3_auxinfos = auxinfo_builder(rauxinfo_groups[1], auxinfo_version)
    if len(rauxinfo_groups) > 2:
        layer4_auxinfos = auxinfo_builder(rauxinfo_groups[2], auxinfo_version)
    else:
        layer4_auxinfos = []
    return layer2_auxinfos, layer3_auxinfos, layer4_auxinfos


def _split_rinchi(rinchi):
    """
    Split a v0.02 RInChI into its constituent parts.

    Args:
        rinchi: A RInChI of version 0.02

    Raises:
        VersionError: RInChI must be version 0.02.

    Returns:
        layer2_inchis, layer3_inchis, layer4_inchis: Lists of the InChIs which made up the RInChI groups, returned in
        the order they were displayed. direction:"+","-", or "=" representing the direction of the reaction.
        u_structs: unknown structures in each layer in the form of a tuple (#2,#3,#4)

    """

    # Separate version information from the RInChI body.
    rinchi_version, rinchi_body = rinchi.split('=')[1].split('/', 1)
    if rinchi_version.startswith("0.02"):
        versions = rinchi_version.split('.', 2)
        if len(versions) > 1:
            inchi_version = versions[2]
        else:
            inchi_version = ''
    else:
        raise VersionError("RInChI must be version 0.02")

    # Remove reaction data layers.
    direction = ""
    if '/d+' == rinchi_body[-3:]:
        rinchi_body = rinchi_body[:-3]
        direction = "+"
    if '/d-' == rinchi_body[-3:]:
        rinchi_body = rinchi_body[:-3]
        direction = "-"
    if '/d=' == rinchi_body[-3:]:
        rinchi_body = rinchi_body[:-3]
        direction = "="

    # Convert RInChI groups to InChIs
    rinchi_groups = rinchi_body.split('///')

    def inchi_builder(rinchi_group, inchi_version):
        u_struct = 0
        if rinchi_group:
            inchi_bodies = rinchi_group.split('//')
            inchis = []
            for inchi_body in inchi_bodies:
                if inchi_body == "X" or inchi_body == "x":
                    u_struct += 1
                else:
                    inchi = 'InChI=' + inchi_version + '/' + inchi_body
                    inchis.append(inchi)
            return inchis, u_struct
        else:
            return [], u_struct

    layer2_inchis, l2u = inchi_builder(rinchi_groups[0], inchi_version)
    layer3_inchis, l3u = inchi_builder(rinchi_groups[1], inchi_version)
    if len(rinchi_groups) > 2:
        layer4_inchis, l4u = inchi_builder(rinchi_groups[2], inchi_version)
    else:
        layer4_inchis = []
        l4u = 0
    u_structs = [l2u, l3u, l4u]
    return layer2_inchis, layer3_inchis, layer4_inchis, direction, u_structs
