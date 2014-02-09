"test user stories (from kata.txt)"

import pytest

import settings
from parser.lines import lines_from_path
from parser.entries import entries_from_lines
from parser.figures import figures_from_entries
from parser.numerals import numerals_from_figures
from parser.accounts import accounts_from_numerals
from parser.results import results_from_accounts

def accounts_from_path(path):
    "return Accounts from input file at Path"
    lines = lines_from_path(path)
    entries = entries_from_lines(lines)
    figures = figures_from_entries(entries)
    numerals = numerals_from_figures(figures)
    accounts = accounts_from_numerals(numerals)
    return accounts

path_to_basic_input = "test/input_files/basic.txt"
path_to_advanced_input = "test/input_files/advanced.txt"

class TestStoryOne:

    def test_story_one(self):
        "confirm Accounts from path match expectations"
        expected = ['000000000', '111111111', '222222222', '333333333',
                    '444444444', '555555555', '666666666', '777777777',
                    '888888888', '999999999', '123456789']
        found = list(accounts_from_path(path_to_basic_input))
        assert expected == found

class TestStoryTwo:

    def test_story_two(self):
        "confirm checksum recognizes [in]valididity of Accounts in input"
        expected_valid = ['000000000', '123456789']
        expected_invalid = ['111111111', '222222222', '333333333', '444444444', '555555555',
                            '666666666', '777777777', '888888888', '999999999']
        accounts = list(accounts_from_path(path_to_basic_input))
        found_valid = filter(settings.checksum, accounts)
        found_invalid = filter(lambda a: not settings.checksum(a), accounts)
        assert (expected_valid, expected_invalid) == (found_valid, found_invalid)

class TestStoryThree:

    basic_results = ['000000000', '111111111 ERR', '222222222 ERR', '333333333 ERR',
                     '444444444 ERR', '555555555 ERR', '666666666 ERR', '777777777 ERR',
                     '888888888 ERR', '999999999 ERR', '123456789']
    advanced_results = ['000000051', '49006771? ILL', '1234?678? ILL', '200000000 ERR',
                        '490067715 ERR', '?23456789 ILL', '0?0000051 ILL', '49086771? ILL']
    @pytest.mark.parametrize('input_path, expected_results', (
            (path_to_basic_input, basic_results),
            (path_to_advanced_input, advanced_results),
            ))
    def test_story_three(self, input_path, expected_results):
        "confirm Story Three correctly labels Account status"
        accounts = accounts_from_path(input_path)
        found_results = list(results_from_accounts(accounts))
        assert expected_results == found_results

class TestStoryFour:

    basic_results = ['000000000', '111111111 ERR', '222222222 ERR',
                     '333333333 ERR', '444444444 ERR', '555555555 AMB',
                     '666666666 AMB', '777777177', '888888888 AMB',
                     '999999999 AMB', '123456789']
    advanced_results = ['000000051', '490067715 AMB', '1234?678?', '200000000',
                        '490067715 AMB', '123456789', '000000051', '490867715']
    @pytest.mark.parametrize('input_path, expected_results', (
            (path_to_basic_input, basic_results),
            (path_to_advanced_input, advanced_results),
            ))
    def test_story_four(self, input_path, expected_results):
        "confirm Story Four correctly determines intended Accounts"
        # TODO: Implement
