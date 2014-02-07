" Test user stories (from kata.txt) "

import pytest
import subprocess

path_to_basic_input = "test/input_files/basic.txt"
path_to_advanced_input = "test/input_files/advanced.txt"

class TestStoryOne:

    def test_story_one(self):
        " confirm story one parses Accounts from StdIn "
        accounts_in_basic_input = ['000000000', '111111111', '222222222', '333333333',
                                   '444444444', '555555555', '666666666', '777777777',
                                   '888888888', '999999999', '123456789']
        expected = str(accounts_in_basic_input) + '\n'
        with open(path_to_basic_input) as input_file:
            found = subprocess.check_output('parser/story_one.py', stdin=input_file)
        assert expected == found

class TestStoryTwo:

    def test_story_two(self):
        " confirm story two recognizes [in]valididity of Accounts "
        valid_accounts_in_basic_input = ['000000000', '123456789',]
        invalid_accounts_in_basic_input = ['111111111', '222222222', '333333333',
                                           '444444444', '555555555', '666666666', 
                                           '777777777', '888888888', '999999999']
        expected = str(valid_accounts_in_basic_input) + '\n' +\
            str(invalid_accounts_in_basic_input) + '\n'
        with open(path_to_basic_input) as input_file:
            found = subprocess.check_output('parser/story_two.py', stdin=input_file)
        assert expected == found

class TestStoryThree:

    def test_story_three_with_basic_input(tmpdir):
        " confirm story three parses Results from basic input file "
        results_in_basic_input = ['000000000', '111111111 ERR', '222222222 ERR', 
                                  '333333333 ERR', '444444444 ERR', '555555555 ERR',
                                  '666666666 ERR', '777777777 ERR', '888888888 ERR',
                                  '999999999 ERR', '123456789']
        expected = str(results_in_basic_input) + '\n'
        with open(path_to_basic_input) as input_file:
            found = subprocess.check_output('parser/story_three.py', stdin=input_file)
        assert expected == found

    def test_story_three_with_advanced_input(tmpdir):
        " confirm story three parses Results from advanced input file "
        results_in_advanced_input = ['000000051', '49006771? ILL', '1234?678? ILL',
                                     '200000000 ERR', '490067715 ERR', '?23456789 ILL',
                                     '0?0000051 ILL', '49086771? ILL',]
        expected = str(results_in_advanced_input) + '\n'
        with open(path_to_advanced_input) as input_file:
            found = subprocess.check_output('parser/story_three.py', stdin=input_file)
        assert expected == found


class TestStoryFour:
    # TODO: Implement
    
    def test_story_four_with_basic_input(tmpdir):
        " confirm story four parses Results from basic input file "
        results_in_basic_input = ['000000000', '111111111 ERR', '222222222 ERR', 
                                  '333333333 ERR', '444444444 ERR', '555555555 AMB',
                                  '666666666 AMB', '777777177', '888888888 AMB',
                                  '999999999 AMB', '123456789']
        expected = str(results_in_basic_input) + '\n'
        with open(path_to_basic_input) as input_file:
            found = subprocess.check_output('parser/parser.py', stdin=input_file)
#        assert expected == found

        results_in_advanced_input = ['000000051', '490067715 AMB', '1234?678?', '200000000',
                                     '490067715 AMB', '123456789', '000000051', '490867715',]

    

