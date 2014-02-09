"test user stories (from kata.txt)"

import pytest
import subprocess

from test_parser import expected_matches_parsed_path

path_to_basic_input = "test/input_files/basic.txt"
path_to_advanced_input = "test/input_files/advanced.txt"

class TestStoryOne:

    def test_story_one(self):
        "confirm Story One correctly parses Accounts from input"
        accounts_in_basic = ['000000000', '111111111', '222222222', '333333333',
                             '444444444', '555555555', '666666666', '777777777',
                             '888888888', '999999999', '123456789']
        assert expected_matches_parsed_path(expected=accounts_in_basic,
                                            parser_path='parser/story_one.py',
                                            input_path=path_to_basic_input)

class TestStoryTwo:

    def test_story_two(self):
        "confirm Story Two recognizes [in]valididity of Accounts in input"
        valid = ['000000000', '123456789']
        invalid = ['111111111', '222222222', '333333333', '444444444','555555555',
                   '666666666', '777777777', '888888888', '999999999']
        expected_results = str(valid) + '\n' + str(invalid)
        assert expected_matches_parsed_path(expected=expected_results,
                                            parser_path='parser/story_two.py',
                                            input_path=path_to_basic_input)

class TestStoryThree:

    basic_results = ('000000000', '111111111 ERR', '222222222 ERR', '333333333 ERR',
                     '444444444 ERR', '555555555 ERR', '666666666 ERR', '777777777 ERR',
                     '888888888 ERR', '999999999 ERR', '123456789',)
    advanced_results = ('000000051', '49006771? ILL', '1234?678? ILL', '200000000 ERR',
                        '490067715 ERR', '?23456789 ILL', '0?0000051 ILL', '49086771? ILL',)
    @pytest.mark.parametrize('input_path, expected_results',(
            (path_to_basic_input, basic_results),
            (path_to_advanced_input, advanced_results),
            ))
    def test_story_three(self, input_path, expected_results):
        "confirm Story Three correctly labels Account status"
        assert expected_matches_parsed_path(expected='\n'.join(expected_results),
                                            parser_path='parser/story_three.py',
                                            input_path=input_path)

class TestStoryFour:

    basic_results = ['000000000', '111111111 ERR', '222222222 ERR', 
                     '333333333 ERR', '444444444 ERR', '555555555 AMB',
                     '666666666 AMB', '777777177', '888888888 AMB',
                     '999999999 AMB', '123456789']
    advanced_results = ['000000051', '490067715 AMB', '1234?678?', '200000000',
                        '490067715 AMB', '123456789', '000000051', '490867715',]
    @pytest.mark.parametrize('input_path, expected_results',(
            (path_to_basic_input, basic_results),
            (path_to_advanced_input, advanced_results),
            ))
    def test_story_four(self, input_path, expected_results):
        "confirm Story Four correctly determines intended Accounts"
        # TODO: uncomment once Story Four implemented
#        assert expected_matches_parsed_path(expected='\n'.join(expected_results),
#                                            parser_path='parser/story_four.py',
#                                            input_path=input_path)


