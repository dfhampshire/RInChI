"""
RInChI Extended Toolkit
-----------------------

This module contains additional functions from that officially distributed by the InChI trust. It develops a range of
tools and programs to manipulate RInChIs, a concise machine readable reaction identifier.

Authors:
 - C.H.G. Allen 2012
 - N.A. Parker 2013
 - B. Hammond 2014
 - D.F. Hampshire 2016

---------------------------------------------------------------------------------------------------------------------

    Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
    the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
    on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
    the specific language governing permissions and limitations under the License.

---------------------------------------------------------------------------------------------------------------------
"""
# Create alias names for the main class objects
from .atom import Atom
from .matcher import Matcher
from .molecule import Molecule
from .reaction import Reaction
from .rinchi_lib import RInChI
