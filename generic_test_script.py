#!/usr/bin/env python3
"""
Script used to test various the module during development.  Not for general distribution.  Successful code is
implemented elsewhere.

    Duncan Hampshire 2017
"""

import time

from rinchi_tools import RInChI, Reaction, conversion, database, utils, v02_rinchi_key


def get_aldols():
    tstart = time.time()
    e = 'InChI=1S/C2H4O/c1-2-3/h2H,1H3'
    c = 'InChI=1S/C4H8O2/c1-4(6)2-3-5/h3-4,6H,2H2,1H3'
    #m = Molecule.composite_inchi_to_simple('InChI=1S/3C4H12N.6CN.Fe/c3*1-5(2,3)4;6*1-2;/h3*1-4H3;;;;;;;/q3*+1;6*-1;+3')
    #r = Reaction('RInChI=0.03.1S/C15H10BrNO3S2/c16-11-5-7-12(8-6-11)17-22(19,20)14-9-10-3-1-2-4-13(10)21-15(14)18/h1-9,17H!C15H10ClFN2O3S2/c16-9-2-1-8-5-14(15(20)23-13(8)6-9)24(21,22)19-10-3-4-11(17)12(18)7-10/h1-7,19H,18H2!C15H9Br2NO3S2/c16-10-4-6-11(7-5-10)18-23(20,21)13-8-9-2-1-3-12(17)14(9)22-15(13)19/h1-8,18H!C15H9BrClNO3S2/c16-10-2-5-12(6-3-10)18-23(20,21)14-7-9-1-4-11(17)8-13(9)22-15(14)19/h1-8,18H!C15H9BrClNO3S2/c16-10-4-6-11(7-5-10)18-23(20,21)13-8-9-2-1-3-12(17)14(9)22-15(13)19/h1-8,18H!C16H12BrNO4S2.C16H12ClNO4S2/c2*1-22-13-5-3-12(4-6-13)18-24(20,21)15-9-10-8-11(17)2-7-14(10)23-16(15)19/h2*2-9,18H,1H3!C16H12BrNO4S2/c1-22-13-6-7-14-10(8-13)9-15(16(19)23-14)24(20,21)18-12-4-2-11(17)3-5-12/h2-9,18H,1H3!C16H12ClNO4S2/c1-22-13-6-4-12(5-7-13)18-24(20,21)15-8-10-2-3-11(17)9-14(10)23-16(15)19/h2-9,18H,1H3!C16H12ClNO5S2/c1-23-13-4-3-11(8-12(13)19)18-25(21,22)15-7-9-6-10(17)2-5-14(9)24-16(15)20/h2-8,18-19H,1H3!C16H12ClNO5S2/c1-23-13-5-4-11(8-12(13)19)18-25(21,22)15-6-9-2-3-10(17)7-14(9)24-16(15)20/h2-8,18-19H,1H3!C16H13FN2O4S2/c1-23-11-3-5-14-9(6-11)7-15(16(20)24-14)25(21,22)19-10-2-4-12(17)13(18)8-10/h2-8,19H,18H2,1H3!C16H13NO5S2/c1-22-13-7-6-11(9-12(13)18)17-24(20,21)15-8-10-4-2-3-5-14(10)23-16(15)19/h2-9,17-18H,1H3!C17H15FN2O4S2/c1-2-24-14-5-3-4-10-8-15(17(21)25-16(10)14)26(22,23)20-11-6-7-12(18)13(19)9-11/h3-9,20H,2,19H2,1H3!C18H17NO5S2/c1-3-24-15-6-4-5-12-11-16(18(20)25-17(12)15)26(21,22)19-13-7-9-14(23-2)10-8-13/h4-11,19H,3H2,1-2H3<>C16H13NO4S2/c1-21-13-8-6-12(7-9-13)17-23(19,20)15-10-11-4-2-3-5-14(11)22-16(15)18/h2-10,17H,1H3/d+')
    #print(Matcher(e,c).sub_count())
    #print(r.has_substructures(reactant_subs=(e,e),product_subs=(c,)))
    file, path = utils.create_output_file('aldols','.rinchi')
    for i in database.search_for_roles('database/rinchi.db','rinchis03', product_subs=(c,), reactant_subs=(e,),limit=0):
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

if __name__ == "__main__":
    #get_aldols()
    #print(timeit.timeit('test4()',"from __main__ import test4",number=10000))
    #print(timeit.timeit('test3()',"from __main__ import test3",number=10000))
    test5()