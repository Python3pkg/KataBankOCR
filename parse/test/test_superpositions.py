"test the superpositions module"

import pytest
import random

from parse import settings
from parse.superpositions import superpositions_from_figures

import check_function

function = superpositions_from_figures
valid_figure = random.choice(settings.figures.keys())
adulterants = ['\t', '-', 'I', 'l', '/', '\\', '\r']

test_iterability = check_function.raises_on_non_iterable(function)
test_element_type = check_function.raises_on_bad_element_type(function, valid_figure)
test_element_length = check_function.raises_on_bad_element_length(function, valid_figure)
test_element_composition = check_function.raises_on_bad_element_composition(function, 
                                                                            valid_figure,
                                                                            adulterants)

figure_superpositions = {
    ' _ ' +
    '| |' +
    '|_|' +
    '   ': {0: {'0'}, 1: {'8'}, 2: {'6', '9'}, 3: {'2', '3', '5', '7'}, 4:{'1', '4'}},
    '   ' +
    '  |' +
    '  |' +
    '   ': {0: {'1'}, 1: {'7'}, 2: {'4'}, 3: {'3'}, 4: {'0', '9'}, 5: {'2', '5', '8'}, 6: {'6'}},
    ' _ ' +
    ' _|' +
    '|_ ' +
    '   ': {0: {'2'}, 2: {'3', '8'}, 3: {'0', '6', '9'}, 4: {'5', '7'}, 5: {'1', '4'}},
    ' _ ' +
    ' _|' +
    ' _|' +
    '   ': {0: {'3'}, 1: {'9'}, 2: {'2', '5', '7', '8'}, 3: {'0', '1', '4', '6'}},
    '   ' +
    '|_|' +
    '  |' +
    '   ': {0: {'4'}, 2: {'1', '9'}, 3: {'3', '5', '7', '8'}, 4: {'0', '6'}, 5: {'2'}},
    ' _ ' +
    '|_ ' +
    ' _|' +
    '   ': {0: {'5'}, 1: {'6', '9'}, 2: {'3', '8'}, 3: {'0', '4'}, 4: {'2', '7'}, 5: {'1'}},
    ' _ ' +
    '|_ ' +
    '|_|' +
    '   ': {0: {'6'}, 1: {'5', '8'}, 2: {'0', '9'}, 3: {'2', '3'}, 4: {'4'}, 5: {'7'}, 6: {'1'}},
    ' _ ' +
    '  |' +
    '  |' +
    '   ': {0: {'7'}, 1: {'1'}, 2: {'3'}, 3: {'0', '4', '9'}, 4: {'2', '5', '8'}, 5: {'6'}},
    ' _ ' +
    '|_|' +
    '|_|' +
    '   ': {0: {'8'}, 1: {'0', '6', '9'}, 2: {'2', '3', '5'}, 3: {'4'}, 4: {'7'}, 5: {'1'}},
    ' _ ' +
    '|_|' +
    ' _|' +
    '   ': {0: {'9'}, 1: {'3', '5', '8'}, 2: {'0', '4', '6'}, 3: {'2', '7'}, 4: {'1'}},
    '   ' +
    ' _|' +
    '  |' +
    '   ': {1: {'1', '4'}, 2: {'3', '7'}, 3: {'9'}, 4: {'2', '5', '8'}, 5: {'0', '6'}},
    '   ' +
    '| |' +
    '|_|' +
    '   ': {1: {'0'}, 2: {'8'}, 3: {'1', '4', '6', '9'}, 4: {'2', '3', '5', '7'}},
    ' _ ' +
    ' _ ' +
    ' _|' +
    '   ': {1: {'3', '5'}, 2: {'6', '9'}, 3: {'2', '7', '8'}, 4: {'0', '1', '4'}},
    }

def test_parses_known_figures_to_superpositions():
    "confirm known figures yield expected superpositions"
    dict_items = figure_superpositions.items()
    figures, superpositions_expected = zip(*dict_items)
    superpositions_found = superpositions_from_figures(figures)
    assert list(superpositions_expected) == list(superpositions_found)
