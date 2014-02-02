import pytest
import mock
import subprocess

import settings
from parser.parser import Parser

from common_tools import file_path_from_entries
from common_tools import entry_from_account

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
        path = path_to_basic_input
        expected = accounts_in_basic_input
        found = Parser(path).accounts
        assert expected == found

class TestStoryTwo:
    " confirm parser recognizes [in]valididity of Accounts in a File "

    def test_story_two_with_basic_input(self):
        " confirm Parser finds Accounts within basic in file "
        path = path_to_basic_input
        accounts = Parser(path).accounts
        for account in accounts:
            valid = settings.checksum(account)
            if valid:
                assert account in valid_accounts_in_basic_input
            else:
                assert account in invalid_accounts_in_basic_input

"""
    def test_main_parses_from_std_in(self, path_and_accounts):
        " confirm Parser.main identifies accounts via std-in "
        path, accounts = path_and_accounts
        with path.open() as input_file:
            output = subprocess.check_output('parser/parser.py', stdin=input_file)
        assert output[:-1] == str(accounts)
"""
