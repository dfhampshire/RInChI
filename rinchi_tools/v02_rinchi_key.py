"""
Version 0.02 RInChIKey generation library module.

This module provides functions to create Long- and Short-RInChIKeys from RInChIs.

The supplied implementation of the inchi_2_inchikey function uses the InChIKey creation algorithm from OASA,
a free python library for the manipulation of chemical formats, now stored permanently in the v02_inchi_key.py module.

Modifications:
 - C.H.G. Allen 2012
 - D.F. Hampshire 2016
    Modified for Python3 compatibility

"""

import hashlib

from . import _external, _v02_inchi_key, utils, v02_tools

# The following variable defines the version number of the RInChIKeys created
# by this module.
RINCHIKEY_VERSION = 'b'


def _inchi_2_inchikey(inchi):
    """
    Take an InChI and return its InChIKey.

    Args:
        inchi: An InChI.

    Returns:
        The InChI's inchikey.
    """
    raw_inchikey = _v02_inchi_key.key_from_inchi(inchi)
    inchikey = "InChIKey=" + raw_inchikey
    return inchikey


def rinchi_2_longkey(rinchi):
    """
    Create Long-RInChIKey from a RInChI.

    Args:
        rinchi: The RInChI of which to create the RAuxInfo.

    Returns:
        The Long-RInChIKey of the RinChI.
    """
    # Split the RInChI into constituent InChIs
    gp1, gp2, gp3, direction, ns = v02_tools._split_rinchi(rinchi)

    # Convert each InChI to an InChIKey
    def inchikey_converter(inchis):
        inchikeys = []
        for inchi in inchis:
            if inchi.split('/', 1)[1] == 'X':
                inchikeys.append('')
            else:
                key = _inchi_2_inchikey(inchi)
                inchikeys.append(key)
        return inchikeys

    gp1_inchikeys = inchikey_converter(gp1)
    gp2_inchikeys = inchikey_converter(gp2)
    gp3_inchikeys = inchikey_converter(gp3)

    # Format the InChIKeys for inclusion in the Long-RInChIKey.
    def rinchikeyfy(inchikeys):
        """
        Process a group of InChIKeys for inclusion in a Long-RInChIKey.

        Args:
            inchikeys: A list of InChIKeys.  An empty string in this list is interpreted as representing the Key of a
                structure which is unable to be described by an InChI.

        Returns:
            A tuple containing:
                versions:
                    A list of the version identifiers of the InchIKeys.
                inchikey_group:
                    A string of InChIKey bodies ready for inclusion in a Long-RInChIKey.
        """
        versions = []
        bodies = []
        for inchikey in inchikeys:
            if inchikey:
                headless_inchikey = inchikey.split('=')[1]
                version = headless_inchikey[23:25]
                versions.append(version)
                body = headless_inchikey[:23] + headless_inchikey[25:]
            else:
                body = 'X'
            bodies.append(body)
        inchikey_group = '-'.join(bodies)
        return versions, inchikey_group

    inchikey_gp1_verss, inchikey_gp1 = rinchikeyfy(gp1_inchikeys)
    inchikey_gp2_verss, inchikey_gp2 = rinchikeyfy(gp2_inchikeys)
    inchikey_gp3_verss, inchikey_gp3 = rinchikeyfy(gp3_inchikeys)

    # Get the version info of the InChIKeys
    inchikey_vers = utils.consolidate(inchikey_gp1_verss + inchikey_gp2_verss + inchikey_gp3_verss)

    # Hash reaction layers.
    if direction:
        direction = "d" + direction
    rxn_layers_hash = _rxn_layers_hasher([direction])

    # Construct and return the Long-RInChIKey
    if inchikey_gp3:
        inchikey_gp3 = '--' + inchikey_gp3
    longkey = 'Long-RInChIKey=%s%s-%s-%s--%s%s' % (
        RINCHIKEY_VERSION, inchikey_vers, rxn_layers_hash, inchikey_gp1, inchikey_gp2, inchikey_gp3)
    return longkey


def rinchi_2_shortkey(rinchi):
    """
    Create a Short-RInChIKey from a RInChI.

    Args:
        rinchi: The RInChI from which to create the Short-RInChIKey

    Returns:
        The Short-RInChIKey of the RInChI
    """
    gp1, gp2, gp3, di, ns = v02_tools._split_rinchi(rinchi)
    gp1_vers, gp1_major, gp1_minor = _rinchi_gp_hasher(gp1)
    gp2_vers, gp2_major, gp2_minor = _rinchi_gp_hasher(gp2)
    gp3_vers, gp3_major, gp3_minor = _rinchi_gp_hasher(gp3)
    vers = utils.consolidate([gp1_vers, gp2_vers, gp3_vers])
    rxn_layers_hash = _rxn_layers_hasher(["d" + di])
    shortkey = 'Short-RInChIKey=%s%s-%s-%s-%s-%s-%s-%s-%s' % (
        RINCHIKEY_VERSION, vers, rxn_layers_hash, gp1_major, gp2_major, gp3_major, gp1_minor, gp2_minor, gp3_minor)
    return shortkey


