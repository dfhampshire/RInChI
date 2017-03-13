#!/usr/bin/env python3
"""
RInChI Master Script. Contains all of the action of the RInChI module!

Uses a system of subparsers which can be called independently.

    Duncan Hampshire 2017

"""

import argparse

import rinchi_add
import rinchi_changes
import rinchi_convert
import rinchi_database
import rinchi_search
import rinchi_stats

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RInChI Module Command Line Tools")

    # Create subparser list
    main_functions = parser.add_subparsers(help='Main Function', dest='command')

    # Create Search functionality
    search_role = 'Search for RInChIs, InChIs & their components or RInChI Keys in a RInChI SQL Database / Flat File'
    search_parser = main_functions.add_parser('search', description=search_role, help=search_role)
    rinchi_search.add_search(search_parser)

    # Add file conversion functionality
    convert_role = "RInChI Conversion to/from other formats"
    convert_parser = main_functions.add_parser('convert', description=convert_role, help=convert_role)
    rinchi_convert.add_convert(convert_parser)

    # Add databasing tools
    db_role = "RInChI SQL Database Manipulation Tools"
    db_parser = main_functions.add_parser('db', description=db_role, help=db_role)
    rinchi_database.add_db(db_parser)

    # Add rinchi changes tools
    changes_role = "RInChI Changes Analysis"
    changes_parser = main_functions.add_parser('changes', description=changes_role, help=changes_role)
    rinchi_changes.add_changes(changes_parser)

    # Add addition functionality
    addition_role = "RInChI Addition"
    addition_parser = main_functions.add_parser('addition', description=addition_role, help=addition_role)
    rinchi_add.add_addition(addition_parser)

    #Add statistical analysis functionality
    stats_role = "RInChI Statistical analysis"
    stats_parser = main_functions.add_parser('stats', description=stats_role,help=stats_role)
    rinchi_stats.add_stats(stats_parser)

    args = parser.parse_args()

    # Direct to the appropriate parser command
    if args.command == 'search':
        rinchi_search.search_ops(args)
    elif args.command == 'convert':
        rinchi_convert.convert_ops(args, convert_parser)
    elif args.command == 'db':
        rinchi_database.db_ops(args, db_parser)
    elif args.command == 'changes':
        rinchi_changes.changes_ops(args, changes_parser)
    elif args.command == 'addition':
        rinchi_add.addition_ops(args, addition_parser)
    elif args.command == 'stats':
        rinchi_stats.stats_ops(args)
    else:
        parser.print_help()
