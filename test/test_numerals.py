" test the numerals module "

import pytest
import random

import settings
from parser.numerals import numerals_from_figures
from parser.validators import Validate

from common_tools import invalid_lengths, fit_to_length, replace_element
from common_tools import get_unknown_figure
from common_tools import entry_from_account

class TestNumeralsFromFigures:
    " exercise the numerals_from_figures function "

    class TestInput:
        " confirm invalid input raises appropriate error "

        def test_with_non_iterable(self, non_iterable):
            " confirm error raised on non-iterable input "
            entries = numerals_from_figures(non_iterable)
            pytest.raises(TypeError, list, entries)

        def test_with_non_string(self, non_string):
            " confirm error raised on iterable that yields a non_string "
            figures = [non_string,]
            entries = numerals_from_figures(figures)
            pytest.raises(TypeError, list, entries)

        @pytest.fixture(params=invalid_lengths(settings.strokes_per_figure))
        def invalid_figure_length(self, request):
            " return an invalid length for a Figure "
            return request.param

        def test_with_figure_of_invalid_length(self, get_figure, invalid_figure_length):
            " confirm error raised for figure of invalid length "
            invalid_length_figure = fit_to_length(get_figure(), invalid_figure_length)
            entries = numerals_from_figures([invalid_length_figure,])
            pytest.raises(ValueError, list, entries)

        some_non_strokes = {'\t', '-', 'I', 'l', '/', '\\', '\r'}
        all_valid_strokes = settings.valid_strokes
        strokes_in_common = some_non_strokes.intersection(all_valid_strokes)
        assert set() == strokes_in_common

        @pytest.mark.parametrize('non_stroke', some_non_strokes)
        def test_with_figure_containing_invalid_stroke(self, get_figure, non_stroke):
            " confirm error raised for figure containing an invalid stroke "
            adulterated_figure = replace_element(get_figure(), non_stroke)
            entries = numerals_from_figures([adulterated_figure,])
            e = pytest.raises(TypeError, list, entries)
            msg = 'Figure "%s" contains unexpected element "%s" at index'
            msg = msg % (adulterated_figure, non_stroke)
            assert msg in e.value.message

    class TestOutput:
        " confirm valid input results in valid output "

        @pytest.fixture
        def figures(self, get_figure):
            " return an entry's worth of random figures "
            return [get_figure() for i in range(settings.figures_per_entry)]

        def test_returns_iterable(self, figures):
            " confirm iterable "
            numerals = numerals_from_figures(figures)
            Validate.iterable(numerals)

        def test_element_types(self, figures):
            " confirm iterable yields strings "
            numerals = numerals_from_figures(figures)
            Validate.elements('type', basestring, figures, 'Numeral')

        def test_element_lengths(self, figures):
            " confirm iterable yields elements of correct length "
            numerals = numerals_from_figures(figures)
            expected_length = 1
            Validate.elements('length', expected_length, numerals, 'Numeral')

        def test_parses_known_figures_to_numerals(self):
            " confirm known figures recognized correctly "
            figures, numerals = zip(*settings.figures.items())
            expected = numerals
            found = tuple(numerals_from_figures(figures))
            assert expected == found


