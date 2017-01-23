#!/usr/bin/env python3
"""
RInChI Conversion Script.

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
"""

import argparse

from rinchi_tools import rinchi_lib, conversion, utils

rinchi_handle = rinchi_lib.RInChI()


def __rdf2rinchi(input_path, rauxinfo=False, longkey=False, shortkey=False, webkey=False, equilibrium=False,
                 fileout=False):
    """Called when -rdf2rinchi is given as the 1st argument of the script."""
    input_name = input_path.split('/')[-1].split('.')[0]
    try:
        input_file = open(input_path).read()
    except IOError:
        print('Could not open file "%s".' % input_path)
        return

    # Generate the requested data.
    results = conversion.rdf_2_rinchis(input_file, 0, 0, equilibrium, rauxinfo, longkey, shortkey, webkey, False)
    rinchi_text = ""
    # Construct output string
    for entry in list(zip(*results)):
        for item in entry:
            rinchi_text += str(item)
            # Uses the output utility
    utils.output(rinchi_text, not fileout, "rinchi", input_name)

    return


def __rxn2rinchi(input_path, ret_rauxinfo=False, longkey=False, shortkey=False, webkey=False, force_equilibrium=False,
                 file_out=False):
    """Called when -rxn2rinchi is given as the 1st argument of the script."""
    input_name = input_path.split('/')[-1].split('.')[0]

    try:
        input_file = open(input_path).read()
    except IOError:
        print('Could not open file "%s".' % input_path)
        return

    # Generate the requested data.
    rinchi, rauxinfo = rinchi_handle.rinchi_from_file_text("RXN", input_file, force_equilibrium)
    rinchi_text = ''
    rinchi_text += rinchi + '\n'
    if ret_rauxinfo:
        rinchi_text += rauxinfo + '\n'
    if longkey:
        rinchi_text += rinchi_handle.rinchikey_from_rinchi(rinchi, "L") + '\n'
    if shortkey:
        rinchi_text += rinchi_handle.rinchikey_from_rinchi(rinchi, "S") + '\n'
    if webkey:
        rinchi_text += rinchi_handle.rinchikey_from_rinchi(rinchi, "W") + '\n'
    # Uses the output utility
    utils.output(rinchi_text, not file_out, "rinchi", input_name)
    return


def __rinchi2file(input_path, rxnout=True, rdout=False, fileout=True):
    """Called when -rinchi2rxn is given as the 1st argument of the script."""
    # Parse RInChI file input.
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

    # Generate RXN file.
    if rxnout or not (rxnout or rdout):
        for index, rinchi_in in enumerate(input_rinchis):
            rxn = rinchi_handle.file_text_from_rinchi(rinchi_in, input_rauxinfos[index], "RXN")
            utils.output(rxn, not fileout, "rxn", input_name)
    if rdout:
        for index, rinchi_in in enumerate(input_rinchis):
            rd = rinchi_handle.file_text_from_rinchi(rinchi_in, input_rauxinfos[index], "RD")
            utils.output(rd, not fileout, "rdf", input_name)
    return


def __rinchi2key(input_path, longkey=False, shortkey=False, webkey=False, inc_rinchi=False, file_out=False):
    """Called when -rinchi2key is given as the 1st argument of the script."""
    # Parse RInChI file input.
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

    # Generate the requested data.
    rinchi_text = ''
    for index, rinchi_in in enumerate(input_rinchis):
        if inc_rinchi:
            rinchi_text += rinchi_in + '\n'
        if longkey:
            rinchi_text += rinchi_handle.rinchikey_from_rinchi(rinchi_in, "L") + '\n'
        if shortkey:
            rinchi_text += rinchi_handle.rinchikey_from_rinchi(rinchi_in, "S") + '\n'
        if webkey:
            rinchi_text += rinchi_handle.rinchikey_from_rinchi(rinchi_in, "W") + '\n'

    utils.output(rinchi_text, not file_out, "rinchi", input_name)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RInChI Conversion tools \n{}".format(__doc__))
    parser.add_argument("inputpath", help="The path of the file to be converted")
    action = parser.add_argument_group('Main Arguments',
                                       'Choose an argument from those below.').add_mutually_exclusive_group(
        required=True)
    action.add_argument("-rx", "--rxn2rinchi", action="store_true", help="RXN to RInChI conversion")
    action.add_argument("-rd", "--rdf2rinchi", action="store_true", help="RDF-to-RInChI conversion")
    action.add_argument("-ri", "--rinchi2file", action="store_true",
                        help="RInChI-to-File conversion. Accepts any file containing a rinchi and optionally rauxinfo. "
                             "Only if the rauxinfo is directly after a rinchi is it paired for the conversion process.")
    action.add_argument("-k", "--rinchi2key", action="store_true", help="RInChi-to-Key conversion")
    optional = parser.add_argument_group("Optional Arguments", "n.b. Some arguments only apply to certain operations.")
    optional.add_argument("-e", "--equilibrium", action="store_true", help="Force output to be an equilibrium reaction")
    optional.add_argument("-ra", "--rauxinfo", action="store_true", help="Generate and return RAuxInfo")
    optional.add_argument("-l", "--longkey", action="store_true",
                          help="Generate and return the Long-RInChIKey along with the RInChI")
    optional.add_argument("-s", "--shortkey", action="store_true",
                          help="Generate and return the Short-RInChIKey along with the RInChI")
    optional.add_argument("-w", "--webkey", action="store_true",
                          help="Generate and return the Web-RInChIKey along with the RInChI")
    optional.add_argument("-f", "--fileout", action="store_true", help="Save the output to disk")
    optional.add_argument("-i", "--include", action="store_true", help="Include original RInChI in the output")
    optional.add_argument("-rdo", "--rdfileoutput", action="store_true", help="Output as RDFile")
    optional.add_argument("-ro", "--rxnoutput", action="store_true", help="Output as RXN file(s)")
    args = parser.parse_args()

    if args.rxn2rinchi:
        __rxn2rinchi(args.inputpath, args.rauxinfo, args.longkey, args.shortkey, args.webkey, args.equilibrium,
                     args.fileout)
    elif args.rdf2rinchi:
        __rdf2rinchi(args.inputpath, args.rauxinfo, args.longkey, args.shortkey, args.webkey, args.equilibrium,
                     args.fileout)
    elif args.rinchi2file:
        __rinchi2file(args.inputpath, args.rxnoutput, args.rdfileoutput, args.fileout)
    elif args.rinchi2key:
        __rinchi2key(args.inputpath, args.longkey, args.shortkey, args.webkey, args.include, args.fileout)
    else:
        parser.print_help()
