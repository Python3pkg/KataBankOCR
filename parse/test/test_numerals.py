"test the numerals module"

import pytest
import random

from parse import settings
from parse.numerals import numerals_from_figures as generator

from fixtures import Figures, Numerals
import check_generator

figure = Figures.get_random()
adulterants = ['\t', '-', 'I', 'l', '/', '\\', '\r']

test_iterability = check_generator.raises_on_non_iterable(generator)
test_element_type = check_generator.raises_on_bad_element_type(generator, figure)
test_element_length = check_generator.raises_on_bad_element_length(generator, figure)
test_element_composition = check_generator.raises_on_bad_element_composition(generator, 
                                                                            figure,
                                                                            adulterants)

def test_valid_figures_yield_valid_numerals():
    "confirm valid figures recognized correctly"
    expected = Numerals.valid()
    found = list(generator(Figures.valid()))
    assert expected == found

def test_flawed_figures_yield_illegible_numerals():
    "confirm flawed figures yield illegible numerals"
    expected = [settings.illegible_numeral] * len(Figures.flawed())
    found = list(generator(Figures.flawed()))
    assert expected == found
