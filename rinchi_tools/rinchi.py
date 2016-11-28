import copy
import re
import tempfile
from collections import Counter, deque
from itertools import zip_longest

from numpy import array, all
from numpy.linalg import matrix_rank
from scipy.sparse import csr_matrix

from rinchi_tools import tools, rinchi_lib, utils, inchi_tools

# Define a handle for the RInChI class within the C++ library
rinchi_handle = rinchi_lib.RInChI()


class Reaction:
    def __init__(self, rinchi):
        """ This class defines a reaction, as defined by a RInChI. Molecule objects are created from all component InChIs,
        and the member functions of the class can be used to analyse various parameters that may be changing across the reaction
        """

        # Split the RInChI into it's InChIs:
        self.rinchi = rinchi.rstrip()
        self.lkey = None
        self.skey = None
        self.wkey = None
        self.reactant_inchis, self.product_inchis, self.reaction_agent_inchis, self.direction, self.no_struct = tools.split_rinchi(
            rinchi)

        # Create Molecule objects for each inchi, breaking down InChIs
        # representing composite species into individual molecule objects
        self.products = []
        self.reactants = []
        self.reaction_agents = []

        self.reaction_fingerprint = None

        # Create Molecule objects for each RInChI - Molecule.new will return a list of molecule objects, one for each disconnected component
        # of the supplied InChI
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
        """Set longkey if not already set, then return longkey"""
        if not self.lkey:
            self.lkey = rinchi_handle.rinchikey_from_rinchi(self.rinchi, "L")
        return self.lkey

    def shortkey(self):
        """Set shortkey if not already set, then return shortkey"""
        if not self.skey:
            self.skey = rinchi_handle.rinchikey_from_rinchi(self.rinchi, "S")
        return self.skey

    def webkey(self):
        """Set webkey if not already set, then return webkey"""
        if not self.wkey:
            self.wkey = rinchi_handle.rinchikey_from_rinchi(self.rinchi, "W")
        return self.wkey

    def calculate_reaction_fingerprint(self, fingerprint_size=1024):
        """ Calculates a reaction fingerprint for a given reaction.
            Uses a 1024 bit fingerprint by default
            Method of Daniel M. Lowe (2015) """

        # This function generates fingerprints for individual molecules using obabel
        # Could be simply modified to use other software packages ie. RDKIT if
        # desired
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

        # If a reaction is missing any category, replace the entry with zero
        # values
        if not reaction_agent_f:
            reaction_agent_f = [0] * fingerprint_size
        if not product_f:
            product_f = [0] * fingerprint_size
        if not reactant_f:
            reactant_f = [0] * fingerprint_size

        # Combining the molecular fingerprints into a reaction fingerprint using the method of Daniel M. Lowe
        # omega and omega_na are empirically derived values as suggested in his
        # 2015 paper
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
        """Outputs the reactants, products, and agents as SVG files in the current directory with the given filename"""
        out = []

        for group in (self.reactant_inchis, self.product_inchis, self.reaction_agent_inchis):
            inchi_tempfile = tempfile.NamedTemporaryFile(mode='w+t', delete=False)

            for inchi in group:
                inchi_tempfile.write(inchi + "\n")
            inchi_tempfile.close()

            # Uses the obabel package - must be installed on the system running
            # the script
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
        """ Calculates the total change in a parameter across a molecule, given a function that accepts a Molecule
        and returns a Python Counter object
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
        """ Takes a function of a Molecule that returns true if a given condition is satisfied
         If the function returns true for any InChI, the parent RInChI is returned
        """
        for mol in self.reactants:
            if func(mol):
                return self.rinchi
        for mol in self.products:
            if func(mol):
                return self.rinchi
        return False

    def present_in_layer(self, layer, inchi):
        """ Accepts a reaction layer, and and a checking function.
        """
        for mol in layer:
            if mol.inchi == inchi:
                return self.rinchi
        return None

    @staticmethod
    def ring_change(mol):
        """ Accepts molecule object and returns a Counter containing the number of rings of each size
        """
        if mol.atoms:
            mol.calculate_rings()
            return mol.ring_count
        else:
            return Counter()

    @staticmethod
    def ring_change_inc_elements(mol):
        """ Accepts molecule object and returns a Counter containing the number of rings of each size
        """
        if mol.atoms:
            mol.calculate_rings()
            mol.set_atomic_elements()
            rings = []
            for ring in mol.rings:
                rings.append("".join([mol.atoms[a].element for a in ring]))

            return Counter(rings)
        else:
            return Counter()

    @staticmethod
    def ring_change_by_element(mol, atoms):
        return mol.contains_ring_by_atoms(atoms)

    @staticmethod
    def formula_change(mol):
        """ Accepts molecule object and returns a Counter containing the molecular formula of the molecule
        """
        mol.chemical_formula_to_dict()
        return Counter(mol.formula_dict)

    @staticmethod
    def valence_change(mol):
        """ Accepts a molecule object and attempts to calculate the valences of each atom
        """
        if mol.atoms:
            mol.set_atomic_elements()
            mol.set_atomic_hydrogen()
            return Counter([a.valence() for a in mol.atoms.values()])
        else:
            return Counter()

    @staticmethod
    def hybrid_change(mol):
        """ Accepts a molecule object and attempts to calculate the hybridisation of each atom
        """
        if mol.atoms:
            mol.set_atomic_elements()
            mol.set_atomic_hydrogen()
            return Counter([a.hybridisation() for a in mol.atoms.values()])
        else:
            return Counter()

    @staticmethod
    def search_for_isotopic(mol):
        """ Returns true if the given molecule has a defined isotopic layer
        """
        if mol.inchi_to_layer("i"):
            return True

    def catalytic_in_inchi(self, inchi):
        """ Returns a rinchi if it is catalytic in the given inchi
        """
        return self.present_in_layer(self.reaction_agents, inchi)

    def is_balanced(self):
        """ Returns true if a reaction is completely balanced"""
        return set(self.change_across_reaction(self.formula_change).values()) == {0}

    ##########################################################################
    # TESTING
    ##########################################################################

    def detect_reaction(self, hyb_i=None, val_i=None, rings_i=None, formula_i=None):
        """ Takes a series of named dicts as parameters and returns True if the given reaction satifies all the conditions.
            Allows searching for reactions based on ring changes, valence changes, formula changes, hybridisation of C atom changes,
            and contained InChIs.
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
            formula = self.change_across_reaction(self.formula_change)
            if not all(entry in formula.items() for entry in formula_i.items()):
                return False
        if val_i:
            val = self.change_across_reaction(self.valence_change)
            if not all([entry in val.items() for entry in val_i.items()]):
                return False
        if hyb_i:
            hyb = self.change_across_reaction(self.hybrid_change)
            if not all([entry in hyb.items() for entry in hyb_i.items()]):
                return False
        if rings_i:
            rings = self.change_across_reaction(self.ring_change)
            if not all([entry in rings.items() for entry in rings_i.items()]):
                return False

        return True


