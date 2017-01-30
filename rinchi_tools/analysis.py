"""
RInChI analysis module.

    Copyright 2012 C.H.G. Allen 2016 D.F Hampshire

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

This module provides functions for the counting rings and stereocentres in
InChIs and RInChIs.  It also provides a function for searching for InChIs
in a database of RInChIs. It also interfaces with the RInChI
v0.03 software as provided by the InChI trust.

The RInChI library and programs are free software developed under the
auspices of the International Union of Pure and Applied Chemistry (IUPAC).
"""

from rinchi_tools import inchi_tools, tools


# Define an exception for the module to use.
class Error(Exception):
    pass


def rxn_ring_change(input_rinchi, pm=(False, False),
                    return_ring_counts_only=False):
    """
    Determine how the number of rings changes in a reaction.

    Args:
        input_rinchi: A RInChI to analyse.
        pm: A tuple containing booleans for whether to calculate ring changes per
            molecule ( pm[0] ) or per cyclic molecule ( pm[1] ). The default is not
            to calculate per molecule.
        return_ring_counts_only: Only return ring counts in each layer

    Returns:
        Either:
            reactant_rings, product_rings, agent_rings:The number of rings in the
                respective layers of the RInChI.
        Or:
            ring_change: The number of rings created by the reaction.  If rings
                are destroyed, this will be negative.  If the reaction is an
                equilibrium or direction is unspecified, the value of ring
                change will be the absolute (i.e. positive) value.

    Raises:
        Error: If the ring change cannot be analysed.  This may either be
            because the reaction contains undefined structures or lacks either
            products or reactants.
    """
    # Count the rings in the RInChI's groups.
    reactants, products, agents, direction, no_structs = tools.split_rinchi(input_rinchi)

    def layer_ring_counter(layer):
        layer_rings = 0
        cyclic_mols = 0
        for inchi in layer:
            inchi_rings = inchi_tools.count_rings(inchi)
            layer_rings += inchi_rings
            if inchi_rings:
                cyclic_mols += 1
        return layer_rings, cyclic_mols

    reactant_rings, reactant_cyclics = layer_ring_counter(reactants)
    product_rings, product_cyclics = layer_ring_counter(products)
    agent_rings, agent_cyclics = layer_ring_counter(agents)
    # If required, return the ring counts and do not calculate ring change.
    if return_ring_counts_only:
        return reactant_rings, product_rings, agent_rings
    # Do not calculate ring change if the RInChI contains undefined structures.
    if not all(v == 0 for v in no_structs):
        raise Error('RInChI contains an undefined structure.')
    # Do not calculate ring change if the RInChI lacks either reactants or
    # products.
    if not (reactants and products):
        raise Error('RInChI must have reactants and products.')
    # If required, divide the number of rings by the number of molecules.
    if pm[0]:
        if pm[1]:
            if reactant_cyclics:
                reactant_rings /= reactant_cyclics
            if product_cyclics:
                product_rings /= product_cyclics
        else:
            reactant_rings /= len(reactants)
            product_rings /= len(products)
    ring_change = product_rings - reactant_rings
    if (direction == '=') or (direction == ''):
        ring_change = abs(ring_change)
    return ring_change


def rxns_ring_changes(rinchis, pm=(False, False)):
    """Analyse a list of rinchis for ring changes.

    Args:
        rinchis: A list of RInChIs.
        pm: A tuple containing booleans for whether to calculate ring changes per
            molecule ( pm[0] ) or per cyclic molecule ( pm[1] ). The default is not
            to calculate per molecule.
    Returns:
        results: A dictionary, of which the keys are reaction ring changes and
            the entries are lists of RInChIs.  This allows for the lookup of
            RInChIs by the number of rings created or destroyed in the
            reaction.
    """
    results = dict()
    for rinchi_entry in rinchis:
        try:
            ring_change = rxn_ring_change(rinchi_entry, pm)
            try:
                results[ring_change].append(rinchi_entry)
            except KeyError:
                results[ring_change] = [rinchi_entry]
        except Error:
            pass
    return results


