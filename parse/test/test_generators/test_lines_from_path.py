"test the lines_from_path generator"

import pytest

from parse.generators.lines_from_path import lines_from_path

import input_files

def test_with_bad_path():
    "confirm a bad path raises an expected error"
    lines = lines_from_path('bad_path_string')
    pytest.raises((OSError, IOError,), list, lines)

@pytest.mark.parametrize('file_path, line_count', (
        (input_files.Basic.path, input_files.Basic.line_count),
        (input_files.Advanced.path, input_files.Advanced.line_count),
        ))
def test_line_count(file_path, line_count):
    "confirm all Lines read"
    expected = line_count
    lines = list(lines_from_path(file_path))
    found = len(lines)
    assert expected == found
