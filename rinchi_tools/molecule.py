"""
RInChI Object Orientated Molecule Class Module

This module contains the Molecule class and associated functions

    B. Hammond 2014
    D. Hampshire 2017 - Significant restructuring of the class to gain more consistent and less verbose code.
"""

import copy
import re
from collections import Counter, deque
from itertools import zip_longest

from numpy.linalg import matrix_rank

from .atom import Atom


class Molecule:
    """
    A class containing a molecule as defined by an inchi.  Contains functions for generating edge lists and node edge
    tables describing molecular graphs, and functions that use molecular graphs to calculate information about the
    molecules - ring sizes, atom hybridisation, contained functional groups etc.
    """

    def __init__(self, inchi):
        self.inchi = inchi.rstrip()

        if ";" in self.inchi or "*" in self.inchi:
            raise ValueError('Composite InChI detected - please use the Molecule.new() method')

        self.atoms = {}  # dictionary of atom objects
        self.formula = None
        self.formula_dict = {}
        self.edge_list = None
        self.fingerprint = None
        self.is_simple = None
        self.conlayer = None
        self.atom_bonds_set = False

        # Ring counting
        self.rings = []
        self.ring_count = None
        self.ring_count_by_atoms = None
        self.ring_permutations = None
        self.has_searched_rings = False
        self.number_of_rings = None

        # Matching flag
        self.matched_in_layer = False

        # Perform initialisation
        self.init_level = None
        self.initialize()

    def __str__(self):
        return "<Molecule Object 'inchi':{}>".format(self.inchi)

    def __repr__(self):
        return "Molecule : {}".format(self.inchi)

    def initialize(self,level=1):
        """
        Initialises the molecule based on a level required
        """
        self.conlayer = self.inchi_to_layer("c")

        if self.conlayer:
            self.number_of_rings = self.count_rings()['rings']
        else:
            self.number_of_rings = 0

        if not self.formula_dict:
            self.chemical_formula_to_dict()
        self.set_atoms()
        if self.conlayer:
            self.calculate_edges()
        self.set_atomic_hydrogen()


    @staticmethod
    def composite_to_simple(inchi):
        """
        Splits an inchi with multiple disconnected components into a list of connected inchis

        # Modified 2017 D Hampshire to split formula of multiple identical components
        # cf. http://www.inchi-trust.org/technical-faq/#5.6

        Args:
            inchi: A inchi (usually composite

        Returns:
            A list of simple inchis within the composite inchi argument
        """

        # Separate the input InChI into the header, formula, and other layers
        layers = inchi.split("/")
        header = layers[0]
        formula = layers[1]
        remainder = layers[2:]

        def formula_multiples(formula):
            """
            Generates the multiple formula strings if of the form 2C6H12
            """
            formulas = formula.split(".")
            multiples = []
            for fm in formulas:
                assert isinstance(fm, str)
                if fm[0].isdigit():
                    cnt, form = re.match('([0-9]+)(.*)',fm).groups()
                    multiples.append([[form]*int(cnt),fm])
            for new_list,fm in multiples:
                insert_list(formulas, fm, new_list)
            return formulas

        def layer_splitter(comps,prefix):
            """
            Generates multiple formula strings
            """
            multiples = []
            for comp in comps:
                assert isinstance(comp, str)
                if '*' in comp:
                    cnt, comp_new = comp.split('*')
                    multiples.append([[comp_new]*int(cnt),comp])

            for new_list,fm in multiples:
                insert_list(comps, fm, new_list)

            comps = [(prefix + item) if (item != "") else "" for item in comps]
            return comps

        def insert_list(lst, original, new):
            """
            Inserts list items at the position of a single item
            """
            lstindex = lst.index(original)
            lst.remove(original)
            lst[lstindex:lstindex] = new
            return lst

        formula = formula_multiples(formula)
        individuals = [formula]

        # Formula is split on '.', other layers are split on ';'

        components = 0

        for l in remainder:
            prefix = l[0]
            ls = l[1:].split(";")
            ls = layer_splitter(ls, prefix)
            individuals.append(ls)


        # Transposes a list of split lists into a list of split inchis
        individuals = list(zip_longest(*individuals, fillvalue=""))
         # Inchis are reassembled and returned
        def gen_lists(ind):
            for i in ind:
                yield [j for j in i if j]

        ret =  (header + "/" + "/".join(x) for x in gen_lists(individuals) if x)
        return ret

    @staticmethod
    def new(inchi):
        """
        Creates a list of new Molecule objects.  Safer than Molecule() due to composite InChI implications.

        Args:
            inchi: An InChI string

        Returns:
            list of Molecule objects.

        """
        if ";" in inchi or "*" in inchi:
            return [Molecule(inch) for inch in Molecule.composite_to_simple(inchi)]
        else:
            return [Molecule(inchi)]
    #####################################################################
    # Generating molecular properties, ie.  molecular graph, chemical formula
    #####################################################################

    def inchi_to_layer(self, l):
        """
        Get a particular layer of the InChI

        Args:
            l: The layer of the InChI to retrieve

        Returns:
            The InChI layer desired
        """
        layers = self.inchi.split("/")
        for layer in layers:
            if layer.startswith(l):
                return layer[1:]
        else:
            return None

    def inchi_to_chemical_formula(self):
        """
        Converts an Inchi to a Chemical formula

        Returns:
            The Chemical Formula of the Molecule as a string
        """
        layers = self.inchi.split("/")
        return layers[1]

    def chemical_formula_to_dict(self):
        """
        Get the chemical formula as a dict

        Returns:
            A dict with elements as keys and number of atoms as value
        """
        result = {}
        if not self.formula:
            self.formula = self.inchi_to_chemical_formula()

        if self.formula_dict:
            return

        # Find all elemental formulae followed by numbers and match the element to the count
        multi_elements = re.findall(r"([A-Z][a-z]?\d+)", self.formula)
        for e in multi_elements:
            result[re.search(r"([A-Z][a-z]?)", e).group()] = int(re.search(r"(\d+)", e).group())

        # Any elements with no following number are implicitly present only once
        single_elements = re.findall(r"([A-Z][a-z]?)(?!\d+)(?![a-z])", self.formula)
        for e in single_elements:
            if e not in result.keys():
                result[e] = 1

        self.formula_dict = result

    def set_atoms(self):
        """
        Sets the atoms objects with their appropriate indexes and elements for each of the instances of the the Atom
        class.
        """
        fd = self.formula_dict.copy()
        fd.pop('H', None)
        elements = tuple(fd.keys())
        num_elements = sum(fd.values())

        if num_elements == 0:
            # Must be hydrogen only
            self.atoms = {1: Atom(1)}
            self.atoms[1].element = 'H'
            self.is_simple = True
        elif num_elements == 1:
            self.atoms = {1: Atom(1)}
            self.atoms[1].element = elements[0]
            self.is_simple = True
        elif num_elements >= 2:
            ordering = []
            ordered_atoms = []

            # In the canonical InChI labelling scheme, carbon is first, all other elements are arranged alphabetically,
            # excluding hydrogen
            if "C" in elements:
                ordering.append("C")
            heteroatoms = sorted([a for a in elements if not (a == "C" or a == "H")])
            ordering += heteroatoms

            for e in ordering:
                ordered_atoms.extend([e] * fd[e])

            # Set index and elements
            for index in range(num_elements):
                self.atoms[index + 1] = Atom(index + 1)
                self.atoms[index + 1].element = ordered_atoms[index]
            self.is_simple = False

        if num_elements == 2 and not self.conlayer:
            # Solves problems when dealing with atoms which contain only two non hydrogen atoms and have no connectivity
            # layer, but their structure can be deduced.
            self.edge_list = [(1, 2)]
            self.conlayer = '1-2'
            self.inchi += ('/c1-2')

    def set_atomic_hydrogen(self):
        """
        Takes the molecular graph and the inchi, and sets the number of protons attached to each atom.

        Requires initialised atoms.
        """
        h_layer = self.inchi_to_layer("h")

        if not h_layer:
            return None

        # Currently ignoring mobile hydrogen - Eliminate mobile hydrogen, stored as bracketed sections of the string
        mobile_groups = re.findall(r"\(H\d?,([\d,]+)\)", h_layer)
        mobile_protons = []

        for group in mobile_groups:
            for num in group.split(","):
                mobile_protons.append(int(num))

        h_layer = re.sub(r"\([\d\-,]+\)", "", h_layer)

        # Split the proton layer by the number of protons being attached to each atom
        list_by_proton = re.findall(r"(?<!H)([\d,\-]+)(?=H(\d?))", h_layer)
        dict_by_proton = {}

        for pair in list_by_proton:
            # Empty string indicates an implied single proton
            if not pair[1]:
                dict_by_proton[1] = pair[0]
            else:
                dict_by_proton[int(pair[1])] = pair[0]

        # Split the string of comma separated numbers and ranges into a list of numbers
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
        """
        Takes the connective layer of an inchi and returns the molecular graph as an edge list, parsing it directly
        using re.

        Returns:
            edges: A list containing the edges of the molecular graph
        """

        # Check if a connection layer is present
        if not self.conlayer:
            return None

        # Initialise a list containing the edges of the molecular graph, and copies of the connective layer that will
        # be destroyed in the process
        conlayer_mut = copy.deepcopy(self.conlayer)
        conlayer_comma = copy.deepcopy(self.conlayer)
        edges = []

        # Timeout variable ensures while loop will terminate, even if a non-valid string is passed
        timeout = 0

        # Deal with any comma separated values first
        for i in range(100):

            # Remove any bracketed sections that do not contain a comma
            trial_sub = re.sub(r"\([\d\-!]+\)", "!", conlayer_comma)

            # Check for timeout
            if i == 99:
                print("Error - TIMEOUT1")
                # return None

            # If the substitution did nothing, process is finished, break out of the loop
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
            # Add correct molecular edges for comma separated pairs of values MAY work for centres with a valence
            # greater than 4
            pairs = re.findall(r"(?=\b(\d+)\([\d\-!]+,(\d+))", conlayer_comma)

            for p in pairs:
                edges.append(tuple(sorted(map(int, p))))
            conlayer_comma = re.sub(r"\b(\d+\([\d\-!]+),\d+", r"\1", conlayer_comma)
            conlayer_comma = re.sub(r"\([\d\-!]+\)", "!", conlayer_comma)

        # All pairs of numbers separated by - or ( are edges of the molecular graph
        pairs = re.findall(r"(?=(\b\d+[\-(]\d+\b))", conlayer_mut)
        for p in pairs:
            edges.append(tuple(sorted(map(int, re.findall(r"\d+", p)))))

        # While there is still a layer of parenthesis remaining, eliminate the lowest layer, and join together the
        # atoms on either side of the parenthesis group
        while "(" in conlayer_mut:
            timeout += 1
            if timeout > 100:
                print("Error - TIMEOUT3")
                return None
            conlayer_mut = re.sub(r"\([\d\-!,]+\)", "!", conlayer_mut)
            pairs = re.findall(r"(?=(\b\d+!\d+\b))", conlayer_mut)
            for p in pairs:
                new_edge = tuple(sorted(map(int, re.findall(r"\d+", p))))
                if new_edge not in edges:
                    edges.append(new_edge)
        return edges

    def calculate_edges(self, edge_list=None):
        """
        Sets the node-edge graph as a dict.

        Args:
            edge_list: A molecular graph as a list of edges.  If no list is passed, the function sets the atoms for its
                own instance.
        """
        if edge_list is None:
            if self.edge_list is None:
                self.edge_list = self.generate_edge_list()
            edge_list = self.edge_list


        # Add bonds to the atom objects
        for edge in edge_list:
            self.atoms[edge[0]].bonds.append(edge[1])
            self.atoms[edge[1]].bonds.append(edge[0])
            self.atom_bonds_set = True

        return edge_list

    def edges_to_atoms(self, ls):
        """
        Sets the node-edge graph as a dict.

        Args:
            lst: A molecular graph as a list of edges.  If no list is passed, the function sets the atoms for its
                own instance.
        """

        llist = {atom: Atom(atom) for edge in ls for atom in edge}

        # Store the molecular graph in node-edge format
        for edge in ls:
            llist[edge[0]].bonds.append(edge[1])
            llist[edge[1]].bonds.append(edge[0])
        return llist

    #######################################################################
    # RING FINDING METHODS
    #######################################################################

    def depth_first_search(self, start=1):
        """
        Performs a DFS over the molecular graph of a given Molecule object, returning a list of edges that form a
        spanning tree (tree edges), and a list of the edges that would cyclise this spanning tree (back edges)

        The number of back edges returned is equal to the number of rings that can be described in the molecule

        Args:
            start: Set which atom should be the starting node

        Returns:
            tree_edges: A list of tree edges.
            back_edges: A list of back edges. The list length is equal to the smallest number of cycles that can
            describe the cycle space of the molecular graph

        """


        # Copy of the atom list that will be destroyed
        llist_mut = copy.deepcopy(self.atoms)

        # Initialise the starting node
        starting_node = start
        current_node = starting_node

        # List and a stack to store the nodes visited
        node_stack = [starting_node]
        nodes_visited = [starting_node]

        # Sorts the edges of the molecular graph into tree edges and back edges Back edges cyclise the molecular
        # graph, and so each back edge corresponds to a cycle
        tree_edges = []
        back_edges = []

        # Main Algorithm
        while node_stack:

            # If the current node has any untraversed edges
            if llist_mut[current_node].bonds:
                for child in llist_mut[current_node].bonds:
                    current_edge = [current_node, child]

                    # If the current node has a previously visited node as a child, this must be a back edge,
                    # forming a cycle.  Otherwise, this is a tree edge to an unexplored node, and the current node is
                    # changed to this node.
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

            # If the current node has no unvisited children, check the parent node.
            else:
                node_stack.pop()
                if node_stack:
                    current_node = node_stack[-1]

        return tree_edges, back_edges

    @staticmethod
    def breadth_first_search(graph, start, finish):
        """
        Get the shortest path between the start and finish nodes

        Adapted from http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/,
        accessed 06/11/2014

        Args:
            graph: an unweighted, undirected vertex-edge graph as a list
            start: the starting node
            finish: the finishing node as

        Returns:
            The shortest path as a list

        """

        # Collections.deque is a doubly linked list - supports fast addition and removal to either end of the list
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
        """
        Recursively iterates over the entire molecular graph, yielding the shortest path between two points

        Adapted from https://www.python.org/doc/essays/graphs/, accessed 15/10/2014

        Args:
            graph: an unweighted, undirected vertex-edge graph as a list
            start: the starting node as a number
            end: the finishing node as a number
            path: latest iteration of the path

        Returns:
            The shortest path as a list of indices
        """

        if path is None:
            path = []
        path = path + [start]

        # Once at the target node, go no further
        if start == end:
            return path

        shortest_path = []

        # Iterates recursively over all non-cyclic paths linking the target and final nodes If a path is smaller than
        # the previous smallest path, it replaces the smallest path.
        for child in graph[start].bonds:
            if child not in path:
                new = self.find_shortest_path(graph, child, end, path)
                if new:
                    if not shortest_path or len(new) < len(shortest_path):
                        shortest_path = new
        return shortest_path

    def find_rings_from_back_edges(self):
        """
        Accepts output from the depth_first_search algorithm, returns a list of all rings within the molecule.

        Will NOT find a minimum cycle basis, but can be used to find an initial cycle set when performing the Horton
        Algorithm (see elsewhere)
        """

        # Initialise list of all rings in the molecule
        rings_list = []
        tree_edges, back_edges = self.depth_first_search()

        for edge in back_edges:
            start, end = edge

            partial_edges = [e for e in (tree_edges + back_edges)]
            partial_edges.remove(edge)

            partial_graph = self.edges_to_atoms(partial_edges)

            path = self.find_shortest_path(partial_graph, start, end)

            rings_list.append(path)
        self.rings = rings_list

    def find_initial_ring_set(self):
        """
        For every edge in the molecule, find the smallest ring is it a part of, add it to a list
        NEEDS REIMPLEMENTATION

        Returns:
            list of all minimal rings, sorted by the number of edges they contain
        """
        # Ensure that the molecular graph was calculated
        cycles = []
        for edge in self.edge_list:
            remainder = [e for e in self.edge_list if not e == edge]
            if not remainder:
                break
            try:
                path = self.breadth_first_search(self.edges_to_atoms(remainder), edge[0], edge[1])
                if path:
                    cycles.append(self.edge_list_to_vector(self.path_to_cycle_edge_list(path)))
            except KeyError:
                pass

        # Return all minimal rings, sorted by the number of edges they contain
        return sorted(cycles, key=sum)

    def find_initial_ring_set_trial(self):
        """
        For every edge in the molecule, find the smallest ring is it a part of, add it to a list
        TRIAL REIMPLEMENTATION, NOT YET WORKING

        Returns:
            list of all minimal rings, sorted by the number of edges they contain
        """
        cycles = []
        for edge in self.edge_list:
            remainder = [e for e in self.edge_list if not e == edge]
            if not remainder:
                break
            for node in self.atoms.keys():
                try:
                    path_a = self.find_shortest_path(self.edges_to_atoms(remainder), edge[0], node)
                    if path_a:
                        path_b = self.find_shortest_path(self.edges_to_atoms(remainder), node, edge[1])
                        if path_b and (len(set(path_a).intersection(path_b)) == 1):
                            cycles.append(self.edge_list_to_vector(self.path_to_cycle_edge_list(path_a + path_b)))
                except KeyError:
                    pass

        # Return all minimal rings, sorted by the number of edges they contain
        return sorted(cycles, key=sum)

    def find_linearly_independent(self, cycles):
        """
        Given a list of candidate cycles, sorted by size, this function attempts to find the smallest,
        linearly independent basis of cycles that spans the entire cycle space of the molecular graph - the Minimum
        Cycle Basis.

        Args:
            cycles: list of candidate cycles sorted by size

        Returns:
            None
        """

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
                # print(cycle, minimum_cycle_basis)

        s = [self.edge_list_to_atoms_spanned(self.vector_to_edge_list(x)) for x in minimum_cycle_basis]
        self.rings = s
        return s

    def edge_list_to_vector(self, subset):
        """
        Converts an edge list to a vector in the (0, 1)^N vector space spanned by the edges of the molecule

        Args:
            subset: The vector subset to use

        Returns:
            The vector stored as a list.
        """
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
        """
        Converts a cycle described by an ordered list of nodes to an edge list

        Args:
            path: The path of the cycle stored as an ordered list

        Returns:
            The edge list
        """
        edges = []
        for i in range(len(path)):
            try:
                edges.append(tuple(sorted((path[i], path[i + 1]))))
            except IndexError:
                edges.append(tuple(sorted((path[i], path[0]))))
        return edges

    def vector_to_edge_list(self, vector):
        """
        Takes an edge vector and returns an edge list

        Args:
            vector: an edge vector stored in an iterable

        Returns:
            The edge list
        """
        ls = []
        for i in range(len(vector)):
            if vector[i]:
                ls.append(self.edge_list[i])
        return ls

    @staticmethod
    def edge_list_to_atoms_spanned(edge_list):
        """
        Takes an edge list and returns a list of atoms spanned

        Args:
            edge_list: An edge list

        Returns:
            A list of all the keys for the atoms which are spanned by the edge list.
        """
        atoms = {}
        for edge in edge_list:
            atoms[edge[0]] = 1
            atoms[edge[1]] = 1
        return list(atoms.keys())

    def calculate_rings(self):
        """
        Sets the ring count property which contains the ring sizes in the format { ring size : number of rings
        present, ...}
        """
        c = self.inchi_to_layer("c")
        if not c or ";" in self.inchi_to_layer("c"):
            self.ring_count = Counter()

        if not self.has_searched_rings:
            if self.number_of_rings:
                self.has_searched_rings = True
                self.find_linearly_independent(self.find_initial_ring_set())
        if self.rings:
            count = Counter([len(ring) for ring in self.rings])
            self.ring_count = count
        else:
            self.ring_count = Counter()

    @staticmethod
    def _generate_permutation_sets(ring):
        ring_perms = []
        ring_d = deque(ring)
        for __ in range(2):
            for _ in range(len(ring)):
                ring_perms.append("".join(ring_d))
                ring_d.rotate()
            ring_d.reverse()
        return ring_perms[0], set(ring_perms)

    def calculate_rings_by_atoms(self):
        """
        Count the rings by atom list eg.  "CCCCCN" will return the number of pyridine fragments in the molecule.

        Returns:
            number of rings
        """

        if not self.has_searched_rings:
            self.calculate_rings()

        count = Counter()

        all_perms_sets = {}
        # For each ring in the molecule

        rings = []
        for ring in self.rings:
            rings.append("".join([self.atoms[a].element for a in ring]))

        for ring in rings:
            if all_perms_sets:
                for ring_set, values in all_perms_sets.items():
                    if ring in values:
                        count[ring_set] += 1
                        break
                else:
                    name, data = self._generate_permutation_sets(ring)
                    count[name] += 1
                    all_perms_sets.update({name: data})
            else:
                name, data = self._generate_permutation_sets(ring)
                count[name] += 1
                all_perms_sets.update({name: data})

        self.ring_permutations = all_perms_sets
        self.ring_count_by_atoms = count

    ################
    # Analysis
    ################

    def get_ring_count(self):
        """
        Get the ring count

        Returns:
            a Counter object containing the number of rings of each size
        """
        if self.atoms:
            self.calculate_rings()
            return self.ring_count
        else:
            return Counter()

    def has_isotopic_layer(self):
        """
        Does the molecule inchi have an isotopic layer?

        Returns:
            A boolean value
        """
        if self.inchi_to_layer("i"):
            return True
        else:
            return False

    def get_hybrid_count(self):
        """
        Calculate the hybridisation of each atom

        Returns:
            A Counter object containing the hybridisation of the atoms
        """
        if self.atoms:
            self.set_atomic_hydrogen()
            return Counter([a.get_hybridisation() for a in self.atoms.values()])
        else:
            return Counter()

    def get_valence_count(self):
        """
        Calculates the valences of each atom in the Molecule

        Returns:
            A Counter object containing the valences of the atoms
        """
        if self.atoms:
            self.set_atomic_hydrogen()
            return Counter([a.get_valence() for a in self.atoms.values()])
        else:
            return Counter()

    def get_ring_count_inc_elements(self):
        """
        Count the rings of a molecule.  Result includes the elements of the ring.

        Returns:
            a Counter containing the number of rings of each size and the elements contained by a ring
        """
        self.calculate_rings_by_atoms()
        return self.ring_count_by_atoms

    def get_formula(self):
        """
        Get chemical empirical formula

        Returns:
            Chemical formula stored as a counter
        """
        self.chemical_formula_to_dict()
        return Counter(self.formula_dict)

    def count_sp3(self, wd=False, enantio=False):
        """
        Count the number of sp3 stereocentres in a molecule.

        Args:
            wd: Whether or not the stereocentre must be well-defined to be counted.
            enantio: Whether or not the structure must be enantiopure to be counted.

        Returns:
            The number of sp3 stereocentres in the structure.
        """
        sp3_centre_count = 0

        # Split the inchi into layers
        inchi_layers = self.inchi.split('/')

        # Collate all the sp3 stereochemistry layers
        sp3_layers = []
        for index, layer in enumerate(inchi_layers):
            if layer.startswith('t'):
                stereolayer = [layer]
                try:
                    if inchi_layers[index + 1].startswith('m'):
                        stereolayer.append(inchi_layers[index + 1])
                        try:
                            if inchi_layers[index + 2].startswith('s'):
                                stereolayer.append(inchi_layers[index + 2])
                        except IndexError:
                            pass
                except IndexError:
                    pass
                try:
                    if inchi_layers[index + 1].startswith('s'):
                        stereolayer.append(inchi_layers[index + 1])
                except IndexError:
                    pass
                sp3_layers.append(stereolayer)

        # If there are no sp3_layers at all, then there is no sp3 stereochemistry.
        if not sp3_layers:
            return sp3_centre_count

        # If enantio is specified, check for '/s2' (relative stereochemistry) or '/s3' (racemic) flags are present.  If
        # either are, the sp3 stereochemistry is not enantiomeric.
        if enantio:
            for layer in sp3_layers:
                for sublayer in layer:
                    if sublayer.startswith('s2') or sublayer.startswith('s3'):
                        return sp3_centre_count

        # If enantio is not specified (or if enantio is specified and there is no "/s2" or "/s3" flag), count and return
        # the stereocentres.
        for sp3_layer in sp3_layers:

            # Consider only the "/t" layer, and discard the "t" flag.
            t_layer = sp3_layer[0][1:]

            # Consider multi-component salts.
            t_layer_by_components = t_layer.split(';')
            for component in t_layer_by_components:

                # Components without stereochemistry will have empty stereolayers.
                if component:
                    sp3_centres = component.split(',')

                    # Consider stoichiometry.
                    multiplier = 1
                    if component[1] == '*':
                        multiplier = int(component[0])
                    for sp3_centre in sp3_centres:

                        # If wd is specified, only count those stereocentres which
                        # aren't "u" (undefined) or "?" (omitted).
                        if wd:
                            if sp3_centre[-1] not in 'u?':
                                sp3_centre_count += multiplier
                        else:
                            sp3_centre_count += multiplier
        return sp3_centre_count

    def count_sp2(self, wd=False):
        """
        Count the number of sp2 stereocentres.

        Args:
            wd: Whether or not the stereocentre must be well-defined to be counted.

        Returns:
            sp2_centre_count: The number of sp2 stereocentres in the structure.
        """
        sp2_centre_count = 0

        # Split the inchi into layers.

        inchi_layers = self.inchi.split('/')
        # Collate the sp2 layers.
        sp2_layers = []
        for layer in inchi_layers:
            if layer.startswith('b'):
                sp2_layers.append(layer[1:])

        # If there are no sp2 layers, the molecule has no sp2 stereochemistry.
        if not sp2_layers:
            return sp2_centre_count
        for sp2_layer in sp2_layers:

            # Discard the "d" flag.
            sp2_layer = sp2_layer[1:]

            # Consider multi-component salts.
            sp2_layer_by_components = sp2_layer.split(';')
            for component in sp2_layer_by_components:

                # Components without stereochemistry will have empty stereolayers
                if component:
                    sp2_centres = component.split(',')

                    # Consider stoichiometry.
                    multiplier = 1
                    if component[1] == '*':
                        multiplier = int(component[0])
                    for sp2_centre in sp2_centres:

                        # If wd is specified, only count those stereocentres which
                        # aren't "u" (undefined) or "?" (omitted).
                        if wd:
                            if sp2_centre[-1] not in 'u?':
                                sp2_centre_count += multiplier
                        else:
                            sp2_centre_count += multiplier
        return sp2_centre_count

    def count_rings(self):
        """
        Count the number of rings in an InChI.

        Returns:
            ring_count: The number of rings in the InChI.
        """
        count = Counter()
        conlayer = self.inchi_to_layer('c')
        if conlayer is None:
            return count

        # For each component, count the number of rings and add it to the total.
        ring_count = 0
        # Simple species do not have a connectivity layer.
        if conlayer:

            # Consider stoichiometry
            multiplier = 1
            if conlayer[1] == '*':
                multiplier = int(conlayer[0])
                conlayer = conlayer[2:]
            atoms = (conlayer.replace('(', '-').replace(')', '-').replace(',', '-').split('-'))
            for index, atom in enumerate(atoms):
                if atom in atoms[:index]:
                    ring_count += multiplier
        count['rings'] = ring_count
        if count['rings'] != 0:
            count['molecules'] = 1
        return count

    def count_centres(self, wd=False, sp2=True, sp3=True):
        """
        Counts the centres contained within an inchi

        Args:
            wd: Whether or not the stereocentre must be well-defined to be counted.
            sp2: Count sp2 centres
            sp3: Count sp3 centres

        Returns:
            stereocentres: The number of stereocentres
            stereo_mols: The number of molecules with stereocentres

        """
        count = Counter(molecules=0)
        if sp2:
            count['sp2'] = self.count_sp2(wd)
        if sp3:
            count['sp3'] = self.count_sp3(wd)
        count['stereocentres'] = count['sp2'] + count['sp3']
        if count['stereocentres'] != 0:
            count['molecules'] = 1
        return count
