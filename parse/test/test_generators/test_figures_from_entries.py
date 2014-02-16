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

test_element_composition = check_generator.raises_on_bad_element_composition(
    generator=figures_from_entries,
    valid_element=fixtures.Entries.get_random(),
    adulterants=fixtures.ArbitraryValues.non_basestring()
    )

@pytest.fixture(params=invalid_lengths(settings.strokes_per_line))
def invalid_stroke_count(request):
    "return an invalid length for a Line"
    return request.param

def test_raises_on_entry_with_line_of_invalid_length(invalid_stroke_count):
    "confirm detection of an invalid length Line within an Entry"
    entry = fixtures.Entries.get_random()
    first_line = entry[0]
    line_of_invalid_length = fit_to_length(first_line, invalid_stroke_count)
    entry = replace_element(entry, line_of_invalid_length)
    iterator = figures_from_entries([entry])
    error = pytest.raises(ValueError, list, iterator)
    for message in ('Entry Line', 'of unexpected length', 'Expected:', 'Found:'):
        assert message in error.value.message

def test_figures_match():
    "confirm figures_from_entries correctly identifies Figures"
    accounts = fixtures.Accounts.get_random(settings.approximate_entries_per_file)
    expected_figures = flatten(map(fixtures.Figures.from_account, accounts))
    entries = map(fixtures.Entries.from_account, accounts)
    found_figures = figures_from_entries(entries)
    assert list(expected_figures) == list(found_figures)
