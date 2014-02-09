"Test the Figures module"

import pytest

import settings
from parser.figures import figures_from_entries
from parser.validators import Validate

from common_tools import figures_from_account, entry_from_account
from common_tools import flatten
from common_tools import invalid_lengths, fit_to_length, replace_element

class TestFiguresFromEntries:
    "exercise the figures_from_entries function"

    @pytest.fixture
    def entry(self, get_account):
        "Return an Entry that represents a random Account"
        return entry_from_account(get_account())

    class TestInput:
        "confirm invalid input raises appropriate error"

        def test_with_non_list(self, entry, non_string):
            "confirm figures_from_entries detects a non-string"
            entry = replace_element(entry, non_string)
            figures = figures_from_entries([entry,])
            pytest.raises(TypeError, list, figures)

        def test_with_list_containing_a_non_string(self, entry, non_string):
            "confirm detection of a non-string within an entry"
            entry = replace_element(entry, non_string)
            figures = figures_from_entries([entry,])
            pytest.raises(TypeError, list, figures)

        @pytest.fixture(params=invalid_lengths(settings.strokes_per_line))
        def invalid_stroke_count(self, request):
            "return an invalid length for a line"
            return request.param

        def test_with_entry_containing_line_of_invalid_length(self, entry, invalid_stroke_count):
            "confirm detection of an invalid length line within an entry"
            first_line = entry[0]
            line_of_invalid_length = fit_to_length(first_line, invalid_stroke_count)
            entry = replace_element(entry, line_of_invalid_length)
            figures = figures_from_entries([entry,])
            pytest.raises(ValueError, list, figures)

    class TestOutput:
        "confirm valid input results in valid output"

        def test_figures_match(self, get_accounts):
            "confirm figures_from_entries correctly identifies figures"
            number_of_accounts_to_test = settings.approximate_entries_per_file
            accounts = get_accounts()
            figures = map(figures_from_account, accounts)
            expected = flatten(figures)
            entries = map(entry_from_account, accounts)
            found = figures_from_entries(entries)
            assert list(expected) == list(found)

