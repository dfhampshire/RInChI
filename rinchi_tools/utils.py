"""
RInChI utilities module.

    D.F. Hampshire 2016

This module provides functions that perform various non RInChI specific tasks.
"""

import os
import subprocess
import sys
import threading
import time


def output(text, output_name, filetype, print_out=False):
    """
    Simple output wrapper to print or write outputs.

    Args:
         text: text input
         output_name: Specifies the filename for the output file
         filetype: specifies the file extension
         print_out: print the text to the screen.

    """

    # If specified, print the output.
    if print_out:
        print(text)

    # Otherwise, save to a file.
    else:
        # Ensure an output directory exists.
        output_file = create_output_file(output_name,filetype)
        output_file.write(text)
        output_file.close()
        os.chdir(os.pardir)
    return


def create_output_file(output_name, filetype):
    """

    Args:
        output_name:
        filetype:

    Returns:

    """
    # Ensure an output directory exists.
    if not os.path.exists('output'):
        os.mkdir('output')
    os.chdir('output')

    # Prevent overwriting.
    if os.path.exists('%s.%s' % (output_name, filetype)):
        index = 1
        while os.path.exists('%s_%d.%s' % (output_name, index, filetype)):
            index += 1
        output_name = '%s_%d.%s' % (output_name, index, filetype)
    else:
        output_name = '%s.%s' % (output_name, filetype)
    output_file = open(output_name, 'w')
    return output_file, output_name


def call_command(args):
    """
    Run a command as a subprocess and return the output

    Args:
         args: The command to execute as a string

    Returns:
        The output of query and error code
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


def read_input_file(input_path, filetype_check=False, return_file_object=False):
    """
    Reads an input path into a string

    Args:
        input_path:
        filetype_check:
        return_file_object:

    Returns:
        A multi-line string or a file object

    """

    # Set file name variables and read file
    input_name_inc_ext = input_path.split('/')[-1].split('.')
    input_name = input_name_inc_ext[0]
    file_extension = input_name_inc_ext[1]
    if return_file_object:
        data = open(input_path)
    else:
        data = open(input_path).read()
    if filetype_check:
        if not file_extension == filetype_check:
            if not file_extension in filetype_check:
                raise IOError("File type is incorrect (wrong extension)")

    return data, input_name, file_extension


def construct_output_text(data, header_order=False):
    """
    Turns a variable containing a list of dicts or a dict into a single string of data

    Args:
        data: The data variable
        header_order

    Returns:
        data_string: The output as a text block
    """

    # Set default order for the output sting
    if not header_order or isinstance(header_order, bool):
        header_order = ['rinchi','rauxinfo','longkey','shortkey','webkey','rxn_data','rxndata']

    if type(data) is dict:
        data = [data]

    data_string = ""

    for entry in data:
        for item in header_order:
            try:
                data_string += entry.get(item, "") + "\n"
            except AttributeError:
                print("Input must be a list of dicts or a dict itself")

    return data_string
