"""
RInChI utilities module.

    2016 D.F. Hampshire

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

This module provides functions that perform various non rinchi specific tasks.
"""

import os
import subprocess


class Error(Exception):
    pass


def output(text, s_out=False, ftype="rxn", input_name="File"):
    """
    Returns a file or stdout as required.
    :param text: text input
    :param s_out: print the text to the screen.
    :param ftype: specifies the file extension
    :param input_name: Specifies the filename for the output file
    """
    # If specified, print the output.
    if s_out:
        print(text)
    # Otherwise, save to a file.
    else:
        # Ensure an output directory exists.
        if not os.path.exists('output'):
            os.mkdir('output')
        os.chdir('output')
        # Prevent overwriting.
        if os.path.exists('%s.%s' % (input_name, ftype)):
            index = 1
            while os.path.exists('%s_%d.%s' % (input_name, index, ftype)):
                index += 1
            output_name = '%s_%d.%s' % (input_name, index, ftype)
        else:
            output_name = '%s.%s' % (input_name, ftype)
        # Write to disk
        output_file = open(output_name, 'w')
        output_file.write(text)
        output_file.close()
        os.chdir(os.pardir)
    return


def call_command(args):
    """Run a command as a subprocess and return the output"""
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("utf-8"), err.decode("utf-8")


def consolidate(items):
    """Check that all non-empty items are identical, and return their value.
    """
    value = ''
    for item in items:
        if item:
            if value:
                if not item == value:
                    raise Error("Non-identical item")
            else:
                value = item
    return value


import sys
import time
import threading

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)
