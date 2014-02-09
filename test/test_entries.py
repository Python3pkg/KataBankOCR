"Test the Entries module"

import pytest
import fileinput

import settings
from parser.entries import entries_from_lines
from parser.validators import Validate

class TestEntriesFromLines:
    "exercise the entries_from_lines function"

    path_to_basic = 'test/input_files/basic.txt'
    path_to_advanced = 'test/input_files/advanced.txt'
    @pytest.fixture(params=(path_to_basic, path_to_advanced,))
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

