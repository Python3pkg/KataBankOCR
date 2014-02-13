"test the superpositions module"

import pytest
import random

from parse import settings
from parse.superpositions import superpositions_from_figures

import check_function
from input_values import figure_superpositions

function = superpositions_from_figures
valid_figure = random.choice(settings.figures.keys())
adulterants = ['\t', '-', 'I', 'l', '/', '\\', '\r']

test_iterability = check_function.raises_on_non_iterable(function)
test_element_type = check_function.raises_on_bad_element_type(function, valid_figure)
test_element_length = check_function.raises_on_bad_element_length(function, valid_figure)
test_element_composition = check_function.raises_on_bad_element_composition(function, 
                                                                            valid_figure,
                                                                            adulterants)

def test_parses_known_figures_to_superpositions():
    "confirm known figures yield expected superpositions"
    dict_items = figure_superpositions.items()
    figures, superpositions_expected = zip(*dict_items)
    superpositions_found = superpositions_from_figures(figures)
    assert list(superpositions_expected) == list(superpositions_found)
