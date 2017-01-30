"""
RInChI test module.

    2016 D.F. Hampshire

This module tests the module functions. Not very user friendly...

The RInChI library and programs are free software developed under the
auspices of the International Union of Pure and Applied Chemistry (IUPAC).

"""

from rinchi_tools import tools, rinchi_lib, inchi_tools, conversion, analysis

rinchi_interface = rinchi_lib.RInChI()

print("\n\n\n========Start Test!========\n================")

# Test addition.py
# Define an arbitrary (and impossible!) three step reaction, inchis names
# "AAA" , "BBB" etc.
three_reactions = ("RInChI=0.03.1S/AAA<>BBB!CCC/d-", "RInChI=0.03.1S/AAA<>DDD/d+", "RInChI=0.03.1S/DDD<>EEE!FFF/d=")
three_reactions_unknown = (
    "RInChI=0.03.1S/AAA<>BBB!CCC/d-/u1-0-0", "RInChI=0.03.1S/AAA<>DDD/d+", "RInChI=0.03.1S/DDD<>EEE!FFF/d+")
# Define an arbitrary (and impossible!) three step reaction, inchis names "AAA" , "BBB" etc. but with unknown structures
# Print results
print(tools.add(three_reactions))
try:
    print(tools.add(three_reactions_unknown))
except tools.Error:
    print("Addition Error raised successfully")
print("================")

# Test analysis.py
test_inchi = "InChI=1S/C6H12O/c1-4-6(3)5(2)7-6/h5H,4H2,1-3H3/t5-,6-/m0/s1"
test_rinchi = ("RInChI=0.03.1S/H2O/h1H2/p-1!C6H12O/c1-4-6(3)5(2)7-6/h5H,4H2,1-3H3/t5-,6-/m0/s1<>C6H14O2/c1-4-6(3,8)5(2)"
               "7/h5,7-8H,4H2,1-3H3/t5-,6+/m1/s1/d-")
test_list_rinchi = [test_rinchi, test_rinchi]
sp2_centre_inchi = "InChI=1S/C4H8/c1-3-4-2/h3-4H,1-2H3/b4-3+"
sp2_centre_rinchi = ("RInChI=0.03.1S/C4H8/c1-3-4-2/h3-4H,1-2H3/b4-3+!C2H6O/c1-2-3/h3H,2H2,1H3<>C4H8O2/c1-3-6-4(2)5/h3H2"
                     ",1-2H3!H2O/h1H2<>H2O4S/c1-5(2,3)4/h(H2,1,2,3,4)/d=")
print(inchi_tools.get_conlayer(test_inchi))
print(inchi_tools.count_rings(test_inchi))
print(analysis.rxn_ring_change(test_rinchi, (False, False), False))
print(analysis.rxn_ring_change(test_rinchi, (False, False), True))
print(analysis.rxn_ring_change(test_rinchi, (True, False), False))
print(analysis.rxn_ring_change(test_rinchi, (True, True), False))
print(analysis.rxns_ring_changes(test_list_rinchi))
print(inchi_tools.count_sp2(sp2_centre_inchi))
print(inchi_tools.count_sp3(test_inchi))
print(analysis.rxn_stereochem_change(test_rinchi))
print(analysis.rxns_stereochem_changes(test_list_rinchi))
print(analysis.search_4_inchi(test_inchi, [test_rinchi]))
print("================")

# Test Conversion.py
print(inchi_tools.inchi_2_auxinfo(test_inchi))
with open('test-resources/rxn_t1.rxn', 'r') as myfile:
    rxn = myfile.read()
molfs = conversion.rxn_2_molfs(rxn)
print(molfs)
print(conversion.molfs_2_rxn(*molfs))
print(inchi_tools.molf_2_inchi(molfs[0][0]))
print(inchi_tools.inchi_2_sdf(test_inchi))

print("================")
# Test tools.py
# build_rinchi implicitly tested in the addition section
test_rinchi2 = ("RInChI=0.03.1S/C2H4O2/c1-2(3)4/h1H3,(H,3,4)!C2H6O/c1-2-3/h3H,2H2,1H3<>C4H8O2/c1-3-6-4(2)5/h3H2,1-2H3!H"
                "2O/h1H2<>H2O4S/c1-5(2,3)4/h(H2,1,2,3,4)/d-")
