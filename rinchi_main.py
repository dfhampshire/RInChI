#!/usr/bin/env python3
"""
RInChI Object Orientated Script. Deprecated

Performs various tasks using functions structure in an Object Orientated manner in the reaction.py, molecule.py,
and atom.py module.

    B. Hammond 2014
    D. Hampshire 2016 - Restructuring of module and class, feature fixing and simplifying.
"""

import argparse

from rinchi_tools.molecule import Molecule
from rinchi_tools.reaction import Reaction

# TODO simplify and test this.  PHP web implementation checked and re-made

args = argparse.ArgumentParser().parse_args()

if args.svg:
    r = Reaction(args.input)
    r.generate_svg_image(args.arg2)
elif args.reactionsearch:
    r = Reaction(args.input)
    print(r.detect_reaction(hyb_i={"sp3": 2}))
elif args.fingerprint:
    r = Reaction(args.input)
    r.calculate_reaction_fingerprint()
    print(repr(r.reaction_fingerprint).replace(" ", ""))
elif args.isotopic:
    r = Reaction(args.input)
    i = r.present_in_reaction(Molecule.has_isotopic_layer)
    if i:
        print(i)
