"test the lines module"

import pytest

from parse import settings
from parse.lines import lines_from_path

from test_input import Basic, Advanced

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

        @pytest.mark.parametrize('file_path, line_count', ((Basic.path, Basic.line_count),
                                                           (Advanced.path, Advanced.line_count),))
        def test_line_count(self, file_path, line_count):
            "confirm all lines read"
            expected = line_count
            lines = lines_from_path(file_path)
            found = len(list(lines))
            assert expected == found
