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


def output(text, output_path=False, default_extension=False):
    """
    Simple output wrapper to print or write outputs.

    Args:
         text: text input
         output_path: Specifies the filename for the output file
         default_extension: specifies the file extension if none in the outputname

    """

    # If specified, save to a file.

    if output_path:
        # Ensure an output directory exists.
        output_file, _ = create_output_file(output_path, default_extension)
        output_file.write(text)
        output_file.close()
        os.chdir(os.pardir)
        print('File Output: {}'.format(output_path))
    # Otherwise, print the output.
    else:
        print(text)


def create_output_file(output_path, default_extension,create_out_dir=True):
    """

    Args:
        output_path:
        default_extension:

    Returns:

    """
    # Assign extension from output name if provided
    owd = os.getcwd()
    output_path_no_ext, extension = os.path.splitext(output_path)
    assert isinstance(extension, str)
    if not extension or extension.isspace():
        extension = default_extension

    # Ensure an output directory exists.
    if create_out_dir:
        if not os.path.exists('output'):
            os.mkdir('output')
        os.chdir('output')

    # Prevent overwriting.
    output_path = output_path_no_ext + extension
    outputdir = os.path.dirname(output_path)
    try:
        os.makedirs(outputdir)
    except:
        pass
    index = 1
    while os.path.exists(output_path):
        output_path = '{}_{}{}'.format(output_path_no_ext, index, extension)
        index += 1
    output_file = open(output_path, 'a+')
    output_path = os.path.abspath(output_path)
    os.chdir(owd)
    return output_file, output_path


def call_command(args,debug=False):
    """
    Run a command as a subprocess and return the output

    Args:
         args: The command to execute as a string

    Returns:
        The output of query and error code
    """
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if debug:
        print(" ".join(args))
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
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay):
            self.delay = delay

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
    input_name, file_extension = os.path.splitext(input_path)
    if return_file_object:
        data = open(input_path)
    else:
        data = open(input_path).read()
    if filetype_check:
        if not file_extension == filetype_check:
            if file_extension not in filetype_check:
                raise IOError("File type is incorrect (wrong extension)")

    return data, input_name, file_extension


def construct_output_text(data, header_order=False):
    """
    Turns a variable containing a list of dicts or a dict or dict of lists into a single string of data

    Args:
        data: The data variable
        header_order: Optional list of keys for the dictionaries. The list can contain non present keys.

    Returns:
        data_string: The output as a text block
    """

    # Set default order for the output sting
    if not header_order or isinstance(header_order, bool):
        header_order = ['rinchi', 'rauxinfo', 'longkey', 'shortkey', 'webkey', 'rxn_data', 'rxndata', 'as_reactant',
                        'as_product', 'as_agent']

    assert isinstance(header_order, list)

    def deconstruct_dict(current_data, the_dict, key_order):
        """
        Turns a dictionary into a multi-line string
        """
        for item in key_order:
            try:
                value = the_dict.get(item, False)
                if value:
                    if isinstance(value, list):
                        current_data = deconstruct_list(current_data, value, key_order)
                    elif isinstance(value, dict):
                        current_data = deconstruct_dict(current_data, value, key_order)
                    else:
                        current_data += str(value) + '\n'
            except AttributeError:
                print("Input must be a list of dicts or a dict itself")
        return current_data

    def deconstruct_list(current_data, the_list, key_order):
        """
        Turns a dictionary into a multi-line string
        """
        for value in the_list:
            if isinstance(value, list):
                current_data = deconstruct_list(current_data, value, key_order)
            elif isinstance(value, dict):
                current_data = deconstruct_dict(current_data, value, key_order)
            else:
                current_data += str(value) + '\n'
        return current_data

    data_string = ""

    if isinstance(data, dict):
        data_string += deconstruct_dict(data_string, data, header_order)
    elif isinstance(data, list) or isinstance(data, tuple):
        data_string += deconstruct_list(data_string, data, header_order)
    else:
        data_string = data

    return data_string.strip()


def counter_to_print_string(counter, name):
    if isinstance(counter,str):
        counter = eval(counter)
    string = '{}\n{}'.format(name,'-'*len(name))
    for key, value in counter.items():
        if value:
            string += '\n' + "{} : {}".format(key,value)
    string += '\n'
    return string


class Hashable(object):
    """
    Make an object hashable for counting
    """

    def __init__(self, val):
        self.val = val

    def __hash__(self):
        return hash(str(self.val))

    def __repr__(self):
        return str(self.val)

    def __eq__(self, other):
        return str(self.val) == str(other.val)

def string_to_dict(string):
    """
    Converts a string of form 'a=1,b=2,c=3' to a dictionary of form {a:1,b:2,c:3}
    Returns:
    """
    assert isinstance(string,str)
    items = string.split(',')
    splititems = (item.split('=') for item in items)
    retdict = {str(i[0]):int(i[1]) for i in splititems}
    return retdict