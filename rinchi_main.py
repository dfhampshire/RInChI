#!/usr/bin/env python3

"""
New Object Orientated Python Scripts

B. Hammond 2014
D. Hampshire 2016
"""

import argparse
from collections import Counter

import scipy.cluster as cluster
from numpy import array, all, equal, rot90
from scipy.spatial import distance

import rinchi_tools.reaction
from rinchi_tools import analysis

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A collection of RInChI Tools - Benjamin Hammond 2014")

    parser.add_argument("input", help="The file or string to be processed")
    parser.add_argument("arg2", nargs="?", help="optional arg 2")

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('-i', '--inchi', action='store_true', help='Process a single InChI')
    action.add_argument('-r', '--rinchi', action='store_true', help='Process a single RInChI')
    action.add_argument('-b', '--batch', action='store_true', help='Process a database of RInChIs')
    action.add_argument('-c', "--clusters", action="store_true", help="Test post please ignore")
    action.add_argument('-t', "--test", action="store_true", help="Test post please ignore")

    parser.add_argument("--key", action="store_true", help="")
    parser.add_argument("--ringcount", action="store_true", help="Calculate the number or change in rings")
    parser.add_argument("--ringsearch", action="store_true",
                        help="Search a collection of RInChIs for a specific ring type, ")
    parser.add_argument("--formula", action="store_true", help="Calculate the change in formula across a reaction")
    parser.add_argument("--isotopic", action="store_true",
                        help="Search for reactions containing defined isotopic layers")
    parser.add_argument("--svg", action="store_true", help="Convert a RInChI to a collection of .svg files")
    parser.add_argument("--valence", action="store_true", help="Change in valence across reaction")
    parser.add_argument("--hybrid", action="store_true", help="Change in hybridisation of C atoms across reaction")
    parser.add_argument("--reactionsearch", action="store_true", help="Search for reaction")
    parser.add_argument("--ringelements", action="store_true", help="Search for reaction")
    parser.add_argument("--quick", action="store_true", help="Speed up search at cost of accuracy")
    parser.add_argument("--list", action="store_true", help="List RInChIs along with results")
    parser.add_argument("--fingerprint", action="store_true", help="Test post please ignore")

    args = parser.parse_args()

    print(args.arg2, args.input)

    try:
        if args.key and args.input.startswith("Long-RInChIKey"):
            args.input = rinchi_tools.database.sql_key_to_rinchi(args.input, "rinchi.db")
    except ValueError:
        print("Could not find Long-RInChIKey in database")
        pass

    if args.inchi:
        # If supplied a single inchi, perform a ring count
        mol = rinchi_tools.molecule.Molecule.new(args.input)
        for m in mol:
            m.calculate_rings()
            print(m.ring_count)

    elif args.rinchi:
        if args.ringcount:
            r = rinchi_tools.reaction.Reaction(args.input)
            print(r.change_across_reaction(r.ring_count))
        elif args.formula:
            r = rinchi_tools.reaction.Reaction(args.input)
            print(r.change_across_reaction(r.formula))
        elif args.svg:
            r = rinchi_tools.reaction.Reaction(args.input)
            r.generate_svg_image(args.arg2)
        elif args.reactionsearch:
            r = rinchi_tools.reaction.Reaction(args.input)
            print(r.detect_reaction(hyb_i={"sp3": 2}))
        elif args.fingerprint:
            r = rinchi_tools.reaction.Reaction(args.input)
            r.calculate_reaction_fingerprint()
            print(repr(r.reaction_fingerprint).replace(" ", ""))
    elif args.reactionsearch:
        counter = 0
        with open(args.input) as data:
            for rin in data:
                try:
                    r = rinchi_tools.reaction.Reaction(rin)
                    if r.detect_reaction(hyb_i={"sp2": -4, "sp3": 4}, rings_i={6: 1}):
                        print(counter, r.rinchi)
                    counter += 1
                except ValueError:
                    print("ERROR", rin)

    elif args.test:
        r1 = rinchi_tools.reaction.Reaction(args.input)
        r1.calculate_reaction_fingerprint()
        sparseness = []

        counter = 1
        with open(args.arg2) as data:
            for rin in data:
                r2 = rinchi_tools.reaction.Reaction(rin)
                r2.calculate_reaction_fingerprint()
                sparseness.append(1024 - len([i for i in r2.reaction_fingerprint if not i]))

                print(counter, distance.euclidean(r1.reaction_fingerprint, r2.reaction_fingerprint))
                counter += 1
        print("Number of non-zero fingerprint entries", sparseness)
        print("Average", sum(sparseness) / len(sparseness))
    elif args.clusters:
        arr = []
        with open(args.input) as data:
            for rin in data:
                r = rinchi_tools.reaction.Reaction(rin)
                r.calculate_reaction_fingerprint()

                arr.append(r.reaction_fingerprint.toarray()[0])

        arr = array(arr)

        arr90 = rot90(arr)
        arr = rot90(arr90[~all(equal(arr90, 0), axis=1)])

        cluster.vq.whiten(arr)

        centroids, _ = cluster.vq.kmeans(arr, 8)
        idx, _ = cluster.vq.vq(arr, centroids)

        print(idx)

    elif args.batch:
        counter = 0
        with open(args.input) as data:
            for rin in data:
                if args.ringcount and not args.quick:
                    # Count the change in ring size across the reactions
                    r = rinchi_tools.reaction.Reaction(rin)
                    res = r.change_across_reaction(r.ring_count)
                    if res and not args.list:
                        print(counter, res)
                    elif res and args.list:
                        print(rin, res)
                    counter += 1
                elif args.ringcount and args.quick:
                    # Count the change in ring size across the reactions
                    try:
                        if "X" not in rin:
                            if analysis.rxn_ring_change(rin):
                                r = rinchi_tools.reaction.Reaction(rin)
                                res = r.change_across_reaction(r.ring_count)
                                if res:
                                    print(counter, res)
                    except ValueError:
                        pass
                    counter += 1
                elif args.ringsearch:
                    # Count the change in a given ring across the reactions,
                    # supplied in a SMILE like form, eg CCCCCN for pyridine
                    r = rinchi_tools.reaction.Reaction(rin)
                    res = r.change_across_reaction(r.ring_count_by_element, args.arg2)
                    if res and not args.list:
                        print(counter, res)
                    elif res and args.list:
                        print(rin, res)
                    counter += 1

                elif args.ringelements:
                    # Count the change in rings returning the change in elemental structure of the rings
                    # e.g.  (CCCCCN : 1) would indicate the reaction forms a
                    # pyridine ring
                    r = rinchi_tools.reaction.Reaction(rin)
                    res_raw = r.change_across_reaction(r.ring_count_inc_elements)

                    # Account for the fact that cyclic permutations of rings
                    # are chemically equivalent
                    res = Counter()
                    for i in res_raw:
                        for j in res:
                            if len(i) == len(j):
                                if i in 2 * j:
                                    # Checking whether a is in 2 * b is equivalent to checking whether a and b are
                                    # cyclic permutations of each other: ABC is contained within 2 * BCA == BCABCA
                                    # whereas no non-cyclic permutations are
                                    # contained
                                    res[j] += res_raw[j]
                                    break
                        else:
                            res[i] = res_raw[i]

                    if res and not args.list:
                        print(counter, res)
                    elif res and args.list:
                        print(rin, res)
                    counter += 1

                elif args.formula:
                    r = rinchi_tools.reaction.Reaction(rin)
                    print(r.change_across_reaction(r.formula))
                elif args.isotopic:
                    r = rinchi_tools.reaction.Reaction(rin)
                    i = r.present_in_reaction(r.has_isotopic_layer)
                    if i:
                        print(i)
                elif args.valence:
                    r = rinchi_tools.reaction.Reaction(rin)
                    print(counter, r.change_across_reaction(r.valence_count))
                    counter += 1
                elif args.hybrid:
                    r = rinchi_tools.reaction.Reaction(rin)
                    print(counter, r.change_across_reaction(r.hybrid_count))
                    counter += 1
