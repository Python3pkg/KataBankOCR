#!/usr/bin/env python

""" Test the entry module"""

import pytest

import settings
from scanner_parser import entry

from entry_testing_tools import entries
from scanner_parser.entry import Entry, InputError

def test_instantiation_with_no_argument():
    " confirm Entry requires more than zero arguments "
    with pytest.raises(TypeError):
        e = Entry()

def test_instantiation_with_multiple_arguments(min=2,max=10):
    " confirm Figure requires fewer than 2 arguments "
    args = min
    while args <= max:
        with pytest.raises(TypeError):
            e = Entry(*range(args))
        args += 1
    
#def test_instantiation_with_valid_lines():
#    " confirm Figure instantiates with a valid string argument "
#    for valid_string in entries.keys():
#        e = Entry(valid_string)
#        assert isinstance(f,Figure)



ideas="""
possible InputErrors
    too many lines
    too few lines
    non string
    line too short
    line too long
    last line un-empty

lines to figures

concat figure values into account number

"""


#lines_per_entry
#figures_per_entry
#figure_width
#characters_per_figure
#valid_figure_characters
#figures
#last_line_empty

