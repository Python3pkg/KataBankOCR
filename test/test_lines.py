"test the lines module"

import pytest

from parser import settings
from parser.lines import lines_from_path

path_to_basic = 'test/input_files/basic.txt'
lines_in_basic = 44
path_to_advanced = 'test/input_files/advanced.txt'
lines_in_advanced = 32

class TestLinesFromPath:
    "exercise the lines_from_path function"

    class TestInput:
        "confirm invalid input raises appropriate error"

        def test_with_bad_path(self):
            "confirm a bad path raises an expected error"
            lines = lines_from_path('bad_path_string')
            pytest.raises((OSError, IOError,), list, lines)

    class TestOutput:
        "confirm valid input results in valid output"

        @pytest.mark.parametrize('file_path, line_count', ((path_to_basic, lines_in_basic),
                                                           (path_to_advanced, lines_in_advanced),))
        def test_line_count(self, file_path, line_count):
            "confirm all lines read"
            expected = line_count
            lines = lines_from_path(file_path)
            found = len(list(lines))
            assert expected == found
