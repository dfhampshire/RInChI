"""
RInChI analysis module.

    Copyright 2012 C.H.G. Allen 2016 D.F Hampshire

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

This module provides functions that use the InChI software are are not specific to RInchi.
It also provides a function for searching for InChIs in a database of RInChIs.

The RInChI library and programs are free software developed under the
auspices of the International Union of Pure and Applied Chemistry (IUPAC).
"""

import os
import tempfile

from rinchi_tools import external, utils


def get_conlayer(inchi):
    """
    Return the connectivity layer of an InChI.

    Args:
        inchi: An InChI.

    Returns:
        conlayer: The connectivity layer from the InChI, if extant (otherwise an empty
            string).
    """
    layers = inchi.split('/')[1:]
    # Remove data before the first "/" (version info and heading).
    layers = layers[1:]
    conlayer = ''
    for layer in layers:
        if layer.startswith('c'):
            conlayer = layer.replace('c', '')
    return conlayer


def count_rings(inchi):
    """
    Count the number of rings in an InChI.

    Args:
        inchi: An InChI.

    Returns:
        ring_count: The number of rings in the InChI.
    """
    full_conlayer = get_conlayer(inchi)
    # Split connectivity layer into contributions from different components.
    conlayers = full_conlayer.split(';')
    # For each component, count the number of rings and add it to the total.
    ring_count = 0
    for conlayer in conlayers:
        # Simple species do not have a connectivity layer.
        if conlayer:
            # Consider stoichiometry
            multiplier = 1
            if conlayer[1] == '*':
                multiplier = int(conlayer[0])
                conlayer = conlayer[2:]
            atoms = (conlayer.replace('(', '-').replace(')', '-')
                     .replace(',', '-').split('-'))
            for index, atom in enumerate(atoms):
                if atom in atoms[:index]:
                    ring_count += multiplier
    return ring_count


def count_sp2(inchi, wd=False):
    """
    Count the number of sp2 stereocentres.

    Args:
        inchi: An InChI.
        wd: Whether or not the stereocentre must be well-defined to be counted.

    Returns:
        sp2_centre_count: The number of sp2 stereocentres in the structure.
    """
    sp2_centre_count = 0
    # Split the inchi into layers.
    inchi_layers = inchi.split('/')
    # Collate the sp2 layers.
    sp2_layers = []
    for layer in inchi_layers:
        if layer.startswith('b'):
            sp2_layers.append(layer[1:])
    # If there are no sp2 layers, the molecule has no sp2 stereochemistry.
    if not sp2_layers:
        return sp2_centre_count
    for sp2_layer in sp2_layers:
        # Discard the "d" flag.
        sp2_layer = sp2_layer[1:]
        # Consider multi-component salts.
        sp2_layer_by_components = sp2_layer.split(';')
        for component in sp2_layer_by_components:
            # Components without stereochemistry will have empty stereolayers
            if component:
                sp2_centres = component.split(',')
                # Consider stoichiometry.
                multiplier = 1
                if component[1] == '*':
                    multiplier = int(component[0])
                for sp2_centre in sp2_centres:
                    # If wd is specified, only count those stereocentres which
                    # aren't "u" (undefined) or "?" (omitted).
                    if wd:
                        if sp2_centre[-1] not in 'u?':
                            sp2_centre_count += multiplier
                    else:
                        sp2_centre_count += multiplier
    return sp2_centre_count


def count_sp3(inchi, wd=False, enantio=False):
    """
    Count the number of sp3 stereocentres in a molecule.

    Args:
        inchi: An InChI
        wd: Whether or not the stereocentre must be well-defined to be counted.
        enantio: Whether or not the structure must be enantiopure to be counted.

    Returns:
        The number of sp3 stereocentres in the structure.
    """
    sp3_centre_count = 0
    # Split the inchi into layers
    inchi_layers = inchi.split('/')
    # Collate all the sp3 stereochemistry layers
    sp3_layers = []
    for index, layer in enumerate(inchi_layers):
        if layer.startswith('t'):
            stereolayer = [layer]
            try:
                if inchi_layers[index + 1].startswith('m'):
                    stereolayer.append(inchi_layers[index + 1])
                    try:
                        if inchi_layers[index + 2].startswith('s'):
                            stereolayer.append(inchi_layers[index + 2])
                    except IndexError:
                        pass
            except IndexError:
                pass
            try:
                if inchi_layers[index + 1].startswith('s'):
                    stereolayer.append(inchi_layers[index + 1])
            except IndexError:
                pass
            sp3_layers.append(stereolayer)
    # If there are no sp3_layers at all, then there is no sp3 stereochemistry.
    if not sp3_layers:
        return sp3_centre_count
    # If enantio is specified, check for '/s2' (relative stereochemistry) or
    # '/s3' (racemic) flags are present.  If either are, the sp3
    # stereochemistry is not enantiomeric.
    if enantio:
        for layer in sp3_layers:
            for sublayer in layer:
                if sublayer.startswith('s2') or sublayer.startswith('s3'):
                    return sp3_centre_count
    # If enantio is not specified (or if enantio is specified and there is no
    # "/s2" or "/s3" flag), count and return the stereocentres.
    for sp3_layer in sp3_layers:
        # Consider only the "/t" layer, and discard the "t" flag.
        t_layer = sp3_layer[0][1:]
        # Consider multi-component salts.
        t_layer_by_components = t_layer.split(';')
        for component in t_layer_by_components:
            # Components without stereochemistry will have empty stereolayers.
            if component:
                sp3_centres = component.split(',')
                # Consider stoichiometry.
                multiplier = 1
                if component[1] == '*':
                    multiplier = int(component[0])
                for sp3_centre in sp3_centres:
                    # If wd is specified, only count those stereocentres which
                    # aren't "u" (undefined) or "?" (omitted).
                    if wd:
                        if sp3_centre[-1] not in 'u?':
                            sp3_centre_count += multiplier
                    else:
                        sp3_centre_count += multiplier
    return sp3_centre_count


