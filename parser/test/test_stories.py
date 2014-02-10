"test user stories (from kata.txt)"

import pytest

from parser import settings
from parser.lines import lines_from_path
from parser.entries import entries_from_lines
from parser.figures import figures_from_entries
from parser.numerals import numerals_from_figures
from parser.accounts import accounts_from_numerals
from parser.results import results_from_accounts

from test_input import Basic, Advanced

def accounts_from_path(path):
    "return Accounts from input file at Path"
    lines = lines_from_path(path)
    entries = entries_from_lines(lines)
    figures = figures_from_entries(entries)
    numerals = numerals_from_figures(figures)
    accounts = accounts_from_numerals(numerals)
    return accounts

class TestStoryOne:

    def test_story_one(self):
        "confirm Accounts from path match expectations"
        expected = Basic.accounts
        found = list(accounts_from_path(Basic.path))
        assert expected == found

class TestStoryTwo:

    def test_story_two(self):
        "confirm checksum recognizes [in]valididity of Accounts in input"
        expected = Basic.valid_accounts, Basic.invalid_accounts
        accounts = list(accounts_from_path(Basic.path))
        valid = lambda a: settings.checksum(a)
        invalid = lambda a: not valid(a)
        found = filter(valid, accounts), filter(invalid, accounts)
        assert expected == found

class TestStoryThree:

    @pytest.mark.parametrize('input_path, expected_results', (
            (Basic.path, Basic.story_three_results),
            (Advanced.path, Advanced.story_three_results),
            ))
    def test_story_three(self, input_path, expected_results):
        "confirm Story Three correctly labels Account status"
        accounts = accounts_from_path(input_path)
        found_results = list(results_from_accounts(accounts))
        assert expected_results == found_results

class TestStoryFour:

    @pytest.mark.parametrize('input_path, expected_results', (
            (Basic.path, Basic.story_four_results),
            (Advanced.path, Advanced.story_four_results),
            ))
    def test_story_four(self, input_path, expected_results):
        "confirm Story Four correctly determines likely intended Accounts"
        # TODO: Implement
