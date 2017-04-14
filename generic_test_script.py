#!/usr/bin/env python3
"""
Script used to test various the module during development.  Not for general distribution.  Successful code is
implemented elsewhere.

    Duncan Hampshire 2017
"""

import time

from rinchi_tools import database, utils


def get_aldols():
    tstart = time.time()
    e = 'InChI=1S/C2H4O/c1-2-3/h2H,1H3'
    c = 'InChI=1S/C4H8O2/c1-4(6)2-3-5/h3-4,6H,2H2,1H3'
    d = 'InChI=1S/C6H12O/c1-4-6(3)5(2)7-6/h5H,4H2,1-3H3/t5-,6-/m0/s1'
    r = 'InChI=1S/C10H8/c1-2-6-10-8-4-3-7-9(10)5-1/h1-8H'
    m = 'InChI=1S/3C4H12N.6CN.Fe/c3*1-5(2,3)4;6*1-2;/h3*1-4H3;;;;;;;/q3*+1;6*-1;+3'
    #c1 = Molecule(m)
    #print(c1.get_ring_count())
    #print(vars(c1))
    #r = Reaction('RInChI=0.03.1S/C16H19ClSi/c1-16(2,3)18(17,14-10-6-4-7-11-14)15-12-8-5-9-13-15/h4-13H,1-3H3!C3H4N2/c1-2-5-3-4-1/h1-3H,(H,4,5)!C5H9NO2/c7-4-1-2-6-5(8)3-4/h4,7H,1-3H2,(H,6,8)<>C21H27NO2Si/c1-21(2,3)25(18-10-6-4-7-11-18,19-12-8-5-9-13-19)24-17-14-15-22-20(23)16-17/h4-13,17H,14-16H2,1-3H3,(H,22,23)<>C3H7NO/c1-4(2)3-5/h3H,1-2H3!H2O/h1H2/d+')
    #print(Matcher(e,c).sub_count())
    #print(r.has_substructures(reactant_subs=(e,e),product_subs=(c,)))
    file, path = utils.create_output_file('aldols','.rinchi')
    for i in database.search_for_roles('database/rinchi.db','rinchis03', product_subs=(c,), reactant_subs=(e,),limit=2000):
        file.write(i + '\n')
    print("Finished in {}".format(time.strftime("%H:%M:%S", time.gmtime(time.time()-tstart))))

if __name__ == "__main__":
    get_aldols()