def rxn_stereochem_change(input_rinchi, wd=False, pm=(False, False),
                          sp2=True, sp3=True):
    """Determine whether a reaction creates or destroys stereochemistry.

    Args:
        wd: Whether only well-defined stereocentres count.
        input_rinchi: A RInChI.
        pm: A tuple of booleans.  The first boolean determines whether to count
            the change in number of stereocentres-per-molecule (rather than
            just the absolute number).  If this is true, the second boolean
            determines whether to count stereocentres-per-molecule-with-
            stereochemistry (if true) or simply stereocentres-per-molecule
            (if false).
        sp2: Whether to count sp2 stereocentres.
        sp3: Whether to count sp3 stereocentres.

    Returns:
        The number of stereocentres created by a reaction.  If the reaction is
        an equilibrium or of undefined direction, the absolute value is
        returned.  Using the "pm" option may result in fractional values.

    Raises:
        Error: If the stereochemical change cannot be computed because the
            RInChI includes undefined structures, or if either reactants or
            products are missing.
    """
    # Grab the data from the input RInChI.
    reactants, products, agents, direction, no_structs = tools.split_rinchi(input_rinchi)
    # If the reaction does not have reactants and products, do not count.
    if not (reactants and products):
        raise Error('RInChI must have reactants and products.')
    # Count the stereocentres in layer 2.
    reactant_stereocentres = 0
    reactant_stereo_mols = 0
    product_stereocentres = 0
    product_stereo_mols = 0

    for inchi in reactants:
        if no_structs[0] != 0:
            raise Error('RInChI Reactants contain undefined structures.')
        sc_change, sm_change = inchi_tools.count_centres(inchi, wd, sp2, sp3)
        reactant_stereocentres += sc_change
        reactant_stereo_mols += sm_change
    for inchi in products:
        if no_structs[1] != 0:
            raise Error('RInChI Products contain undefined structures.')
        sc_change, sm_change = inchi_tools.count_centres(inchi, wd, sp2, sp3)
        product_stereocentres += sc_change
        product_stereo_mols += sm_change
    # If required, divide stereocentres by the number of molecules.
    if pm[0]:
        if pm[1]:
            if reactant_stereo_mols:
                reactant_stereocentres /= reactant_stereo_mols
            if product_stereo_mols:
                product_stereocentres /= product_stereo_mols
        else:
            reactant_stereocentres /= len(reactants)
            product_stereocentres /= len(products)
    # Calculate the change.
    stereocentre_change = product_stereocentres - reactant_stereocentres
    if direction == '+' or direction == '-':
        return stereocentre_change
    else:
        return abs(stereocentre_change)


def rxns_stereochem_changes(rinchis, wd=False, pm=(False, False),
                            sp2=True, sp3=True):
    """Analyse a list of RInChIs for stereochemical changes.

    Args:
        rinchis: A list of RInChIs.
        wd: Whether only well-defined stereocentres count.
        pm: A tuple of booleans.  The first boolean determines whether to count
            the change in number of stereocentres-per-molecule (rather than
            just the absolute number).  If this is true, the second boolean
            determines whether to count stereocentres-per-molecule-with-
            stereochemistry (if true) or simply stereocentres-per-molecule
            (if false).
        sp2: Whether to count sp2 stereocentres.
        sp3: Whether to count sp3 stereocentres.

    Returns:
        results: A dictionary, of which the keys are changes in stereocentres
            and the entries are lists of RInChIs.  This allows for the lookup
            of RInChIs by the number of stereocentres created or destroyed in
            the reaction.
    """
    results = dict()
    for rinchi_entry in rinchis:
        try:
            stereochange = rxn_stereochem_change(
                rinchi_entry, wd, pm, sp2, sp3)
            try:
                results[stereochange].append(rinchi_entry)
            except KeyError:
                results[stereochange] = [rinchi_entry]
        except Error:
            pass
    return results


def search_4_inchi(sought_inchi, rinchis, location=''):
    """Search for an InChI in a list of RInChIs.

    Args:
        sought_inchi: The InChI to search for.
        rinchis: The list of RInChIs in which to search for the InChI.
        location: Where in the RInChIs to search for the InChI.  This is a
            single character which can be either:
                a) r: for Reactants.
                b) p: for Products.
                c) e: for Equilibrium reactants.
                d) a: for reaction Agents.

    Returns:
        results: A list of RInChIs in which the InChI is found in the location
            specified.
    """
    results = []
    for rinchi in rinchis:
        reactants, products, agents, direction, no_structs = tools.split_rinchi(rinchi)
        if direction == '+' or direction == '-':
            eqibs = []
        elif direction == '=':
            eqibs = reactants + products
        else:
            reactants = []
            products = []
            eqibs = []

        def they_call_me_the_seeker(search_inchi, group):
            # (I've been seeking low and hiiiiigh)
            for inchi in group:
                if search_inchi == inchi:
                    results.append(rinchi)

        if location.startswith('r'):
            they_call_me_the_seeker(sought_inchi, reactants)
        elif location.startswith('p'):
            they_call_me_the_seeker(sought_inchi, products)
        elif location.startswith('a'):
            they_call_me_the_seeker(sought_inchi, agents)
        elif location.startswith('e'):
            they_call_me_the_seeker(sought_inchi, eqibs)
        else:
            they_call_me_the_seeker(sought_inchi, (reactants + products + agents))
    return results
