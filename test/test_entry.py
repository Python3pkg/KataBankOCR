#!/usr/bin/env python

""" Test the entry module"""

import pytest

import settings
from scanner_parser import entry

#from entry_testing_tools import gen_strings
#from figure_testing_tools import StringGenerators as StrGen
from scanner_parser.entry import Entry, InputError

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

