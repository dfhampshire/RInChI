# !/usr/bin/env python3
"""
Script used to test various the module during development.  Not for general distribution.  Successful code is
implemented elsewhere.

    Duncan Hampshire 2017
"""

from rinchi_tools.matcher import Matcher
from rinchi_tools.molecule import Molecule


def test():
    m = Molecule('InChI=1S/C30H18O4/c31-25-21-15-7-8-16-22(21)26(32)29(25,19-11-3-1-4-12-19)30(20-13-5-2-6-14-20)27(33)23-17-9-10-18-24(23)28(30)34/h1-18H')

    p = Molecule('InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3')
    mt = Matcher(p,m)
    print(mt.is_sub())

