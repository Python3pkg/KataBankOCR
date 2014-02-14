"test the lines_from_path generator"

import pytest

from parse.generators.lines_from_path import lines_from_path

from fixtures import Files

def test_with_bad_path():
    "confirm a bad path raises an expected error"
    lines = lines_from_path('bad_path_string')
    pytest.raises((OSError, IOError,), list, lines)

@pytest.mark.parametrize('file_path, line_count', (
        (Files.Basic.path, Files.Basic.line_count),
        (Files.Advanced.path, Files.Advanced.line_count),))
def test_line_count(file_path, line_count):
    "confirm all lines read"
    expected = line_count
    lines = lines_from_path(file_path)
    found = len(list(lines))
    assert expected == found
