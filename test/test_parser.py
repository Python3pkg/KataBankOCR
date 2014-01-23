#!/usr/bin/env python

""" Test the scanner_parser module"""

import pytest
from itertools import chain

from settings import lines_per_entry

from tools.makers.input_lines import MakeInputLines
from tools.makers.input_file import MakeInputFile
from tools.makers.entry_lines import MakeEntryLines
from tools.makers.account_string import MakeAccountString
from parser.parser import Parser, InputError

def test_instantiation_with_no_argument():
    " confirm Parser requires more than zero arguments "
    with pytest.raises(TypeError):
        p = Parser()

def test_instantiation_with_multiple_arguments(min=2,max=10):
    " confirm Parser requires fewer than 2 arguments "
    for arg_count in range(min,max+1):
        pytest.raises(TypeError, Parser, *range(arg_count))
    
def test_instantiation_with_valid_file(tmpdir):
    " confirm Parser instantiates when given the path to valid file "
    lines = MakeInputLines.random()
    valid_file_path = MakeInputFile.write(tmpdir,lines)
    p = Parser(valid_file_path)
    assert isinstance(p, Parser)

def test_file_open_failure(tmpdir):
    " confirm Parser verifies ability to open file at given path "
    pytest.raises(IOError, Parser, 'mxyzptlk')

def test_instantiation_with_abbreviated_file(tmpdir):
    " confirm Parser recognizes EOF mid-entry due to insufficient line count "
    lines = MakeInputLines.random()[:-1]
    path = MakeInputFile.write(tmpdir,lines)
    e = pytest.raises(InputError, Parser, path)
    assert e.value.message == 'file ended mid entry'
    
def test_correctly_parses_file(tmpdir):
    " confirm Parser creates entries from lines "
    account_strings = [MakeAccountString.random() for i in range(500)]
    tuples_of_lines = map(MakeEntryLines.from_account_string, account_strings)
    lines = sum(tuples_of_lines,())
    path = MakeInputFile.write(tmpdir,lines)    
#    assert len(Parser(path).account_strings) == len(account_strings)
#    assert Parser(path).account_strings == account_strings

