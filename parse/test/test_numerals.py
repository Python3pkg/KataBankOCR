"test the numerals module"

import pytest
import random

from parse import settings
from parse.numerals import numerals_from_figures

import check_function
 
function = numerals_from_figures
valid_figure = random.choice(settings.figures.keys())
adulterants = ['\t', '-', 'I', 'l', '/', '\\', '\r']

test_iterability = check_function.raises_on_non_iterable(function)
test_element_type = check_function.raises_on_bad_element_type(function, valid_figure)
test_element_length = check_function.raises_on_bad_element_length(function, valid_figure)
test_element_composition = check_function.raises_on_bad_element_composition(function, 
                                                                            valid_figure,
                                                                            adulterants)

def test_parses_known_figures_to_numerals():
    "confirm known figures recognized correctly"
    figures, numerals = zip(*settings.figures.items())
    expected = numerals
    found = tuple(numerals_from_figures(figures))
    assert expected == found

@pytest.fixture
def unknown_figure():
    " return Figure of valid length & Strokes, but no matching Numeral "
    for i in range(100):
        valid_figures = settings.figures.keys()
        strokes = list(random.choice(valid_figures))
        random.shuffle(strokes)
        figure = ''.join(strokes)
        if figure not in valid_figures:
            return figure
    raise ValueError('Failed to generate an unknown figure')

def test_parses_unknown_figures_to_illegible_numeral(unknown_figure):
    "confirm unknown figure yields illegible numeral"
    expected = [settings.illegible_numeral]
    found = list(numerals_from_figures([unknown_figure]))
    assert expected == found
