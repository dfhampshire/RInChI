#!/usr/bin/env python3
"""
RInChI conversion script

Converts RInChIs to and from various chemical reaction file formats.

    C. Allen 2012
    D.F. Hampshire 2016 - Code rewritten for Python 3 using the argparse module, and major structural and procedural
    changes.

"""

import argparse

from rinchi_tools import conversion, utils


def __rdf2rinchi(input_path, rauxinfo=False, longkey=False, shortkey=False, webkey=False, equilibrium=False,
                 file_out=False):
    """
    Called when -rdf2rinchi is given as the 1st argument of the script
    """
    try:
        rdf_file, input_name, _ = utils.read_input_file(input_path)
    except IOError:
        print('Could not open file "%s".' % input_path)
        return

    # Generate the requested data and convert to a string
    results = conversion.rdf_to_rinchis(rdf_file, 0, 0, equilibrium, rauxinfo, longkey, shortkey, webkey, False)
    rinchi_text = utils.construct_output_text(results)

    # Uses the output utility
    utils.output(rinchi_text, input_name, "rinchi", print_out= not file_out)


def __rxn2rinchi(input_path, ret_rauxinfo=False, longkey=False, shortkey=False, webkey=False, force_equilibrium=False,
                 file_out=False):
    """
    Called when -rxn2rinchi is given as the 1st argument of the script."""

    try:
        input_file, input_name, _ = utils.read_input_file(input_path)
    except IOError:
        print('Could not open file "%s".' % input_path)
        return

    # Generate the requested data.
    rinchi_text = utils.construct_output_text(conversion.rxn_to_rinchi(input_file, ret_rauxinfo, longkey, shortkey, webkey,
                                                                       force_equilibrium, file_out))
    # Uses the output utility
    utils.output(rinchi_text, input_name, "rinchi", print_out=not file_out)


def __rinchi2file(input_path, rxnout=True, file_out=True):
    """
    Called when -rinchi2rxn is given as the 1st argument of the script."""

    try:
        output, input_name, _ = utils.read_input_file(input_path, return_file_object=True)
    except IOError:
        print('Could not open file "%s".' % input_path)
        return

    if rxnout:
        filetype_args = "rxn"
    else:
        filetype_args = "rdf"

    filetext_list = conversion.rinchi_to_file(input_path, rxnout=rxnout)

    for filetext in filetext_list:
        utils.output(filetext, input_name, filetype_args, print_out=not file_out)


def __rinchi2key(input_path, longkey=False, shortkey=False, webkey=False, inc_rinchi=False, file_out=False):
    """
    Called when -rinchi2key is given as the 1st argument of the script."""

    try:
        input_file, input_name, _ = utils.read_input_file(input_path)
    except IOError:
        print('Could not open file "%s".' % input_path)
        return

    data = conversion.rinchi_to_keys(input_file, longkey, shortkey, webkey, inc_rinchi)
    key_text = utils.construct_output_text(data)
    utils.output(key_text,input_name,"rinchi",not file_out)


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