test_rauxinfo2 = ("RAuxInfo=0.03.1/1/N:1,2,3,4/E:(3,4)/rA:4nCCOO/rB:s1;s2;d2;/rC:-3.8549,-.5552,0;-2.8321,.0354,0;-2.83"
                  "21,1.2168,0;-1.8089,-.5554,0;!0/N:3,2,1/rA:3nOCC/rB:s1;s2;/rC:2.499,-.1614,0;1.4762,.4292,0;.453,-.1"
                  "615,0;<>0/N:5,1,4,2,6,3/rA:6nCCOCCO/rB:s1;s2;s3;s4;d2;/rC:7.2384,-1.0475,0;8.2613,-.4569,0;8.2613,.7"
                  "246,0;9.2844,1.3153,0;10.3076,.7246,0;9.2844,-1.0476,0;!0/N:1/rA:1nO/rB:/rC:12.5696,.0354,0;<>1/N:2,"
                  "3,4,5,1/E:(1,2,3,4)/CRV:5.6/rA:5nSOOOO/rB:s1;s1;d1;d1;/rC:6.4257,-2.7792,0;7.1757,-2.7792,0;5.6757,-"
                  "2.7792,0;6.4257,-3.5292,0;6.4257,-2.0292,0;")
print(test_rinchi2, tools.split_rinchi_inc_auxinfo(test_rinchi2, test_rauxinfo2))
print("@@@@@@@@@@@@@@@@@@@")
print(test_rinchi, tools.split_rinchi(test_rinchi))
print(tools.split_rinchi_only_auxinfo(test_rinchi2, test_rauxinfo2))
print("================")
print(tools.gen_rauxinfo(test_rinchi2))
print(test_rauxinfo2)
print("================")
print(tools.build_rinchi_rauxinfo(*tools.split_rinchi_inc_auxinfo(test_rinchi2, test_rauxinfo2)))
input_file = open("test-resources/test.rdf").read()
print(rinchi_interface.rinchi_from_file_text("RD", input_file, False))
deduper_test = ("RInChI=0.03.1S/C2H4O2/c1-2(3)4/h1H3,(H,3,4)!C2H4O2/c1-2(3)4/h1H3,(H,3,4)!C2H6O/c1-2-3/h3H,2H2,1H3<>C4H"
                "8O2/c1-3-6-4(2)5/h3H2,1-2H3!H2O/h1H2<>H2O4S/c1-5(2,3)4/h(H2,1,2,3,4)/d=")
dedup_raux = ("RAuxInfo=0.03.1/1/N:1,2,3,4/E:(3,4)/rA:4nCCOO/rB:s1;s2;d2;/rC:-3.8549,-.5552,0;-2.8321,.0354,0;-2.8321,1"
              ".2168,0;-1.8089,-.5554,0;!1/N:1,2,3,4/E:(3,4)/rA:4nCCOO/rB:s1;s2;d2;/rC:-3.8549,-.5552,0;-2.8321,.0354,0"
              ";-2.8321,1.2168,0;-1.8089,-.5554,0;!0/N:3,2,1/rA:3nOCC/rB:s1;s2;/rC:2.499,-.1614,0;1.4762,.4292,0;.453,-"
              ".1615,0;<>0/N:5,1,4,2,6,3/rA:6nCCOCCO/rB:s1;s2;s3;s4;d2;/rC:7.2384,-1.0475,0;8.2613,-.4569,0;8.2613,.724"
              "6,0;9.2844,1.3153,0;10.3076,.7246,0;9.2844,-1.0476,0;!0/N:1/rA:1nO/rB:/rC:12.5696,.0354,0;<>1/N:2,3,4,5,"
              "1/E:(1,2,3,4)/CRV:5.6/rA:5nSOOOO/rB:s1;s1;d1;d1;/rC:6.4257,-2.7792,0;7.1757,-2.7792,0;5.6757,-2.7792,0;6"
              ".4257,-3.5292,0;6.4257,-2.0292,0;")
print("====\n", rinchi_interface.inchis_from_rinchi(deduper_test, dedup_raux), "\n====")
print(tools.deduper(deduper_test, dedup_raux))

print("Test Completed!")
