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

figure_partial_superpositions = {
    ' _ ' +
    '| |' +
    '|_|' +
    '   ': {0: {'0'}, 1: {'8'}, 2: {'6', '9'}},
    '   ' +
    '  |' +
    '  |' +
    '   ': {0: {'1'}, 1: {'7'}, 2: {'4'}},
    ' _ ' +
    ' _|' +
    '|_ ' +
    '   ': {0: {'2'}, 2: {'3', '8'}},
    ' _ ' +
    ' _|' +
    ' _|' +
    '   ': {0: {'3'}, 1: {'9'}, 2: {'2', '5', '7', '8'}},
    '   ' +
    '|_|' +
    '  |' +
    '   ': {0: {'4'}, 2: {'1', '9'}},
    ' _ ' +
    '|_ ' +
    ' _|' +
    '   ': {0: {'5'}, 1: {'6', '9'}, 2: {'3', '8'}},
    ' _ ' +
    '|_ ' +
    '|_|' +
    '   ': {0: {'6'}, 1: {'5', '8'}, 2: {'0', '9'}},
    ' _ ' +
    '  |' +
    '  |' +
    '   ': {0: {'7'}, 1: {'1'}, 2: {'3'}},
    ' _ ' +
    '|_|' +
    '|_|' +
    '   ': {0: {'8'}, 1: {'0', '6', '9'}, 2: {'2', '3', '5'}},
    ' _ ' +
    '|_|' +
    ' _|' +
    '   ': {0: {'9'}, 1: {'3', '5', '8'}, 2: {'0', '4', '6'}},}

def test_parses_known_figures_to_superpositions():
    "confirm known figures yield expected superpositions"
    dict_items = figure_partial_superpositions.items()
    figures, partial_superpositions_expected = zip(*dict_items)
    superpositions_found = superpositions_from_figures(figures)
    parial_superpositions_found = map(_partial_superposition, superpositions_found)
    assert list(partial_superpositions_expected) == list(parial_superpositions_found)

def _partial_superposition(superposition):
    "return superposition limited to 2 or fewer stroke differences"
    return dict([(k, v) for (k, v) in superposition.items() if k <= 2])
