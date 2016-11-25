#!/usr/bin/env python3

"""RInChI Conversion Script.

    Copyright 2016 D.F. Hampshire

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


This script is able to convert between RXNfiles, RDfiles and RInChIs.. It also
interfaces with the RInChI v0.03 software as provided by the InChI trust.

The RInChI library and programs are free software developed under the
auspices of the International Union of Pure and Applied Chemistry (IUPAC).


RXN-to-RInChI conversion:

    Invoked by having -rxn2rinchi as the script's first argument.

    Sample use:
        ./rinchi_convert.py -rxn2rinchi /some/path/myfile -options

    Options:
        -equilibrium
            Force output to be an equilibrium reaction
        -rauxinfo
            Generate and return RAuxInfo along with the RInChI.
        -longkey
            Generate and return the Long-RInChIKey along with the RInChI.
        -shortkey
            Generate and return the Short-RInChIKey along with the RInChI.
        -webkey
            Generate and return the Web-RInChIKey along with the RInChI.
        -fout
            Save the output to disk, rather than printing to the terminal.

RDF-to-RInChI conversion:

    Invoked by having -rdf2rinchi as the script's first argument.

    Sample use:
        ./rinchi_convert.py -rdf2rinchi /some/path/myfile -options

    Options:
        -equilibrium
            Force output to be an equilibrium reaction
        -rauxinfo
            Generate and return RAuxInfo along with the RInChI.
        -longkey
            Generate and return the Long-RInChIKey along with the RInChI.
        -shortkey
            Generate and return the Short-RInChIKey along with the RInChI.
        -webkey
            Generate and return the Web-RInChIKey along with the RInChI.
        -fout
            Save the output to disk, rather than printing to the terminal.


RInChI-to-File conversion:

    Invoked by having -rinchi2file as the script's first argument. Accepts
    any file containing a rinchi and optionally rauxinfo. Only if the rauxinfo
    is directly after a rinchi is it paired for the conversion process.

    Sample use:
        ./rinchi_convert.py -rinchi2file /some/path/myrinchi.rinchi -options

    Options:
        -stdout
            Print the file to the terminal, rather than saving to disk.

RInChi-to-Key conversion:

    Invoked by having -rinchi2key as the script's first argument.

    Sample use:
        ./rinchi_convert.py -rinchi2key /some/path/myrinchi.rinchi -options

    Options:
        -longkey
            Generate and return the Long-RInChIKey along with the RInChI.
        -shortkey
            Generate and return the Short-RInChIKey along with the RInChI.
        -webkey
            Generate and return the Web-RInChIKey along with the RInChI.
        -fout
            Save the output to disk, rather than printing to the terminal.
        -inc
            Include original RInChI in the output.
"""

import sys

from rinchi_tools import rinchi_lib, conversion, utils

rinchi_handle = rinchi_lib.RInChI()


def __rdf2rinchi(args):
    """Called when -rdf2rinchi is given as the 1st argument of the script."""
    if not args:
        print("Please specify an file for conversion.")
        return
        # Parse RDfile input.
    input_path = args[0]
    input_name = input_path.split('/')[-1].split('.')[0]
    try:
        input_file = open(input_path).read()
    except IOError:
        print('Could not open file "%s".' % input_path)
        return
    # Parse optional arguments
    return_rauxinfo = False
    return_longkey = False
    return_shortkey = False
    return_webkey = False
    force_equilibrium = False
    file_out = False
    for arg in args[1:]:
        if arg.startswith('-e'):
            force_equilibrium = True
        if arg.startswith('-r'):
            return_rauxinfo = True
        if arg.startswith('-l'):
            return_longkey = True
        if arg.startswith('-s'):
            return_shortkey = True
        if arg.startswith('-w'):
            return_webkey = True
        if arg.startswith('-f'):
            file_out = True

    # Generate the requested data.
    results = conversion.rdf_2_rinchis(
        input_file,
        0,
        0,
        force_equilibrium,
        return_rauxinfo,
        return_longkey,
        return_shortkey,
        return_webkey,
        False)

    # Construct output string
    rinchi_text = ''
    for entry in list(zip(*results)):

        read_index = 0  # Ensures correct element referencing
        rinchi_text += str(entry[read_index]) + '\n'
        read_index += 1
        if return_rauxinfo:
            rinchi_text += str(entry[read_index]) + '\n'
            read_index += 1
        if return_longkey:
            rinchi_text += str(entry[read_index]) + '\n'
            read_index += 1
        if return_shortkey:
            rinchi_text += str(entry[read_index]) + '\n'
            read_index += 1
        if return_webkey:
            rinchi_text += str(entry[read_index]) + '\n'
            read_index += 1

    # Uses the output utility
    utils.output(rinchi_text, not file_out, "rinchi", input_name)

    return


def __rxn2rinchi(args):
    """Called when -rxn2rinchi is given as the 1st argument of the script."""
    # Check that an file is given.
    if not args:
        print("Please specify an file for conversion.")
        return
        # Parse RXNfile input.
    input_path = args[0]
    input_name = input_path.split('/')[-1].split('.')[0]
    try:
        input_file = open(input_path).read()
    except IOError:
        print('Could not open file "%s".' % input_path)
        return
    # Parse optional arguments
    return_rauxinfo = False
    return_longkey = False
    return_shortkey = False
    return_webkey = False
    force_equilibrium = False
    file_out = False
    for arg in args[1:]:
        if arg.startswith('-e'):
            force_equilibrium = True
        if arg.startswith('-r'):
            return_rauxinfo = True
        if arg.startswith('-l'):
            return_longkey = True
        if arg.startswith('-s'):
            return_shortkey = True
        if arg.startswith('-w'):
            return_webkey = True
        if arg.startswith('-f'):
            file_out = True

    # Generate the requested data.
    rinchi, rauxinfo = rinchi_handle.rinchi_from_file_text(
        "RXN", input_file, force_equilibrium)

    rinchi_text = ''
    rinchi_text += rinchi + '\n'
    if return_rauxinfo:
        rinchi_text += rauxinfo + '\n'
    if return_longkey:
        rinchi_text += rinchi_handle.rinchikey_from_rinchi(rinchi, "L") + '\n'
    if return_shortkey:
        rinchi_text += rinchi_handle.rinchikey_from_rinchi(rinchi, "S") + '\n'
    if return_webkey:
        rinchi_text += rinchi_handle.rinchikey_from_rinchi(rinchi, "W") + '\n'

    # Uses the output utility
    utils.output(rinchi_text, not file_out, "rinchi", input_name)

    return