def _rinchi_gp_hasher(rinchi_gp):
    """
    Create a two-part hash of a RInChI group.

    Args:
        rinchi_gp: A list of InChIs, which together make up a RInChI group.

    Returns:
        key_vers, majors_hash, minors_hash: A two-part hash of the RInChI group.

    Raises:
        InchiError: If the InChI isn't version 1S.
    """
    majors = []
    minors = []
    key_vers = 'SA'
    total_proton_count = 0
    for inchi in rinchi_gp:
        if inchi.startswith('InChI='):
            inchi = inchi[6:]
        vers, body = inchi.split('/', 1)
        if vers != '1S':
            raise _external.InChIError('Sorry, only RInChI version X.X.1S is supported at present.')
        layers = body.split('/')
        major_layers = [layers[0]]
        proton_count = 0
        i = 1
        for layer in layers[1:]:
            if layer[0] in 'chq':
                major_layers.append(layer)
                i += 1
            elif layer[0] == 'p':
                proton_count += int(layer[1:])
                i += 1
            else:
                break
        minor_layers = layers[i:]
        major = '/'.join(major_layers)
        minor = '/'.join(minor_layers)
        minor = minor and "/" + minor
        majors.append(major)
        minors.append(minor)
        total_proton_count += proton_count
    majors_group = '//'.join(majors)
    any_minors = False
    for minor in minors:
        if minor:
            any_minors = True
    if any_minors:
        minors_group = '//'.join(minors)
    else:
        minors_group = ''
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    proton_count_letter = 13 + total_proton_count
    if proton_count_letter < 0:
        proton_count_letter = 0
    if proton_count_letter > 25:
        proton_count_letter = 0
    majors_hash = _alphabet_hash(majors_group, 10)
    minors_hash = alphabet[proton_count_letter] + _alphabet_hash(minors_group, 4)
    return key_vers, majors_hash, minors_hash


def _rxn_layers_hasher(rxn_layers):
    """
    Create a 5char "hash" of a RInChI's reaction layers.

    Args:
        rxn_layers: A list of the reaction layers, including their 1char flags(but not including the /'s)

    Returns:
        The 5char "hash".  The scare-quotes reflect the fact that this is not a true hash,
        as the first character is in fact a directionality flag.

    Raises:
        RinchiError: If the rxn_layers are non-standard.
    """

    # Loop over the layers looking for the direction layer, and set the direction flag accordingly.
    for index, layer in enumerate(rxn_layers):
        dlayer_found = False
        if layer.startswith('d'):
            if dlayer_found:
                raise _external.RInChIError('RInChI contains more than one direction layer!')
            if layer[1] == "+":
                dflag = "F"
            elif layer[1] == "-":
                dflag = "B"
            elif layer[1] == "=":
                dflag = "E"
            else:
                raise _external.RInChIError('Non-standard direction layer!')
            dlayer_found = True
            dlayer_index = index
    if not dlayer_found:
        dflag = 'N'

    # Remove the direction layer, if extant.
    if dlayer_found:
        del rxn_layers[dlayer_index]

    # Sort the other layers into a standard format, and hash them up.
    other_layers = '/'.join(rxn_layers)
    rest_hashed = _alphabet_hash(other_layers, 4)

    # Concatenate and return the final product.
    return dflag + rest_hashed


def _alphabet_hash(arg, length='64'):
    """
    Hash an argument using sha256 and alphabetical representation.

    Args:
        arg: Argument to hash
        length: the length of the SHA hash desired

    Returns:
        The SHA256 hash
    """
    length = int(length)

    def sha256_hash(arg):
        return hashlib.sha256(bytes(arg, encoding='utf-8')).hexdigest()

    def alphabet_encode(num, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        if num == 0:
            return alphabet[0]
        arr = []
        base = len(alphabet)
        while num:
            rem = num % base
            num //= base
            arr.append(alphabet[rem])
        arr.reverse()
        return ''.join(arr)

    digest = alphabet_encode(int(sha256_hash(arg), 16))
    if len(digest) > length:
        return digest[0:length]
    else:
        return digest
