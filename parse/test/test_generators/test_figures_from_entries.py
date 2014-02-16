"test the figures_from_entries generator"

import pytest

from parse.generators.figures_from_entries import figures_from_entries

from common_tools import adulterate_iterable
import check_generator
import fixtures

test_iterability = check_generator.raises_on_non_iterable(generator=figures_from_entries)

test_element_type = \
    check_generator.raises_on_bad_element_type(generator=figures_from_entries,
                                               value_or_type=fixtures.Entries.get_random())

test_element_length = \
    check_generator.raises_on_bad_element_length(generator=figures_from_entries,
                                                 valid_element=fixtures.Entries.get_random())

def _raises_on_faulty_line(fault, faulty_lines):
    "return test of error raised on invalid Line within Entry"
    def line_test():
        for line in faulty_lines:
            adulterated_entry = adulterate_iterable(fixtures.Entries.get_random(), line)
            iterator = figures_from_entries([adulterated_entry])
            error = pytest.raises((ValueError, TypeError), list, iterator)
            for message in ('Entry Line', fault):
                assert message in error.value.message
    return line_test

test_line_type = _raises_on_faulty_line(fault='of unexpected type',
                                        faulty_lines=fixtures.Lines.of_invalid_types())

test_line_legth = _raises_on_faulty_line(fault='of unexpected length',
                                         faulty_lines=fixtures.Lines.of_invalid_lengths())

test_line_compositions = _raises_on_faulty_line(fault='contains unexpected element',
                                                faulty_lines=fixtures.Lines.with_invalid_strokes())

def test_identifies_known_entries_as_expected_figures():
    "confirm figures_from_entries correctly identifies Figures"
    account = fixtures.Accounts.get_random()
    expected_figures = fixtures.Figures.from_account(account)
    entry = fixtures.Entries.from_account(account)
    found_figures = figures_from_entries([entry])
    assert list(expected_figures) == list(found_figures)
