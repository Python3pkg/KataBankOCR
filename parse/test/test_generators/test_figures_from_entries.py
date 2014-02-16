"test the figures_from_entries generator"

import pytest

from parse import settings
from parse.generators.figures_from_entries import figures_from_entries

from common_tools import flatten, invalid_lengths, fit_to_length, replace_element
import check_generator
import fixtures

test_iterability = check_generator.raises_on_non_iterable(generator=figures_from_entries)

test_element_type = \
    check_generator.raises_on_bad_element_type(generator=figures_from_entries,
                                               value_or_type=fixtures.Entries.get_random())
test_element_length = \
    check_generator.raises_on_bad_element_length(generator=figures_from_entries,
                                                 valid_element=fixtures.Entries.get_random())
test_element_composition = \
    check_generator.raises_on_bad_element_composition(generator=figures_from_entries,
                                                      valid_element=fixtures.Entries.get_random(),
                                                      adulterants=[[], (), 1, False, True, 1.0])

class TestInput:
    "confirm invalid input raises appropriate error"

    @pytest.fixture(params=invalid_lengths(settings.strokes_per_line))
    def invalid_stroke_count(self, request):
        "return an invalid length for a line"
        return request.param

    def test_with_entry_containing_line_of_invalid_length(self, invalid_stroke_count):
        "confirm detection of an invalid length line within an entry"
        entry = fixtures.Entries.get_random()
        first_line = entry[0]
        line_of_invalid_length = fit_to_length(first_line, invalid_stroke_count)
        entry = replace_element(entry, line_of_invalid_length)
        pytest.raises(ValueError, list, figures_from_entries([entry]))

class TestOutput:
    "confirm valid input results in valid output"

    def test_figures_match(self, get_accounts):
        "confirm figures_from_entries correctly identifies figures"
        accounts = fixtures.Accounts.get_random(settings.approximate_entries_per_file)
        expected = flatten(map(fixtures.Figures.from_account, accounts))
        entries = map(fixtures.Entries.from_account, accounts)
        found = figures_from_entries(entries)
        assert list(expected) == list(found)