def count_centres(inchi, wd=False, sp2=True, sp3=True):
    """
    Counts the centres contained within an inchi

    Args:
        inchi: The InChI to search for the centres
        wd: Whether or not the stereocentre must be well-defined to be counted.
        sp2: Count sp2 centres
        sp3: Count sp3 centres

    Returns:
        stereocentres: The number of stereocentres
        stereo_mols: The number of molecules with stereocentres

    """
    stereocentres = 0
    stereo_mols = 0
    if sp2:
        stereocentres += count_sp2(inchi, wd)
    if sp3:
        stereocentres = count_sp3(inchi, wd)
    if stereocentres:
        stereo_mols = 1
    return stereocentres, stereo_mols


def inchi_2_auxinfo(inchi):
    """Run the InChI software on an InChI to generate AuxInfo.

    The function saves the InChI to a temporary file, and runs the inchi-1
    program on this tempfile as a subprocess.  The AuxInfo will not include
    2D coordinates, but an AuxInfo of some kind is required for the InChI
    software to convert an InChI to an SDFile.

    Args:
        inchi: An InChI from which to generate AuxInfo.

    Returns:
        auxinfo: The InChI's AuxInfo (will not contain 2D coordinates).
    """
    # Save the InChI to a temporary file.
    inchi_tempfile = tempfile.NamedTemporaryFile(delete=False)
    inchi_tempfile.write(bytes(inchi, 'UTF-8'))
    # A newline is required at the end of the file or the InChI program fails
    # to generate any output (this may be a bug).
    inchi_tempfile.write(bytes('\n', 'UTF-8'))
    inchi_tempfile.close()
    # Run the inchi-1 program, and extract the AuxInfo
    args = [external.INCHI_PATH, inchi_tempfile.name, '-stdio',
            '-InChI2Struct']
    raw_inchi_out, inchi_err = utils.call_command(args)
    os.unlink(inchi_tempfile.name)
    auxinfo = raw_inchi_out.splitlines()[2]
    return auxinfo


def inchi_2_sdf(inchi, auxinfo=""):
    """Run the InChI software on an InChI to output an SDF.

    The function works by saving the inchi and auxinfo strings to a tempfile,
    and running the inchi-1 program on this tempfile as a subprocess.

    If no AuxInfo is specified, it is created by the inchi-1 software and the
    SDF is generated as usual.  However, this SDF will not possess 2D
    coordinate data.

    Args:
        inchi: An InChI.
        auxinfo: The InChI's AuxInfo.

    Returns:
        sdf: The contents of an SDF as a string.
    """
    # Serve up an AuxInfo if one is not provided.
    if not auxinfo:
        auxinfo = inchi_2_auxinfo(inchi)

    # Save the InChI and AuxInfo to a temporary file.
    inchi_aux_file = tempfile.NamedTemporaryFile(delete=False)
    inchi_aux_file.write(bytes(inchi + '\n' + auxinfo, 'UTF-8'))
    inchi_aux_file.close()
    # Convert the InChI and AuxInfo file to an SDF
    args = [external.INCHI_PATH, inchi_aux_file.name, '-STDIO', '-NoLabels',
            '-OutputSDF']
    sdf_out, sdf_log = utils.call_command(args)
    # Delete the tempfile and return the SDF
    os.unlink(inchi_aux_file.name)
    return sdf_out


def molf_2_inchi(molf, return_auxinfo=False):
    """Run the InChI creation software on a molfile.

    The function works by saving the molfile string to a tempfile, and running
    the inchi-1 program on this tempfile as a subprocess.  It is assumed that
    the inchi-1 executable is in the current directory.

    In the future, this function might be better implemented without the need
    to write the molfile to a temp directory.  A python implementation of the
    inchi conversion software would allow this.

    Args:
        molf: The contents of a molfile as a string.
        return_auxinfo: If true, will generate AuxInfo for the InChI.

    Returns:
        inchi: The InChI.
        auxinfo: The InChI's AuxInfo, if required.  N.B.  If the inchi program fails to generate data,
        an empty string will be returned instead.
    """
    # Saves the molfile to a temporary file.
    molf_tempfile = tempfile.NamedTemporaryFile(delete=False)
    molf_tempfile.write(bytes(molf, 'UTF-8'))
    molf_tempfile.close()
    # Runs inchi-1 program on this molfile, and stores the output.
    inchi_args = [
        external.INCHI_PATH,
        molf_tempfile.name,
        '-STDIO',
        '-NoLabels']
    if not return_auxinfo:
        inchi_args.append('-AuxNone')
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
    if return_auxinfo:
        return inchi, auxinfo
    else:
        return inchi
