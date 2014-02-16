"Test the entries_from_lines generator"

import pytest

from parse.generators.entries_from_lines import entries_from_lines

import check_generator
import fixtures

test_iterability = check_generator.raises_on_non_iterable(generator=entries_from_lines)

def test_known_lines_grouped_to_known_entries():
    "confirm known lines grouped into known entries"
    expected = fixtures.Entries.of_basic_input_file()
    lines = fixtures.Lines.of_basic_input_file()
    found = entries_from_lines(lines)
    assert expected == list(found)

def test_insufficient_line_count_raises_expected_error():
    "confirm a truncated list of lines raises appropriate error"
    expected = fixtures.Entries.of_basic_input_file()
    lines = fixtures.Lines.of_basic_input_file()
    lines = lines[:-1]
    entries = entries_from_lines(lines)
    pytest.raises(ValueError, list, entries)
    message = 'File ended mid-entry'
