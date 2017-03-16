import collections
from itertools import product

from .molecule import Molecule


class Matcher(object):
    """
    Implementation of VF2 algorithm for matching as a subgraph of another.

    made using
    http://lalg.fri.uni-lj.si/pub/amalfi/papers/vf-algorithm.pdf

    Uses the python set implementation widely for best performance.
    """

    def __init__(self, sub, master):

        # Set invariant objects
        self.backup = Backup(self)
        self.sub = sub
        self.master = master
        sub.set_atomic_elements()
        master.set_atomic_elements()
        assert isinstance(self.sub, Molecule)
        assert isinstance(self.master, Molecule)
        self.sub_atoms = set(self.sub.atoms.keys())
        self.master_atoms = set(self.master.atoms.keys())
        self.yes = False

        # These are changed by the backup class. However, only self.last_mapped is actually stored.
        self.atom_mapping = set()  # Partial mapping solution M (s)
        self.sub_atoms_mapped = set()  # M_master (s)
        self.master_atoms_mapped = set()  # M_master (s)
        self.last_mapped = ()

        # These are used in place and do not need to be backed up
        self.term_sets = ()

    def is_covering(self):
        """Checks if all the atoms are mapped from the sublist in the lists"""
        return all(atom_index in self.sub_atoms_mapped for atom_index in (self.sub.atoms.keys()))

    def new_state(self, mapping):
        self.atom_mapping.add(mapping)
        self.sub_atoms_mapped.add(mapping[0])
        self.master_atoms_mapped.add(mapping[1])
        self.last_mapped = mapping

    @staticmethod
    def get_terminal_atoms(atoms_mapped_set, molecule):
        """
        Gets the set of atoms in a moleculethat are not in the current mapping but are branches of the current mapping
        """
        terminal_set = set()
        for atom in atoms_mapped_set:
            terminal_set.update(molecule.atoms[atom].bonds)
        terminal_set.difference_update(atoms_mapped_set)
        return terminal_set

    def get_backup_mappings(self):
        """
        Get the trial mappings of the atoms in the event that no terminal mappings are found.

        The inclusion of the min is fundamental to quick execution of the script
        """
        min_unmapped_sub = min(self.sub_atoms - self.sub_atoms_mapped)
        unmapped_master = self.master_atoms - self.master_atoms_mapped
        for unmapped_master_atom in unmapped_master:
            yield min_unmapped_sub, unmapped_master_atom

    def get_terminal_mappings(self):
        """
        Gets the mappings based on terminal atoms
        """
        if not self.term_sets:  # Avoid recalculating terminal sets from earlier tests
            sub_terminal = self.get_terminal_atoms(self.sub_atoms_mapped, self.sub)
            master_terminal = self.get_terminal_atoms(self.master_atoms_mapped, self.master)
        else:
            sub_terminal = self.term_sets[0]
            master_terminal = self.term_sets[1]

        if not sub_terminal or not master_terminal:
            return None
        else:
            # This definition of P(s) ensures states not visited twice
            return set(product((min(sub_terminal),), master_terminal))

    def gen_possible_mappings(self):
        """
        The function P(s) which generates the mappings to be tested for the particular current mapping M(s)
        """
        mappings = self.get_terminal_mappings()
        if mappings is None:
            mappings = self.get_backup_mappings()
        assert isinstance(mappings, collections.Iterable)
        return mappings

    def match(self):
        """
        Extends the isomorphism mapping, and acts as the iterating function in the VF2 algorithm.

        This function is called recursively to determine if a complete
        isomorphism can be found between sub and master.  It cleans up the class
        variables after each recursive call. If an isomorphism is found,
        we return the mapping.
        """
        if self.is_covering():
            self.yes = True
            yield self.atom_mapping
        else:
            for mapping in self.gen_possible_mappings():
                if self.is_compatible(mapping):
                    self.backup.backup()
                    self.new_state(mapping)
                    for the_mapping in self.match():
                        yield the_mapping
                    # restore data structures
                    self.backup.restore()

    def is_compatible(self, mapping):
        """
        Checks if
        1. The atom mapping has the correct atom
        2. Checks that other things

        returns a list of compatable atoms.
        """
        # Add checks here for comparing whether the master atom matches the sub atom
        # insert boolean functions or other test criteria
        master_atom = self.master.atoms[mapping[1]]
        sub_atom = self.sub.atoms[mapping[0]]
        element_ok = master_atom.element == sub_atom.element
        hyb_ok = master_atom.get_hybridisation() == sub_atom.get_hybridisation()

        criteria = [self.bonds_compatible(mapping), self.count_compatable(mapping),element_ok, hyb_ok]

        # General criteria

        # Application specific criteria e.g. element
        # Return True if all criteria filled
        return all(criteria)

    def bonds_compatible(self, mapping):
        """
        Checks if the bonds to the atoms in the mapping are compatible
        """
        # Get the bonds to the already mapped graph
        sub_atom_bonds = set(self.sub.atoms[mapping[0]].bonds).intersection(self.sub_atoms_mapped)
        master_atom_bonds = set(self.master.atoms[mapping[1]].bonds).intersection(self.master_atoms_mapped)
        # Convert the sub atoms to master atoms
        master_atom_bonds_from_sub = set(self.sub_to_master(atom) for atom in sub_atom_bonds)

        return master_atom_bonds == master_atom_bonds_from_sub

    def sub_to_master(self, index):
        """
        Converts a sub graph index to the master index
        """
        for mapping in self.atom_mapping:
            if index == mapping[0]:
                return mapping[1]

    def master_to_sub(self, index):
        """
        Converts a sub graph index to the master index
        """
        for mapping in self.atom_mapping:
            if index == mapping[1]:
                return mapping[0]

    def gen_test_state(self, mapping):
        """
        Generates a test state for testing criteria.
        """
        atom_mapping = self.atom_mapping.copy()
        sub_atoms_mapped = self.sub_atoms_mapped.copy()
        master_atoms_mapped = self.master_atoms_mapped.copy()
        atom_mapping.add(mapping)
        sub_atoms_mapped.add(mapping[0])
        master_atoms_mapped.add(mapping[1])
        return atom_mapping, sub_atoms_mapped, master_atoms_mapped

    def count_compatable(self, mapping):
        self.term_sets = ()
        new_state = self.gen_test_state(mapping)
        master_term = self.get_terminal_atoms(new_state[2], self.master)  # Calculate Tin_master
        sub_term = self.get_terminal_atoms(new_state[1], self.sub)  # Calculate Tin_sub
        term_test = len(master_term) >= len(sub_term)
        other_sub = self.sub_atoms - new_state[1] - sub_term
        other_master = self.master_atoms - new_state[2] - master_term
        other_nodes = len(other_master) >= len(other_sub)
        passed = all((term_test, other_nodes))
        if passed:
            self.term_sets = (sub_term, master_term)
        return passed

    def is_sub(self):
        """Returns True if a subgraph of G1 is isomorphic to G2."""
        try:
            next(self.match())
            return True
        except StopIteration:
            return False

    def sub_count(self):
        return sum(1 for _ in self.match())


class Backup(object):
    def __init__(self, matcher_object):
        self.mapping_stack = []
        assert isinstance(matcher_object, Matcher)
        self.mr = matcher_object

    def restore(self):
        """
        Restores the previous mapping in the event of a failed mapping
        """

        # Restore the sets
        try:
            self.mr.master_atoms_mapped.discard(self.mr.last_mapped[1])
            self.mr.sub_atoms_mapped.discard(self.mr.last_mapped[0])
            self.mr.atom_mapping.discard(self.mr.last_mapped)
        except IndexError:
            # happens if there was no last added atom
            pass
        # Reset the last mapped
        try:
            self.mr.last_mapped = self.mapping_stack.pop()
        except IndexError:
            # Happens if there is no backup
            pass

    def backup(self):
        """
        Backs up this iteration of the mapping
        """
        instance = self.mr.last_mapped
        self.mapping_stack.append(instance)

    def depth(self):
        depth = len(self.mapping_stack)
        return depth
