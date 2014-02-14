"Test the entries_from_lines generator"

import pytest

from parse import settings
from parse.generators.entries_from_lines import entries_from_lines

import check_generator
 
test_iterability = check_generator.raises_on_non_iterable(generator=entries_from_lines)

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

# TODO: grab lines from fixtures and use those
