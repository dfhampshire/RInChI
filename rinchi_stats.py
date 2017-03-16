#!/usr/bin/env python3
"""
RInChI Statictics Script

Searches an SQL database for InChIs.

    D. Hampshire 2017 - Rewrote search function completely. Based on the work of B. Hammond 2014
"""

import argparse

from rinchi_tools import tools, utils


def add_stats(subparser):
    assert isinstance(subparser, argparse.ArgumentParser)

    # Add main search arguments
    subparser.add_argument("input", help="The flat file of rinchis to generate statistics from")
    subparser.add_argument('-all', action="store_true",help='return all information')
    subparser.add_argument("-r","--reactants", action="store_true",help="Include information about the reactants")
    subparser.add_argument('-p','--products',action="store_true",help='Include Information about the products')
    subparser.add_argument("-a",'--agents',action = 'store_true', help='Include information about the agents')
    subparser.add_argument("-d", '--directions', action='store_true', help='Include information about the directions')
    subparser.add_argument('-u', '--unknownstructs', action='store_true',
                           help='Include information about unknown structures')
    subparser.add_argument("-m",'--mostcommon',nargs='?', const=5,default=None,
                           help='Only include information about the most commonly occuring items')


def stats_ops(args):
    data = tools.rinchi_to_dict_list(open(args.input),)
    rinchis = (item['rinchi'] for item in data)
    data = tools.process_stats(rinchis, int(args.mostcommon))
    p_string = 'STATS\n-----\n'
    p_string += utils.counter_to_print_string(data['pops'],'Populations')
    if args.reactants or args.all:
        p_string += '\n' + utils.counter_to_print_string(data['reactants'], 'Reactants')
    if args.products or args.all:
        p_string += '\n' + utils.counter_to_print_string(data['products'],'Products')
    if args.agents or args.all:
        p_string += '\n' + utils.counter_to_print_string(data['agents'], 'Agents')
    if args.directions or args.all:
        p_string += '\n' + utils.counter_to_print_string(data['directions'], 'Directions')
    if args.unknownstructs or args.all:
        p_string += '\n' + utils.counter_to_print_string(data['unknownstructs'],'Unknown Structures')
    print(p_string)


if __name__ == "__main__":
    role = "RInChI Statistical analysis"
    parser = argparse.ArgumentParser(description=role)
    add_stats(parser)
    args = parser.parse_args()
    stats_ops(args)