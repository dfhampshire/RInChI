#!/usr/bin/env python3
"""
Script used to test various the module during development.  Not for general distribution.  Successful code is
implemented elsewhere.

    Duncan Hampshire 2017
"""

import time, os

from rinchi_tools import RInChI, Reaction, conversion, database, utils, v02_rinchi_key, Molecule


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


def test():
    r = 'RInChI=0.03.1S/C4H8O/c1-3-4(2)5-3/h3-4H,1-2H3/t3-,4?/m0/s1<>C4H9BrO/c1-3(5)4(2)6/h3-4,6H,1-2H3/t3-,4+/m1/s1!Na.H2O/h;1H2/q+1;/p-1/d-'
    print(Reaction(r).generate_svg_image("letsgo"))

def test2():
    with open("tester",mode="w+b") as f:
        f.write(bytes("InChI=1S/C6H12/c1-4-6(3)5-2/h4H,5H2,1-3H3\n",encoding="utf-8"))
        i_out, i_err = utils.call_command(["obabel", "-iinchi", f.name, "-osvg", "-xd", "-xC", "-xj", "-xr 1"])
        print(i_err)
        print(i_out)

def test3():
    r = RInChI().rinchikey_from_rinchi("RInChI=0.03.1S/C4H8O/c1-3-4(2)5-3/h3-4H,1-2H3/t3-,4?/m0/s1<>C4H9BrO/c1-3(5)4(2)6/h3-4,6H,1-2H3/t3-,4+/m1/s1!Na.H2O/h;1H2/q+1;/p-1/d-","L")

def test4():
    r = v02_rinchi_key.rinchi_2_longkey("RInChI=0.02.1S/C4H8O/c1-3-4(2)5-3/h3-4H,1-2H3/t3-,4?/m0/s1///C4H9BrO/c1-3(5)4(2)6/h3-4,6H,1-2H3/t3-,4+/m1/s1//Na.H2O/h;1H2/q+1;/p-1/d-")


def test5():
    rdf = open('../newdata/I20160830.rdf').read()
    csv = 'test-resources/test.csv'
    conversion.rdf_to_csv_append(rdf,csv)

def test6():
    root_dir = "../newdata"
    for root, folders, filenames in os.walk(root_dir):
        lister = filenames[2854:]
        for i in lister:
            path = root+'/'+i
            dest = root + '/todo' + i
            os.rename(path,dest)

if __name__ == "__main__":
    #get_aldols()
    #print(timeit.timeit('test4()',"from __main__ import test4",number=10000))
    #print(timeit.timeit('test3()',"from __main__ import test3",number=10000))
    get_aldols()