# !/usr/bin/env python3
"""
Script used to test various the module during development.  Not for general distribution.  Successful code is
implemented elsewhere.

    Duncan Hampshire 2017
"""

from rinchi_tools import database


def test():
    e = 'InChI=1S/C2H4O/c1-2-3/h2H,1H3'
    c = 'InChI=1S/C3H6O2/c4-2-1-3-5/h2,5H,1,3H2'
    for i in database.search_for_roles('database/rinchi.db','rinchis03',product_subs=(c,),reactant_subs=(e,),limit=20000):
        print(i)
    #todo randomize

test()