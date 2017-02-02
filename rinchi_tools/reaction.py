"""
RInChI Object Orientated Reaction Class Module

This module contains the Reaction class and associated functions

    B. Hammond 2014
    D. Hampshire 2017 - Significant restructuring of the class to gain more consistent and less verbose code.
"""

import tempfile
from collections import Counter

from numpy import all, array
from scipy.sparse import csr_matrix

from rinchi_tools import tools, utils
from rinchi_tools.molecule import Molecule
from rinchi_tools.rinchi_lib import RInChI as RInChI_Handle


class Reaction:
    """
    This class defines a reaction, as defined by a RInChI.  Molecule objects are created from all component InChIs,
    and the member functions of the class can be used to analyse various parameters that may be changing across the
    reaction
    """

    def __init__(self, rinchi):
        """
        Args:
            rinchi: A RInChI which represent the reaction
        """

        # Split the RInChI into it's InChIs:
        self.rinchi = rinchi.rstrip()
        self.lkey = None
        self.skey = None
        self.wkey = None
        self.reactant_inchis, self.product_inchis, self.reaction_agent_inchis, self.direction, self.no_struct = tools.split_rinchi(
            rinchi)

        # Create Molecule objects for each inchi, breaking down InChIs representing composite species into individual
        # molecule objects
        self.products = []
        self.reactants = []
        self.reaction_agents = []

        self.reaction_fingerprint = None

        # Create Molecule objects for each RInChI - Molecule.new will return a list of molecule objects, one for each
        # disconnected component of the supplied InChI
        for i in self.reactant_inchis:
            self.reactants.extend(Molecule.new(i))

        for i in self.product_inchis:
            self.products.extend(Molecule.new(i))

        for i in self.reaction_agent_inchis:
            self.reaction_agents.extend(Molecule.new(i))

    #########################################
    # Calculating reaction properties ie keys, fingerprints
    #########################################

    def longkey(self):
        """
        Set longkey if not already set, then return longkey
        """
        if not self.lkey:
            self.lkey = RInChI_Handle().rinchikey_from_rinchi(self.rinchi, "L")
        return self.lkey

    def shortkey(self):
        """
        Set shortkey if not already set, then return shortkey
        """
        if not self.skey:
            self.skey = RInChI_Handle().rinchikey_from_rinchi(self.rinchi, "S")
        return self.skey

    def webkey(self):
        """
        Set webkey if not already set, then return webkey
        """
        if not self.wkey:
            self.wkey = RInChI_Handle().rinchikey_from_rinchi(self.rinchi, "W")
        return self.wkey

    def calculate_reaction_fingerprint(self, fingerprint_size=1024):
        """
        Calculates a reaction fingerprint for a given reaction.  Uses a 1024 bit fingerprint by default

        Method of Daniel M. Lowe (2015)

        This function generates fingerprints for individual molecules using obabel. Could be simply modified to use
        other software packages ie.  RDKIT if desired

        Args:
            fingerprint_size: The length of the fingerprint to be generated.

        """

        def generate_fingerprint(inchi):
            i_out, i_err = utils.call_command(["obabel", "-iinchi", "-:" + inchi, "-ofpt"])
            i_out = "".join(i_out.replace(" ", "").split("\n")[1:])

            bitarray = []
            i_out = bytearray.fromhex(i_out)
            for byte in i_out:
                bitarray.extend(map(int, list(format(byte, '08b'))))
            return bitarray

        for i in self.reactants:
            i.fingerprint = generate_fingerprint(i.inchi)
        for i in self.products:
            i.fingerprint = generate_fingerprint(i.inchi)
        for i in self.reaction_agents:
            i.fingerprint = generate_fingerprint(i.inchi)

        # Combining the fingerprints for each class of molecule
        reactant_f = [sum(i) for i in zip(*[j.fingerprint for j in self.reactants if j.fingerprint])]
        product_f = [sum(i) for i in zip(*[j.fingerprint for j in self.products if j.fingerprint])]
        reaction_agent_f = [sum(i) for i in zip(*[j.fingerprint for j in self.reaction_agents if j.fingerprint])]

        # If a reaction is missing any category, replace the entry with zero values
        if not reaction_agent_f:
            reaction_agent_f = [0] * fingerprint_size
        if not product_f:
            product_f = [0] * fingerprint_size
        if not reactant_f:
            reactant_f = [0] * fingerprint_size

        # Combining the molecular fingerprints into a reaction fingerprint using the method of Daniel M.  Lowe omega
        # and omega_na are empirically derived values as suggested in his 2015 paper
        omega_na = 10
        omega_a = 1
        res = []
        for i in range(0, len(reactant_f)):
            res.append(omega_na * (product_f[i] - reactant_f[i]) + omega_a * reaction_agent_f[i])

        # Reaction fingerprint is stored as a numpy sparse array
        self.reaction_fingerprint = csr_matrix(array(res))

    ##########################################
    # Conversions
    #########################################

    def generate_svg_image(self, outname):
        """
        Outputs the reactants, products, and agents as SVG files in the current directory with the given filename

        Args:
            outname: the name of the file to output the SVG image
        """
        out = []

        for group in (self.reactant_inchis, self.product_inchis, self.reaction_agent_inchis):
            inchi_tempfile = tempfile.NamedTemporaryFile(mode='w+t', delete=False)

            for inchi in group:
                inchi_tempfile.write(inchi + "\n")
            inchi_tempfile.close()

            # Uses the obabel package - must be installed on the system running the script
            i_out, i_err = utils.call_command(
                ["obabel", "-iinchi", inchi_tempfile.name, "-osvg", "-xd", "-xC", "-xj", "-xr 1"])
            print(i_err)
            out.append(i_out)

        for i in range(len(out)):
            with open(outname + str(i) + ".svg", "w") as text:
                text.write(out[i])

    ############################################
    # Calculating changes across reactions
    ###########################################

    def change_across_reaction(self, func, args=None):
        """
        Calculates the total change in a parameter across a molecule, Molecule class function and returns a Python
        Counter object

        Args:
            func: The class function to calculate the parameter
            args: Args if required for the function

        Returns:
            the change in the parameter

        """
        count_products = Counter()
        count_reactants = Counter()

        for mol in self.reactants:
            if args:
                count_reactants = count_reactants + func(mol, args)
            else:
                count_reactants = count_reactants + func(mol)

        for mol in self.products:
            if args:
                count_products = count_products + func(mol, args)

            else:
                count_products = count_products + func(mol)

        count_products.subtract(count_reactants)
        return count_products

    def present_in_reaction(self, func):
        """
        Tests if a molecule is present in the reaction

        Args:
            func: function of a Molecule object that returns True if a given condition is satisfied

        Returns:
            If the function returns true for any InChI, the parent RInChI is returned

        """
        for mol in self.reactants:
            if func(mol):
                return self.rinchi
        for mol in self.products:
            if func(mol):
                return self.rinchi
        return False

    @staticmethod
    def present_in_layer(layer, inchi):
        """
        Checks if an InChI is is present in a layer

        Args:
            layer: A reaction layer
            inchi: an Inchi

        Returns:
            Returns the rinchi if the inchi is present, otherwise returns None.

        """
        for mol in layer:
            if mol.inchi == inchi:
                return True
        return False

    def catalytic_in_inchi(self, inchi):
        """
        Determine whether the reaction is catalytic in a particular chemical

        Args:
            inchi: A InChI string specifying a molecule

        Returns:
            True or False (Boolean)
        """
        return self.present_in_layer(self.reaction_agents, inchi)

    def is_balanced(self):
        """
        Determine if a reaction is balanced

        Returns:
            True if Balanced, False otherwise.
        """
        return set(self.change_across_reaction(Molecule.get_formula).values()) == {0}

    def detect_reaction(self, hyb_i=None, val_i=None, rings_i=None, formula_i=None):
        """
        Detect if a reaction satisfies certain conditions.  Allows searching for reactions based on ring changes,
        valence changes, formula changes, hybridisation of C atom changes.

        Args:
            All args are dictionaries of the format {property:count,property2:count2,...}
            hyb_i: The hybridisation change(s) desired
            val_i: The valence change(s) desired
            rings_i: The ring change(s) desired
            formula_i: The formula change(s) desired

        Returns:
            True if the given reaction satisfies all the conditions, otherwise False.
        """

        if val_i is None:
            val_i = {}
        if rings_i is None:
            rings_i = {}
        if formula_i is None:
            formula_i = {}
        if hyb_i is None:
            hyb_i = {}
        if formula_i:
            formula = self.change_across_reaction(Molecule.get_formula)
            if not all(entry in formula.items() for entry in formula_i.items()):
                return False
        if val_i:
            val = self.change_across_reaction(Molecule.get_valence_count)
            if not all([entry in val.items() for entry in val_i.items()]):
                return False
        if hyb_i:
            hyb = self.change_across_reaction(Molecule.get_hybrid_count)
            if not all([entry in hyb.items() for entry in hyb_i.items()]):
                return False
        if rings_i:
            rings = self.change_across_reaction(Molecule.get_ring_count)
            if not all([entry in rings.items() for entry in rings_i.items()]):
                return False

        return True
