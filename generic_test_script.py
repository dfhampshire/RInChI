# !/usr/bin/env python3
"""
Script used to test various the module during development.  Not for general distribution.  Successful code is
implemented elsewhere.

    Duncan Hampshire 2017
"""
import cProfile

from rinchi_tools.matcher import Matcher
from rinchi_tools.molecule import Molecule


def test():
    m = Molecule('InChI=1S/C30H18O4/c31-25-21-15-7-8-16-22(21)26(32)29(25,19-11-3-1-4-12-19)30(20-13-5-2-6-14-20)27(33)23-17-9-10-18-24(23)28(30)34/h1-18H')

    p = Molecule('InChI=1S/C9H6O2/c10-8-5-9(11)7-4-2-1-3-6(7)8/h1-4H,5H2')
    mt = Matcher(p,m)
    matcher = mt.match()
    print(next(matcher))

cProfile.run('test()')