def __rinchi2file(args):
    """Called when -rinchi2rxn is given as the 1st argument of the script."""
    # Check that a RInChI file is given.
    if not args:
        print('Please specify a RInChI file for conversion.')
        return
    # Parse RInChI file input.
    input_path = args[0]
    input_name = input_path.split('/')[-1].split('.')[0]
    try:
        input_file = open(input_path)
    except IOError:
        print('Could not open file "%s".' % input_path)
        return
    input_rinchis = []
    input_rauxinfos = []
    rinchi_last = False  # Ensure rinchis are appended correctly

    for line in input_file.readlines():
        if line.startswith('RInChI'):
            input_rinchis.append(line.strip())
            if rinchi_last:
                input_rauxinfos.append("")
            rinchi_last = True
        elif line.startswith('RAux') and rinchi_last:
            input_rauxinfos.append(line.strip())
            rinchi_last = False

    while len(input_rinchis) > len(input_rauxinfos):
        input_rauxinfos.append("")

    input_file.close()
    # Parse optional arguments.
    std_out = False
    rxnout = True
    rdout = False
    for arg in args[1:]:
        if arg.startswith('-s'):
            std_out = True
        if arg.startswith('-rd'):
            rxnout = False
            rdout = True
        if arg.startswith('-rx'):
            rxnout = True

    # Generate RXN file.
    if rxnout:
        for index, rinchi_in in enumerate(input_rinchis):
            rxn = rinchi_handle.file_text_from_rinchi(
                rinchi_in, input_rauxinfos[index], "RXN")
            utils.output(rxn, std_out, "rxn", input_name)
    if rdout:
        for index, rinchi_in in enumerate(input_rinchis):
            rd = rinchi_handle.file_text_from_rinchi(
                rinchi_in, input_rauxinfos[index], "RD")
            utils.output(rd, std_out, "rdf", input_name)
    return


def __rinchi2key(args):
    """Called when -rinchi2key is given as the 1st argument of the script."""
    # Check that a RInChI file is given.
    if not args:
        print('Please specify a RInChI file for conversion.')
        return
    # Parse RInChI file input.
    input_path = args[0]
    input_name = input_path.split('/')[-1].split('.')[0]
    try:
        input_file = open(input_path)
    except IOError:
        print('Could not open file "%s".' % input_path)
        return
    input_rinchis = []
    input_rauxinfos = []
    rinchi_last = False
    # Ensure rinchis are appended correctly
    for line in input_file.readlines():
        if line.startswith('RInChI'):
            input_rinchis.append(line.strip())
            if rinchi_last:
                input_rauxinfos.append("")
            rinchi_last = True
        elif line.startswith('RAux') and rinchi_last:
            input_rauxinfos.append(line.strip())
            rinchi_last = False

    while len(input_rinchis) > len(input_rauxinfos):
        input_rauxinfos.append("")

    input_file.close()
    # Parse optional arguments.
    return_longkey = False
    return_shortkey = False
    return_webkey = False
    inc_rinchi = False
    file_out = False

    for arg in args[1:]:
        if arg.startswith('-l'):
            return_longkey = True
        if arg.startswith('-s'):
            return_shortkey = True
        if arg.startswith('-w'):
            return_webkey = True
        if arg.startswith('-f'):
            file_out = True
        if arg.startswith('-i'):
            inc_rinchi = True

    # Generate the requested data.
    rinchi_text = ''
    for index, rinchi_in in enumerate(input_rinchis):
        if inc_rinchi:
            rinchi_text += rinchi_in + '\n'
        if return_longkey:
            rinchi_text += rinchi_handle.rinchikey_from_rinchi(
                rinchi_in, "L") + '\n'
        if return_shortkey:
            rinchi_text += rinchi_handle.rinchikey_from_rinchi(
                rinchi_in, "S") + '\n'
        if return_webkey:
            rinchi_text += rinchi_handle.rinchikey_from_rinchi(
                rinchi_in, "W") + '\n'

    utils.output(rinchi_text, not file_out, "rinchi", input_name)
    return


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command_line_args = sys.argv[2:]
        if sys.argv[1] == '-rxn2rinchi':
            __rxn2rinchi(command_line_args)
        elif sys.argv[1] == '-rinchi2file':
            __rinchi2file(command_line_args)
        elif sys.argv[1] == '-rdf2rinchi':
            __rdf2rinchi(command_line_args)
        elif sys.argv[1] == '-rinchi2key':
            __rinchi2key(command_line_args)
        else:
            print('First argument must be one of:')
            print('-rxn2rinchi: To convert an RXNfile to a RInChI.')
            print('-rinchi2rxn: To convert a RInChI to an RXNfile.')
            print('-rdf2rinchi: To convert an RDfile to RInChI(s).')
            print('-rinchi2key: To convert a RInChI to an RInChI key.')
    else:
        print(__doc__)
