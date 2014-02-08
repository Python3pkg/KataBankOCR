" Test Parser module "

import pytest
import subprocess

path_to_basic_input = "test/input_files/basic.txt"
path_to_advanced_input = "test/input_files/advanced.txt"

def test_parser_with_basic_input(tmpdir):
    " confirm Results from basic input file "
    expected_results = [
        '000000000',
        '111111111 ERR',
        '222222222 ERR', 
        '333333333 ERR',
        '444444444 ERR',
        '555555555 ERR',
        '666666666 ERR',
        '777777777 ERR',
        '888888888 ERR',
        '999999999 ERR',
        '123456789'
        ]
    expected = '\n'.join(expected_results) + '\n'
    with open(path_to_basic_input) as input_file:
        found = subprocess.check_output('parser/parser.py', stdin=input_file)
    assert expected == found

def test_parser_with_advanced_input(tmpdir):
    " confirm Results from advanced input file "
    expected_results = [
        '000000051', 
        '49006771? ILL',
        '1234?678? ILL',
        '200000000 ERR',
        '490067715 ERR',
        '?23456789 ILL',
        '0?0000051 ILL',
        '49086771? ILL',
        ]
    expected = '\n'.join(expected_results) + '\n'
    with open(path_to_advanced_input) as input_file:
        found = subprocess.check_output('parser/parser.py', stdin=input_file)
    assert expected == found

