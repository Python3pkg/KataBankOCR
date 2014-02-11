"Test the Figures module"

import pytest

from parse import settings
from parse.figures import figures_from_entries

from common_tools import figures_from_account, entry_from_account, flatten
from common_tools import invalid_lengths, fit_to_length, replace_element
import check_function

function = figures_from_entries
semi_valid_entry = ['', '', '', '']   # 'semi' because not checking line length here
adulterants = [[], (), 1, False, True, 1.0]

test_iterability = check_function.raises_on_non_iterable(function)
test_element_type = check_function.raises_on_bad_element_type(function, semi_valid_entry)
test_element_length = check_function.raises_on_bad_element_length(function, semi_valid_entry)
test_element_composition = check_function.raises_on_bad_element_composition(function, 
                                                                            semi_valid_entry,
                                                                            adulterants)

class TestFiguresFromEntries:
    "exercise the figures_from_entries function"

    @pytest.fixture
    def entry(self, get_account):
        "Return an Entry that represents a random Account"
        return entry_from_account(get_account())

    class TestInput:
        "confirm invalid input raises appropriate error"

        @pytest.fixture(params=invalid_lengths(settings.strokes_per_line))
        def invalid_stroke_count(self, request):
            "return an invalid length for a line"
            return request.param

        def test_with_entry_containing_line_of_invalid_length(self, entry, invalid_stroke_count):
            "confirm detection of an invalid length line within an entry"
            first_line = entry[0]
            line_of_invalid_length = fit_to_length(first_line, invalid_stroke_count)
            entry = replace_element(entry, line_of_invalid_length)
            figures = figures_from_entries([entry])
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
