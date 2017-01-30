"""
RInChI utilities module.

    2016 D.F. Hampshire

This module provides functions that perform various non RInChI specific tasks.
"""

import os
import subprocess
import sys
import threading
import time


def output(text, s_out=False, ftype="rxn", input_name="File"):
    """
    Simple output wrapper to print or write outputs.
    
    Args:
         text: text input
         s_out: print the text to the screen.
         ftype: specifies the file extension
         input_name: Specifies the filename for the output file

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
    """
    Run a command as a subprocess and return the output
    
    Args:
         args: The command to execute as a string

    Returns: The output of query and error code
    """
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("utf-8"), err.decode("utf-8")


def consolidate(items):
    """
    Check that all non-empty items in an iterable are identical

    Args:
         items:

    Raises:
         ValueError: Items are not all identical

    Returns:
         value: the value of all the items in the list
    """
    value = ''
    for item in items:
        if item:
            if value:
                if not item == value:
                    raise ValueError("Non-identical item")
            else:
                value = item
    return value


class Spinner:
    """
    A spinner which shows during a long process.
    """
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def __spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        """
        Starts the spinner
        """
        self.busy = True
        threading.Thread(target=self.__spinner_task).start()

    def stop(self):
        """
        Stops the spinner
        """
        self.busy = False
        time.sleep(self.delay)
