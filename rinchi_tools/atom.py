"""
RInChI Object Orientated code as developed by Ben Hammond 2014

Significant restructuring of classes by Duncan Hampshire 2016 to gain more consistent and less verbose code.

This module contains the Atom class
"""


class Atom:
    """A class containing a brief description of an atom, for use as nodes in a graph describing a molecule
    """
    def __init__(self, index=None):
        self.index = index
        self.bonds = []
        self.protons = 0
        self.mobile_protons = 0
        self.element = None
        self.isotope = None

    def valence(self):
        """
        Get the valence as determined by counting the number of bonds.

        Returns: Number of bonds

        """
        if self.mobile_protons == 0:
            return len(self.bonds) + self.protons
        else:
            return None

    def hybridisation(self):
        """
        Gets the atom hybridisation.  Only defined for C atoms but still useful

        Returns: None or a string signalling the hybridisation e.g.  "sp2"
        """
        if self.valence():
            if self.element == "C":
                if self.valence() == 4:
                    return "sp3"
                elif self.valence() == 3:
                    return "sp2"
                elif self.valence() == 2:
                    return "sp"
