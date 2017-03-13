# !/usr/bin/env python3
"""
Script used to test various the module during development.  Not for general distribution.  Successful code is
implemented elsewhere.

    Duncan Hampshire 2017
"""
from collections import Counter

from rinchi_tools import conversion


def test():
    d = open('test-resources/testrxn').read()
    print(conversion.rxn_to_rinchi(d))


def test2():
    for i in range(10000):
        c = Counter({1: 1, 2: 2, 3: 3, 4: -1, 5: 5, 6: 0})
        to_remove = set()
        for key, value in c.items():
            if value == 0:
                to_remove.add(key)
        for key in to_remove:
            del c[key]
    print(c)


def test3():
    for i in range(10000):
        c = Counter({1: 1, 2: 2, 3: 3, 4: -1, 5: 5, 6: 0})
        c = Counter({k: v for k, v in c.items() if v != 0})
    print(c)


test()
