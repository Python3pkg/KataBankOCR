#!/usr/bin/env python

""" Test the scanner_parser module"""

import pytest
import subprocess

from settings import lines_per_entry

from tools.makers.input_lines import MakeInputLines
from tools.makers.input_file import MakeInputFile
from tools.makers.entry_lines import MakeEntryLines
from tools.makers.account_string import MakeAccountString
from parser.errors import InputError
from parser.parser import Parser

def test_instantiation_with_no_argument():
    " confirm Parser requires more than zero arguments "
    pytest.raises(IOError, Parser)
#    e = pytest.raises(InputError, Parser)
#    assert e.value.message == 'nothing to parse'

def test_instantiation_with_multiple_arguments(min=2,max=10):
    " confirm Parser requires fewer than 2 arguments "
    for arg_count in range(min,max+1):
        pytest.raises(TypeError, Parser, *range(arg_count))
    
def test_instantiation_with_valid_file(tmpdir):
    " confirm Parser instantiates when given the path to a valid input file "
    path = MakeInputFile.random(tmpdir)
    p = Parser(path)
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
   
def test_instantiation_with_empty_file(tmpdir):
    " confirm Parser recognizes empty file "
    path = MakeInputFile.from_account_strings(tmpdir, [])
    e = pytest.raises(InputError, Parser, path)
    assert e.value.message == 'nothing to parse'
   
@pytest.fixture() 
def account_strings_and_path(tmpdir):
    " return 500 valid account strings and a path to a file representing them "
    account_strings = [MakeAccountString.random() for i in range(500)]
    lists_of_lines = map(MakeEntryLines.from_account_string, account_strings)
    lines = sum(lists_of_lines,[])
    path = MakeInputFile.write(tmpdir,lines)
    return account_strings, path

def test_correctly_parses_file(account_strings_and_path):
    " confirm Parser creates entries from lines "
    account_strings, path = account_strings_and_path
    assert Parser(path).account_strings == account_strings

def test_main_parses_from_std_in(account_strings_and_path):
    " confirm Parser.main parses correctly "
    account_strings, path = account_strings_and_path
    with path.open() as input_file:
        output = subprocess.check_output('parser/parser.py', stdin=input_file)
    assert output[:-1] == str(account_strings)



