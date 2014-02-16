"test the superpositions_from_figures generator"

from parse.generators.superpositions_from_figures import superpositions_from_figures

import check_generator
import fixtures

test_iterability = check_generator.raises_on_non_iterable(generator=superpositions_from_figures)
test_element_type = \
    check_generator.raises_on_bad_element_type(generator=superpositions_from_figures,
                                               value_or_type=fixtures.Figures.get_random())
test_element_length = \
    check_generator.raises_on_bad_element_length(generator=superpositions_from_figures,
                                                 valid_element=fixtures.Figures.get_random())
test_element_composition = \
    check_generator.raises_on_bad_element_composition(generator=superpositions_from_figures,
                                                      valid_element=fixtures.Figures.get_random(),
                                                      adulterants=['\t', '-', 'I', 'l', '/', '\r'])

def test_parses_valid_figures_to_superpositions():
    "confirm known figures yield expected superpositions"
    expected = fixtures.Superpositions.of_valid_figures()
    found = superpositions_from_figures(fixtures.Figures.valid())
    assert list(expected) == list(found)

def test_parses_flawed_figures_to_superpositions():
    "confirm known figures yield expected superpositions"
    expected = fixtures.Superpositions.from_flawed_figures()
    found = superpositions_from_figures(fixtures.Figures.flawed())
    assert list(expected) == list(found)
