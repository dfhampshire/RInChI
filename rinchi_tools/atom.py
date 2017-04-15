"""
RInChI Object Orientated Atom Class Module
------------------------------------------

This module contains the Atom class and associated functions

Modifications:
 - B. Hammond 2014
 - D. Hampshire 2017
    Restructuring and changes as documented in Project Report
"""


class Atom:
    """
    A class containing a brief description of an atom, for use as nodes in a graph describing a molecule
    """
    def __init__(self, index=None):
        self.index = index
        self.bonds = []
        self.protons = 0
        self.mobile_protons = 0
        self.element = None
        self.isotope = None
        self.hyb = None
        self.attached_edges = None
        self.valence = None
        self.mpcc = 0 # Mobile proton center count

    def __str__(self):
        try:
            if self.element is not None:
                return "<Atom Object 'index':{} 'element':{} 'H':{} 'Mob-H':{} 'MPCC': {}>".format(self.index,
                                                                                                   self.element,
                                                                                                   self.protons,
                                                                                                   self.mobile_protons,
                                                                                                   self.mpcc)
            else:
                return "<Atom Object 'index':{} 'element':None>".format(self.index)
        except:
            return '<Atom Object>'

    def __repr__(self):
        try:
            if self.element is not None:
                return "<Atom Object 'index':{} 'element':{} 'H':{} 'Mob-H':{} 'MPCC': {}>".format(self.index,
                                                                                                   self.element,
                                                                                                   self.protons,
                                                                                                   self.mobile_protons,
                                                                                                   self.mpcc)
            else:
                return "<Atom Object 'index':{} 'element':None>".format(self.index)
        except:
            return '<Atom Object>'

    def get_valence(self):
        """
        Get the valence as determined by counting the number of bonds.

        Returns:
            Number of bonds
        """
        if self.valence is None:
            if self.mobile_protons == 0:
                self.valence =  len(self.bonds) + self.protons
        return self.valence

    def get_hybridisation(self):
        """
        Gets the atom hybridisation.  Only defined for C atoms but still useful

        Returns:
            None or a string signalling the hybridisation e.g.  "sp2"
        """
        if self.hyb is None:
            if self.get_valence():
                if self.element == "C":
                    if self.get_valence() == 4:
                        self.hyb = "sp3"
                    elif self.get_valence() == 3:
                        self.hyb = "sp2"
                    elif self.get_valence() == 2:
                        self.hyb = "sp"
        return self.hyb

    def get_attached_edges(self):
        """
        Get the edges attached to this atom.

        Returns: The edges attached to the molecule.
        """
        if self.attached_edges is None:
            self.attached_edges = [tuple(sorted((self.index, bond))) for bond in self.bonds]
        return self.attached_edges
