"""RInChI external software location module.

    Copyright 2012 C.H.G. Allen
    Modified 2016 D. Hampshire

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

This module defines variables that specify the paths to external software
used by the RInChI tools.

INCHI_PATH: Specifies the path of the InChI creation software (supplied).
"""
import os

# Path to IUPAC's InChI executable.
path = os.path.dirname(os.path.abspath(__file__))
INCHI_PATH = path + '/inchi-1'

