import pytest
import mock
import subprocess

import settings
from parser.parser import Parser
from parser.stream import Stream
from parser.lines import Lines
from parser.entry import Entry
from parser.figure import Figure

path_to_basic_input = "test/input_files/basic.txt"
accounts_in_basic_input = ['000000000', '111111111', '222222222', '333333333',
                           '444444444', '555555555', '666666666', '777777777',
                           '888888888', '999999999', '123456789']
valid_accounts_in_basic_input = ['000000000', '123456789',]
invalid_accounts_in_basic_input = ['111111111', '222222222', '333333333',
                                   '444444444', '555555555', '666666666', 
                                   '777777777', '888888888', '999999999']

path_to_advanced_input = "test/input_files/advanced.txt"
accounts_in_advanced_input = ['000000051', '49006771?', '1234?678?', '200000000',
                              '490067715', '?23456789', '0?0000051', '49086771?',]

class TestStoryOne:
    " confirm we can read Accounts from a File "

    def test_story_one_with_basic_input(self):
        " confirm Parser finds Accounts within basic input file "
        numeral_from_figure = Parser(Figure.check, None, None, Figure.numeral_from_figure)
        account_from_entry = Parser(Entry.check, Entry.figures_from_entry, 
                                    numeral_from_figure, account_from_numerals)
        accounts_from_lines = Parser(Lines.check, Lines.entries_from_lines, 
                                     account_from_entry, None)
        accounts_from_stream = Parser(Stream.check, Stream.timmed_lines_from_stream,
                                      accounts_from_lines, None)
        path = path_to_basic_input
        expected = accounts_in_basic_input
        with io.open(path) as stream:
            found = accounts_from_stream.parser(stream)
            assert expected == found

class TestStoryTwo:
    " confirm parser recognizes [in]valididity of Accounts in a File "

    def test_story_one_with_basic_input(self):
        " confirm Parser finds Accounts within basic input file "
        numeral_from_figure = Parser(Figure.check, None, None, Figure.numeral_from_figure)
        account_from_entry = Parser(Entry.check, Entry.figures_from_entry, 
                                    numeral_from_figure, account_from_numerals)
        accounts_from_lines = Parser(Lines.check, Lines.entries_from_lines, 
                                     account_from_entry, None)
        accounts_from_stream = Parser(Stream.check, Stream.timmed_lines_from_stream,
                                      accounts_from_lines, None)
        path = path_to_basic_input
        expected = accounts_in_basic_input
        with io.open(path) as stream:
            found = accounts_from_stream.parser(stream)
            assert expected == found

"""
    def test_main_parses_from_std_in(self, path_and_accounts):
        " confirm Parser.main identifies accounts via std-in "
        path, accounts = path_and_accounts
        with path.open() as input_file:
            output = subprocess.check_output('parser/parser.py', stdin=input_file)
        assert output[:-1] == str(accounts)
"""
