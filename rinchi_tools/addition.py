"""
RInChI addition module.

    Copyright 2012 C.H.G. Allen 2016 D.F. Hampshire

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


This module provides a function for adding together RInChIs representing the
individual steps of a multi-step reaction into one RInChI representing the
overall process. It also interfaces with the RInChI v0.03 software as provided
by the InChI trust.

The RInChI library and programs are free software developed under the
auspices of the International Union of Pure and Applied Chemistry (IUPAC).
"""

from rinchi_tools import tools


# Define an exception for the module to use.


class Error(Exception):
    pass


def add(rinchis):
    """ Combines a list of RInChIs into one combined RInChI.

    N.B. As stoichiometry is not represented in the input, this is an
        approximate addition.

    Substances from RInChIs are sorted into one of four "pots":
        "Used" contains substances which have acted as a reagent, and have not
            yet been created again as a product.
        "Made" contains substances which have been created as a product of a
            step, and have yet to be used again.
        "Present" contains substance which have been present during a step,
            but have not yet been used up or substances which have been used as
            a reagent, and later regenerated as a product.
        "Intermediates" contains substances which have been created as a
            product, and later used as a reagent.

    Each RinChI is considered in turn:

    The reactants are considered:
        If novel, add to "used".
        If in "used", remain in "used".
        If in "made", move to "intermediates".
        If in "present", move to "used".
        If in "intermediates", remain in "intermediates".
    The products are considered:
        If novel, add to "made".
        If in "used", move to "present".
        If in "made", remain in "made".
        If in "present", remain in "present".
        If in "intermediates", move to "made".
    The extras are considered:
        If novel, add to "present".

    The pots are then emptied into the following output receptacles:
        "Used" -> LHS InChIs
        "Made" -> RHS InChIs
        "Present" -> BHS InChIs
        "Intermediates" -> discarded

    Finally, the RInChI is constructed in the usual way and returned.

    Args:
        rinchis: A list of RInChIs, representing a sequence of reactions making
            up one overall process.  The order of this list is important, as
            each RInChI is interpreted as a step in the overall process. They must
            also have a clearly defined direction.

    Returns:
        rinchi: A RInChI representing the overall process.
    """
    used = set()
    made = set()
    present = set()
    intermediates = set()
    # Iterate over the RInChI steps.
    for rinchi in rinchis:
        # Parse the structures in the RInChI.
        reactants, products, extras, direction, no_structs = tools.split_rinchi(rinchi)
        if not all(v == 0 for v in no_structs):
            raise Error("No structures present")
        # Sort the structures into the various pots as per the algorithm.
        for reactant in reactants:
            if reactant in used:
                pass
            elif reactant in made:
                made.remove(reactant)
                intermediates.add(reactant)
            elif reactant in present:
                present.remove(reactant)
                used.add(reactant)
            elif reactant in intermediates:
                pass
            else:
                used.add(reactant)
        for product in products:
            if product in used:
                used.remove(product)
                present.add(product)
            elif product in made:
                pass
            elif product in present:
                pass
            elif product in intermediates:
                intermediates.remove(product)
                made.add(products)
            else:
                made.add(product)
        for extra in extras:
            if extra in used:
                pass
            elif extra in made:
                pass
            elif extra in present:
                pass
            elif extra in intermediates:
                pass
            else:
                present.add(extra)
    # Construct the overall InChI.
    return tools.build_rinchi(used, made, present, '+')
