"Test the Entries module"

import pytest
import fileinput

from parse import settings
from parse.entries import entries_from_lines
from parse.validators import Validate

import input_files
import check_function
 
function = entries_from_lines

test_iterability = check_function.raises_on_non_iterable(function)

@pytest.mark.parametrize('iterable, groups', (
        ('abcd', [['a', 'b', 'c', 'd']]),
        (['a', 'b', 'c', 'd'], [['a', 'b', 'c', 'd']]),
        ('12345678', [['1', '2', '3', '4'], ['5', '6', '7', '8']]),
        ('abcdefghijklmnop', [['a', 'b', 'c', 'd'],
                              ['e', 'f', 'g', 'h'],
                              ['i', 'j', 'k', 'l'],
                              ['m', 'n', 'o', 'p']]),
        ))
def test_groupings(iterable, groups):
    "confirm iterable elements correctly grouped"
    expected = groups
    found = entries_from_lines(iterable)
    assert expected == list(found)
