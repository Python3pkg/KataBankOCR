#!/usr/bin/env python

""" Test the scanner_parser module"""

import settings
from makers import MakeInputFile
from scanner_parser import scanner_parser

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
