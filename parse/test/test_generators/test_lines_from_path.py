"test the lines_from_path generator"

import pytest

from parse import settings
from parse.generators.lines_from_path import lines_from_path

import fixtures

def test_with_bad_path():
    "confirm a bad path raises an expected error"
    lines = lines_from_path('bad_path_string')
    pytest.raises((OSError, IOError,), list, lines)

def test_line_count():
    "confirm all Lines read"
    accounts = fixtures.Accounts.of_basic_input_file()
    line_count = len(accounts) * settings.lines_per_entry
    expected = line_count
    path = fixtures.Paths.basic_input_file()
    lines = lines_from_path(path)
    found = len(list(lines))
    assert expected == found