class Molecule:
    def __init__(self, inchi):
        """ A class containing a molecule as defined by an inchi. Contains functions for generating
            edge lists and node edge tables describing molecular graphs, and functions that use
            molecular graphs to calculate information about the molecules - ring sizes, atom hybridisation,
            contained functional groups etc.
        """
        self.inchi = inchi.rstrip()
        self.atoms = {}
        self.formula = None
        self.formula_dict = {}

        self.rings = []
        self.ring_count = None
        self.molecular_graph = None
        self.fingerprint = None
        self.edge_list = None
        # Flag for whether a ring search has taken place, avoids unnecessary
        # computation
        self.has_searched_rings = False
        self.has_set_elements = False
        # Flag for whether the molecule has a connection layer - whether or not
        # it is a simple species
        self.has_conlayer = True if self.inchi_to_layer("c") else False

        # For all molecules, construct molecular graph
        if self.has_conlayer:
            self.number_of_rings = inchi_tools.count_rings(inchi)
        else:
            self.number_of_rings = 0

        self.generate_atoms()

    @staticmethod
    def composite_inchi_to_simple(inchi):
        """ Splits an inchi with multiple disconnected components into a list of connected inchis
        """

        # Separate the input InChI into the header, formula, and other layers
        layers = inchi.split("/")
        header = layers[0]
        formula = layers[1].split(".")
        remainder = layers[2:]
        split_remainder = [formula]

        # Formula is split on '.', other layers are split on ';'
        for l in remainder:
            prefix = l[0]
            ls = l.split(";")
            split_remainder.append([ls[0]] + [prefix + x for x in ls[1:]])

        # Transposes a list of split lists into a list of split inchis
        split_remainder = list(zip_longest(*split_remainder, fillvalue=""))

        # Inchis are reassembled and returned
        lst = []
        for i in split_remainder:
            lst.append([j for j in i if len(j) > 1])
        return [header + "/" + "/".join(x) for x in lst if x]

    @staticmethod
    def new(inchi):
        """ Takes an InChI string and returns a list of Molecule objects.
        If there is a semicolon in the InChI string, then the InChI represents a collection of disconnected species:
        the InChI is separated and a list of Molecules for each separate species is returned.
        """
        if ";" in inchi:
            return [Molecule(inch) for inch in Molecule.composite_inchi_to_simple(inchi)]
        else:
            return [Molecule(inchi)]

    #####################################################################
    # Generate molecular properties, ie. molecular graph, chemical formula
    #####################################################################

    def inchi_to_chemical_formula(self):
        """ Takes an InChI and outputs only the chemical formula
        """
        layers = self.inchi.split("/")
        return layers[1]

    def chemical_formula_to_dict(self):
        """ Accepts a chemical formula and returns a dict with elements as keys and number of atoms as value
        """
        # Dict with elemental formulae as keys, and number of atoms in formula
        # as values
        result = {}
        if not self.formula:
            self.formula = self.inchi_to_chemical_formula()

        # Find all elemental formulae followed by numbers and match the element
        # to the count
        multi_elements = re.findall(r"([A-Z][a-z]?\d+)", self.formula)
        for e in multi_elements:
            result[re.search(r"([A-Z][a-z]?)", e).group()] = int(re.search(r"(\d+)", e).group())

        # Any elements with no following number are implicitly present only
        # once
        single_elements = re.findall(r"([A-Z][a-z]?)(?!\d+)(?![a-z])", self.formula)
        for e in single_elements:
            if e not in result.keys():
                result[e] = 1

        self.formula_dict = result

    def set_atomic_elements(self):
        """ Takes an InChI and a dict of Atoms and assigns each atom an element
        MOSTLY WORKING
        """
        if not self.formula_dict:
            self.chemical_formula_to_dict()
        ordering = []
        ordered_atoms = []

        # In the canonical InChI labelling scheme, carbon is first, all other elements are arranged
        # alphabetically, excluding hydrogen
        if "C" in self.formula_dict.keys():
            ordering.append("C")
        heteroatoms = sorted([a for a in self.formula_dict.keys() if not (a == "C" or a == "H")])

        ordering += heteroatoms
        for e in ordering:
            ordered_atoms.extend([e] * self.formula_dict[e])

        self.has_set_elements = True

        # Match the canonical InChI labels to their elements
        if self.has_conlayer:
            for i in range(len(ordered_atoms)):
                self.atoms[i + 1].element = ordered_atoms[i]

    def inchi_to_layer(self, l):
        """ Takes an InChI and a label l, and returns only the layer starting with l as a string"""
        layers = self.inchi.split("/")
        for layer in layers:
            if layer.startswith(l):
                return layer[1:]
        else:
            return None

    def set_atomic_hydrogen(self):
        """ Takes a molecular graph with already set elements and the corresponding inchi, and sets the
            number of protons attached to each atom
        """
        h_layer = self.inchi_to_layer("h")

        if not h_layer:
            return None

        # Currently ignoring mobile hydrogen
        # Eliminate mobile hydrogen, stored as bracketed sections of the string
        mobile_groups = re.findall(r"\(H\d?,([\d,]+)\)", h_layer)
        mobile_protons = []

        for group in mobile_groups:
            for num in group.split(","):
                mobile_protons.append(int(num))

        h_layer = re.sub(r"\([\d\-,]+\)", "", h_layer)

        # Split the proton layer by the number of protons being attached to
        # each atom
        list_by_proton = re.findall(r"(?<!H)([\d,\-]+)(?=H(\d?))", h_layer)
        dict_by_proton = {}

        for pair in list_by_proton:
            # Empty string indicates an implied single proton
            if not pair[1]:
                dict_by_proton[1] = pair[0]
            else:
                dict_by_proton[int(pair[1])] = pair[0]

        # Split the string of comma separated numbers and ranges into a list of
        # numbers
        for key in dict_by_proton.keys():
            if dict_by_proton[key].startswith(","):
                dict_by_proton[key] = dict_by_proton[key][1:]

            indexes = []
            for entry in dict_by_proton[key].split(","):
                if "-" in entry:
                    imin, imax = entry.split("-")
                    indexes.extend(range(int(imin), int(imax) + 1))
                else:
                    indexes.append(int(entry))
            # Give each atom the correct number of protons
            for index in indexes:
                self.atoms[index].protons = key
                # Mark atoms with mobile protons as such
        for index in mobile_protons:
            self.atoms[index].mobile_protons = 1

    def generate_edge_list(self):
        """ Takes the connective layer of an inchi and returns the molecular graph as an edge list, parsing
        it directly using regular expressions rather than converting it to a MOL file using the inchi-1 executable
        """
        conlayer = self.inchi_to_layer("c")
        # Check if a connection layer was actually passed
        if not conlayer:
            self.has_conlayer = False
            return None

            # Initialise a list containing the edges of the molecular graph, and copies of the connective layer
        # that will be destroyed in the process
        conlayer_mut = copy.deepcopy(conlayer)
        conlayer_comma = copy.deepcopy(conlayer)
        edges = []

        # Timeout variable ensures while loop will terminate, even if a
        # non-valid string is passed
        timeout = 0

        # Deal with any comma separated values first
        for i in range(100):
            # Remove any bracketed sections that do not contain a comma
            trial_sub = re.sub(r"\([\d\-!]+\)", "!", conlayer_comma)

            # Check for timeout
            if i == 99:
                print("Error - TIMEOUT1")
                # return None

            # If the substitution did nothing, process is finished, break out
            # of the loop
            if trial_sub != conlayer_comma:
                conlayer_comma = trial_sub
            else:
                break
        while "," in conlayer_comma:
            timeout += 1
            if timeout > 100:
                print(self.inchi)
                print("Error - TIMEOUT2")
                return None
            # Add correct molecular edges for comma separated pairs of values
            # MAY work for centres with a valence greater than 4
            pairs = re.findall(r"(?=\b(\d+)\([\d\-!]+,(\d+))", conlayer_comma)

            for p in pairs:
                edges.append(list(map(int, p)))
            conlayer_comma = re.sub(r"\b(\d+\([\d\-!]+),\d+", r"\1", conlayer_comma)
            conlayer_comma = re.sub(r"\([\d\-!]+\)", "!", conlayer_comma)

        # All pairs of numbers separated by - or ( are edges of the molecular
        # graph
        pairs = re.findall(r"(?=(\b\d+[\-(]\d+\b))", conlayer_mut)
        for p in pairs:
            edges.append(list(map(int, re.findall(r"\d+", p))))

        # While there is still a layer of parenthesis remaining, eliminate the
        # lowest layer, and join together the atoms on either side of the
        # parenthesis group
        while "(" in conlayer_mut:
            timeout += 1
            if timeout > 100:
                print("Error - TIMEOUT3")
                return None
            conlayer_mut = re.sub(r"\([\d\-!,]+\)", "!", conlayer_mut)
            pairs = re.findall(r"(?=(\b\d+!\d+\b))", conlayer_mut)
            for p in pairs:
                new_edge = list(map(int, re.findall(r"\d+", p)))
                if new_edge not in edges:
                    edges.append(new_edge)
        return edges

    def generate_atoms(self, lst=None):
        """ Takes a molecular graph as a list of edges and returns a node-edge graph as a dictionary
        If no list is passed, the function sets the atoms for an instance of a Molecule object
        """
        # Initialise key for each atom label, each with the value of an empty
        # list
        if lst:
            ls = lst
        else:
            self.edge_list = self.generate_edge_list()
            ls = self.edge_list
            if not ls:
                return None

        llist = {atom: Atom() for edge in ls for atom in edge}

        # Store the molecular graph in node-edge format
        for edge in ls:
            llist[edge[0]].bonds.append(edge[1])
            llist[edge[1]].bonds.append(edge[0])
        if lst:
            return llist
        else:
            self.atoms = llist

            #######################################################################
            # RING FINDING METHODS
            #######################################################################

    def depth_first_search(self, start=1):
        """ Performs a DFS over the molecular graph of a given Molecule object, returning a list of edges that form
        a spanning tree (tree edges), and a list of the edges that would cyclise this spanning tree (back edges)

        The number of back edges returned is equal to the smallest number of cycles that can describe the cycle space of
        the molecular graph
        """

        # Ensure that the molecular graph has been generated
        if not self.atoms:
            self.generate_atoms()

        # Copy of the atom list that will be destroyed
        llist_mut = copy.deepcopy(self.atoms)

        # Initialise the starting node
        starting_node = start
        current_node = starting_node

        # List and a stack to store the nodes visited
        node_stack = [starting_node]
        nodes_visited = [starting_node]

        # Sorts the edges of the molecular graph into tree edges and back edges
        # Back edges cyclise the molecular graph, and so each back edge
        # corresponds to a cycle
        tree_edges = []
        back_edges = []

        # Main Algorithm
        while node_stack:
            # If the current node has any untraversed edges
            if llist_mut[current_node].bonds:
                for child in llist_mut[current_node].bonds:
                    current_edge = [current_node, child]

                    # If the current node has a previously visited node as a child, this must be a back edge,
                    # forming a cycle. Otherwise, this is a tree edge to an unexplored node, and the current
                    # node is changed to this node.
                    if child in nodes_visited:
                        back_edges.append(current_edge)
                        llist_mut[current_node].bonds.remove(child)
                        llist_mut[child].bonds.remove(current_node)
                    else:
                        nodes_visited.append(child)
                        tree_edges.append(current_edge)

                        llist_mut[current_node].bonds.remove(child)
                        llist_mut[child].bonds.remove(current_node)

                        node_stack.append(child)
                        current_node = child
                        break
            # If the current node has no unvisited children, check the parent
            # node.
            else:
                node_stack.pop()
                if node_stack:
                    current_node = node_stack[-1]

        return tree_edges, back_edges

    @staticmethod
    def breadth_first_search(graph, start, finish):
        """ Accepts an unweighted, undirected vertex-edge graph and returns as a list the shortest path between
        the start and finish nodes.

        Adapted from http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/,
        accessed 06/11/2014
        """

        # Collections.deque is a doubly linked list - supports fast addition
        # and removal to either end of the list
        queue = deque([(start, [start])])
        while queue:
            (vertex, path) = queue.popleft()
            for nxt in set(graph[vertex].bonds) - set(path):
                if nxt == finish:
                    # Target node has been found, return the path
                    return path + [nxt]
                else:
                    queue.append((nxt, path + [nxt]))

    def find_shortest_path(self, graph, start, end, path=None):
        """ Recursively iterates over the entire molecular graph, yielding the shortest path between two points
        Adapted from https://www.python.org/doc/essays/graphs/, accessed 15/10/2014
        """

        if path is None:
            path = []
        path = path + [start]

        # Once at the target node, go no further
        if start == end:
            return path

        shortest_path = []

        # Iterates recursively over all non-cyclic paths linking the target and final nodes
        # If a path is smaller than the previous smallest path, it replaces the
        # smallest path.
        for child in graph[start].bonds:
            if child not in path:
                new = self.find_shortest_path(graph, child, end, path)
                if new:
                    if not shortest_path or len(new) < len(shortest_path):
                        shortest_path = new
        return shortest_path

    def find_rings_from_back_edges(self):
        """ Accepts output from the depth_first_search algorithm, returns a list of all rings
            within the molecule.

            Will NOT find a minimum cycle basis, but can be used to find an initial cycle set
            when performing the Horton Algorithm (see elsewhere)
        """

        # Initialise list of all rings in the molecule. Accepts

        rings_list = []
        tree_edges, back_edges = self.depth_first_search()

        for edge in back_edges:
            start, end = edge

            partial_edges = [e for e in (tree_edges + back_edges)]
            partial_edges.remove(edge)

            partial_graph = self.generate_atoms(partial_edges)

            path = self.find_shortest_path(partial_graph, start, end)

            rings_list.append(path)
        self.rings = rings_list

    def find_initial_ring_set(self):
        """ For every edge in the molecule, find the smallest ring is it a part of, add it to a list
            NEEDS REIMPLEMENTATION
        """
        # Ensure that the molecular graph was calculated
        if not self.atoms:
            return None
        self.generate_atoms()
        cycles = []
        for edge in self.edge_list:
            remainder = [e for e in self.edge_list if not e == edge]
            if not remainder:
                break
            try:
                path = self.breadth_first_search(self.generate_atoms(remainder), edge[0], edge[1])
                if path:
                    cycles.append(self.edge_list_to_vector(self.path_to_cycle_edge_list(path)))
            except KeyError:
                pass
        # Return all minimal rings, sorted by the number of edges they contain
        return sorted(cycles, key=sum)

    def find_initial_ring_set_trial(self):
        """ For every edge in the molecule, find the smallest ring is it a part of, add it to a list
            TRIAL REIMPLEMENTATION, NOT YET WORKING
        """
        if not self.atoms:
            return None
        self.generate_atoms()
        cycles = []
        for edge in self.edge_list:
            remainder = [e for e in self.edge_list if not e == edge]
            if not remainder:
                break
            for node in self.atoms.keys():
                try:
                    path_a = self.find_shortest_path(self.generate_atoms(remainder), edge[0], node)
                    if path_a:
                        path_b = self.find_shortest_path(self.generate_atoms(remainder), node, edge[1])
                        if path_b and (len(set(path_a).intersection(path_b)) == 1):
                            cycles.append(self.edge_list_to_vector(self.path_to_cycle_edge_list(path_a + path_b)))
                except KeyError:
                    pass
        # Return all minimal rings, sorted by the number of edges they contain
        return sorted(cycles, key=sum)

    def find_linearly_independent(self, cycles):
        """ Given a list of candidate cycles, sorted by size, this function attempts to find the
        smallest, linearly independent basis of cycles that spans the entire cycle space of the
        molecular graph - the Minimum Cycle Basis.
        """

        # If no atoms are set, molecule is a simple species - has no rings
        if not self.atoms:
            self.rings = None
            self.ring_count = Counter()
            return None

        # Calculates the minimal cycle basis for an inputted sorted cycle space
        minimum_cycle_basis = []
        for cycle in cycles:

            # If all the rings have been found, stop
            if len(minimum_cycle_basis) == self.number_of_rings:
                break

            # Try adding each cycle to the basis
            matrix = (minimum_cycle_basis + [cycle])

            # If the rank of the basis has not increased, the new cycle is linearly dependent on the
            # current basis, and so is not a member of the MCB
            if matrix_rank(matrix) == len(minimum_cycle_basis) + 1:
                minimum_cycle_basis.append(cycle)
                # elif cycle == [sum(i) % 2 for i in zip(*minimum_cycle_basis)]:
                # print(cycle, minimum_cycle_basis

        s = [self.edge_list_to_atoms(self.vector_to_edge_list(x)) for x in minimum_cycle_basis]

        self.rings = s
        return None

    def edge_list_to_vector(self, subset):
        # Converts an edge list to a vector in the (0, 1)^N vector space
        # spanned by the edges of the molecule
        vector = []
        for edge in self.edge_list:
            if edge in subset:
                vector.append(1)
            elif [edge[1], edge[0]] in subset:
                vector.append(1)
            else:
                vector.append(0)
        return vector

    @staticmethod
    def path_to_cycle_edge_list(path):
        # Converts a cycle described by an ordered list of nodes to an edge
        # list
        edges = []
        for i in range(len(path)):
            try:
                edges.append([path[i], path[i + 1]])
            except IndexError:
                edges.append([path[i], path[0]])
        return edges

    def vector_to_edge_list(self, vector):
        # Takes an edge vector and returns an edge list
        ls = []
        for i in range(len(vector)):
            if vector[i]:
                ls.append(self.edge_list[i])
        return ls

    @staticmethod
    def edge_list_to_atoms(edge_list):
        # Takes an edge list and returns a list of atoms spanned
        atoms = {}
        for edge in edge_list:
            atoms[edge[0]] = 1
            atoms[edge[1]] = 1
        return atoms.keys()

    def calculate_rings(self):
        """ Takes an InChI as input and returns a Python Counter dict in the format
        ring size : number of rings present """

        # TEMPORARY FIX for algorithm breaking on disconnected components
        c = self.inchi_to_layer("c")
        if not c or ";" in self.inchi_to_layer("c"):
            self.ring_count = Counter()
            # return None

        if not self.has_searched_rings:
            if self.number_of_rings:
                self.has_searched_rings = True
                self.find_linearly_independent(self.find_initial_ring_set())
        if self.rings:
            count = Counter([len(ring) for ring in self.rings])
            self.ring_count = count
        else:
            self.ring_count = Counter()

    def contains_ring_by_atoms(self, atoms):
        """ Returns the number of rings of a given atomic configuration: eg. "CCCCCN" will
        return the number of pyridine fragments in the molecule.
        """

        if not self.has_searched_rings:
            self.calculate_rings()
        if not self.has_set_elements:
            self.set_atomic_elements()

        count = Counter()

        # Collections.deque is used to store the atom lists - supports fast
        # cyclic permutation
        atom_list = deque(atoms.rstrip())

        # For each ring in the molecule
        for ring in self.rings:
            # For each cyclic permutation of the input string
            ring_deque = deque([self.atoms[j].element for j in ring])
            for i in range(len(atom_list)):
                if ring_deque == atom_list:
                    count[atoms] += 1
                    break
                atom_list.rotate(1)
            else:
                # If no match found, check again with the input string reversed
                atom_list.reverse()
                for i in range(len(atom_list)):
                    if ring_deque == atom_list:
                        count[atoms] += 1
                        break
                    atom_list.rotate(1)
        return count


class Atom:
    def __init__(self, index=None):
        """ A class containing a brief description of an atom, for use as nodes in a graph describing a molecule
        """
        self.index = index
        self.bonds = []
        self.protons = 0
        self.mobile_protons = 0
        self.element = None
        self.isotope = None

    def valence(self):
        if self.mobile_protons == 0:
            return len(self.bonds) + self.protons
        else:
            return None

    def hybridisation(self):
        """Currently only defined for C atoms but still useful"""
        if self.valence():
            if self.element == "C":
                if self.valence() == 4:
                    return "sp3"
                elif self.valence() == 3:
                    return "sp2"
                elif self.valence() == 2:
                    return "sp"