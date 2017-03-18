#!/usr/bin/env python3
"""
RInChI conversion script

Converts RInChIs to and from various chemical reaction file formats.

    C. Allen 2012
    D.F. Hampshire 2016 - Code rewritten for Python 3 using the argparse module, and major structural and procedural
    changes.

"""

import argparse
import os

from rinchi_tools import Reaction, conversion, utils


def convert_ops(args, parser):
    """
    Contains the operations for running the script

    Args:
        args: the args from the command line
        parser: the parser object
    """

    if args.filein:
        args.input, input_name, extension = utils.read_input_file(args.input)
    if args.rxn2rinchi:
        data = conversion.rxn_to_rinchi(args.input, force_equilibrium=args.equilibrium, ret_rauxinfo=args.rauxinfo,
                                        longkey=args.longkey, shortkey=args.shortkey, webkey=args.webkey)
        text = utils.construct_output_text(data)
        utils.output(text, args.fileout, ".rinchi")
    elif args.rdf2rinchi:
        data = conversion.rdf_to_rinchis(args.input, force_equilibrium=args.equilibrium, return_rauxinfos=args.rauxinfo,
                                         return_longkeys=args.longkey, return_shortkeys=args.shortkey,
                                         return_webkeys=args.webkey)
        text = utils.construct_output_text(data)
        utils.output(text, args.fileout, ".rinchi")
    elif args.rinchi2file:
        data = conversion.rinchi_to_file(args.input, args.rxnfileoutput)
        text = utils.construct_output_text(data)
        utils.output(text, args.fileout, '.rxn' if args.rxnfileoutput else '.rdf')
    elif args.rinchi2key:
        data = conversion.rinchis_to_keys(args.input, longkey=args.longkey, shortkey=args.shortkey, webkey=args.webkey,
                                          inc_rinchi=args.include_rinchi, inc_rauxinfo=args.rauxinfo)
        text = utils.construct_output_text(data)
        utils.output(text, args.fileout, ".rinchi")
    elif args.rdf2csv:
        if not args.fileout:
            parser.error('IOError - Fileout path required')
        if os.path.isfile(args.fileout):  # Append the file out if it exists
            conversion.rdf_to_csv_append(args.input, args.fileout)
        else:  # Otherwise create a file
            conversion.rdf_to_csv(args.input, args.fileout, return_rauxinfo=args.rauxinfo, return_longkey=args.longkey,
                                  return_shortkey=args.shortkey, return_webkey=args.webkey)
    elif args.dir2csv:
        if not args.fileout:
            parser.error('IOError - Fileout path required')
        conversion.create_csv_from_directory(args.input, args.fileout, return_rauxinfo=args.rauxinfo,
                                             return_longkey=args.longkey, return_shortkey=args.shortkey,
                                             return_webkey=args.webkey)
    elif args.svg:
        for rinchi in args.input.splitlines():
            if rinchi.startswith("RInChI="):
                r = Reaction(rinchi)
                r.generate_svg_image(os.path.splitext(args.fileout)[0])
    else:
        parser.print_help()


def add_convert(subparser):
    """
    Add the arguments for converting the files

    Args:
        subparser: The parser or subparser to add the argument to
    """

    assert isinstance(subparser, argparse.ArgumentParser)

    subparser.add_argument("input", help="The path of the file or folder to be converted, or the input string")

    # Add options for the type of conversion desired
    action = subparser.add_argument_group('Conversion Type').add_mutually_exclusive_group(required=True)
    action.add_argument("--rxn2rinchi", action="store_true", help="RXN to RInChI conversion")
    action.add_argument("--rdf2rinchi", action="store_true", help="RDF to RInChI conversion")
    action.add_argument("--rinchi2file", action="store_true",
                        help="RInChI-to-File conversion. Accepts any file containing a rinchi and optionally rauxinfo. "
                             "The RAuxInfo must immediately follow the RInChI")
    action.add_argument("--rinchi2key", action="store_true", help="RInChi to RInChI-Key conversion")
    action.add_argument('--rdf2csv', action='store_true', help='Create or append a .csv with an rdfile')
    action.add_argument('--dir2csv', action='store_true', help='Convert a directory of rdfiles to a single csv file')
    action.add_argument("--svg", action="store_true", help="Convert a RInChI to a collection of .svg files")

    # Add options for all commands
    opt_all = subparser.add_argument_group("All operations")
    opt_all.add_argument("-o", "--fileout", nargs='?', const='output', default=False, help="Save the output to disk. ")
    opt_all.add_argument('-i', '--filein', action='store_true', help='Assert that the input is a file')

    # Add options for converting to RInChI filetype
    opt_to_rinchi = subparser.add_argument_group("Conversion to RInChI file")
    opt_to_rinchi.add_argument("-e", "--equilibrium", action="store_true",
                               help="Force output to be an equilibrium reaction")
    opt_to_rinchi.add_argument("-ra", "--rauxinfo", action="store_true", help="Generate and return RAuxInfo")
    opt_to_rinchi.add_argument("-l", "--longkey", action="store_true",
                               help="Generate and return the Long-RInChIKey")
    opt_to_rinchi.add_argument("-s", "--shortkey", action="store_true",
                               help="Generate and return the Short-RInChIKey")
    opt_to_rinchi.add_argument("-w", "--webkey", action="store_true",
                               help="Generate and return the Web-RInChIKey")

    # Add options for converting to Keys
    opt_to_key = subparser.add_argument_group("Converting RInChIs to Keys")
    opt_to_key.add_argument("-r", "--include_rinchi", action="store_true", help="Include original RInChI in the output")

    # Add options for converting to RXN/RDF. n.b the order of the 2nd and 3rd statements IS important!
    opt_to_file = subparser.add_argument_group("Converting to a RXN/RDF")
    opt_to_file.add_argument("-ordf", "--rdfileoutput", action="store_false", dest='rxnfileoutput',
                             help="Output as RDFile. Otherwise RXN file(s) are produced")
    opt_to_file.add_argument("-orxn", '--rxnfileoutput', action="store_true",
                             help="Output as RXNFile")


if __name__ == "__main__":
    role = "RInChI Conversion tools"
    parser = argparse.ArgumentParser(description=role)
    add_convert(parser)
    args = parser.parse_args()
    convert_ops(args, parser)
