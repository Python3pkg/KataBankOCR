#!/usr/bin/env python

""" Test the scanner_parser module"""

import pytest

import settings

from tools.decorators import repeats
from tools.makers import MakeInputFile
from parser.parser import Parser

def test_instantiation_with_no_argument():
    " confirm Parser requires more than zero arguments "
    with pytest.raises(TypeError):
        p = Parser()

def test_instantiation_with_multiple_arguments(min=2,max=10):
    " confirm Parser requires fewer than 2 arguments "
    for arg_count in range(min,max+1):
        pytest.raises(TypeError, Parser, *range(arg_count))
    
@repeats(1000)
def test_instantiation_with_valid_lines():
    " confirm Parser instantiates with a valid path string argument "
#    path = 
#    p = Entry(MakeEntryLines.valid())
#    assert isinstance(e,Entry)
    pass



FileErrors = """
    can't open file
    file empty
    file ended mid-entry
"""

full_check = """
def test_recognition_of_numbers_in_valid_file():
    " confirm scanner_parser parses valid file into correct account numbers "
    account_number = random_account_number()
    entry_lines = account_number_to_lines(account_number)
    e = Entry(tuple(entry_lines))
    assert e.account_number == account_number
"""
#def test_handling_of_file_containing_faulty_figures():

def test_file(tmpdir):
    account_number_count = 500
    path = tmpdir.join(str(account_number_count) + '_valid_account_numbers.txt')
    MakeInputFile.valid(path,account_number_count)
    F = path.open()
    A = F.readline()
    B = F.readline()
    assert A != B

    #more
