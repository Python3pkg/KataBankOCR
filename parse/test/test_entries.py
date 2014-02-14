"Test the Entries module"

import pytest

from parse import settings
from parse.entries import entries_from_lines as generator

import check_generator
 
test_iterability = check_generator.raises_on_non_iterable(generator)

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
    found = generator(iterable)
    assert expected == list(found)

# TODO: grab lines from fixtures and use those
