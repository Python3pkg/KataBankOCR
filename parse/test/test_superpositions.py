"test the superpositions_from_figures generator"

from parse.superpositions import superpositions_from_figures as generator

import check_generator
from fixtures import Figures, Superpositions

figure = Figures.get_random()
adulterants = ['\t', '-', 'I', 'l', '/', '\\', '\r']

test_iterability = check_generator.raises_on_non_iterable(generator)
test_element_type = check_generator.raises_on_bad_element_type(generator, figure)
test_element_length = check_generator.raises_on_bad_element_length(generator, figure)
test_element_composition = check_generator.raises_on_bad_element_composition(generator, 
                                                                            figure,
                                                                            adulterants)

def test_parses_valid_figures_to_superpositions():
    "confirm known figures yield expected superpositions"
    expected = Superpositions.of_valid_figures()
    found = generator(Figures.valid())
    assert list(expected) == list(found)

def test_parses_flawed_figures_to_superpositions():
    "confirm known figures yield expected superpositions"
    expected = Superpositions.from_flawed_figures()
    found = generator(Figures.flawed())
    assert list(expected) == list(found)

