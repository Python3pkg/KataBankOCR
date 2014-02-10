"Test the Entries module"

import pytest
import fileinput

from parse import settings
from parse.entries import entries_from_lines
from parse.validators import Validate

import test_input

class TestEntriesFromLines:
    "exercise the entries_from_lines function"

    @pytest.fixture(params=(test_input.Basic.path, test_input.Advanced.path))
    def lines(self, request):
        "return a list of lines for testing"
        path = request.param
        lines = []
        for line in fileinput.input(path):
            lines.append(str(line).rstrip('\n'))
        return lines

    class TestInput:
        "confirm invalid input raises appropriate error"

        def test_with_non_iterable(self, non_iterable):
            "confirm error raised on non-iterable input"
            entries = entries_from_lines(non_iterable)
            pytest.raises(TypeError, list, entries)

        def test_with_insufficient_line_count(self, lines):
            "confirm error raised if EOF within an Entry"
            if settings.lines_per_entry > 1:
                lines = lines[:-1]
                entries = entries_from_lines(lines)
                e = pytest.raises(ValueError, list, entries)
                assert 'File ended mid-Entry.' in e.value.message

    class TestOutput:
        "confirm valid input results in valid output"

        @pytest.mark.parametrize('iterable, groups', (
                ('abcd', [['a', 'b', 'c', 'd']]),
                (['a', 'b', 'c', 'd'], [['a', 'b', 'c', 'd']]),
                ('12345678', [['1', '2', '3', '4'], ['5', '6', '7', '8']]),
                ('abcdefghijklmnop', [['a', 'b', 'c', 'd'],
                                      ['e', 'f', 'g', 'h'],
                                      ['i', 'j', 'k', 'l'],
                                      ['m', 'n', 'o', 'p']]),
                ))
        def test_groupings(self, iterable, groups):
            "confirm iterable elements correctly grouped"
            expected = groups
            found = entries_from_lines(iterable)
            assert expected == list(found)

