"test the numerals_froms_figures generator"

from parse import settings
from parse.generators.numerals_from_figures import numerals_from_figures

import check_generator
import fixtures

test_iterability = check_generator.raises_on_non_iterable(generator=numerals_from_figures)

test_element_type = \
    check_generator.raises_on_bad_element_type(generator=numerals_from_figures,
                                               value_or_type=fixtures.Figures.get_random())
test_element_length = \
    check_generator.raises_on_bad_element_length(generator=numerals_from_figures,
                                                 valid_element=fixtures.Figures.get_random())
test_element_composition = \
    check_generator.raises_on_bad_element_composition(generator=numerals_from_figures,
                                                      valid_element=fixtures.Figures.get_random(),
                                                      adulterants=['\t', '-', 'I', 'l', '/', '\r'])

def test_valid_figures_yield_valid_numerals():
    "confirm valid figures recognized correctly"
    expected = fixtures.Numerals.valid()
    found = list(numerals_from_figures(fixtures.Figures.valid()))
    assert expected == found

def test_flawed_figures_yield_illegible_numerals():
    "confirm flawed figures yield illegible numerals"
    expected = [settings.illegible_numeral] * len(fixtures.Figures.flawed())
    found = list(numerals_from_figures(fixtures.Figures.flawed()))
    assert expected == found
