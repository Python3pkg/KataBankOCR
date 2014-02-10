"test the numerals module"

import pytest
import random

from parse import settings
from parse.numerals import numerals_from_figures

from common_tools import invalid_lengths, fit_to_length, replace_element

class TestNumeralsFromFigures:
    "exercise the numerals_from_figures function"

    class TestInput:
        "confirm expected error raised by invalid input"

        def test_with_non_iterable(self, non_iterable):
            "confirm error raised on non-iterable input"
            entries = numerals_from_figures(non_iterable)
            pytest.raises(TypeError, list, entries)

        def test_with_non_string(self, non_string):
            "confirm error raised on iterable that yields a non_string"
            figures = [non_string]
            entries = numerals_from_figures(figures)
            pytest.raises(TypeError, list, entries)

        @pytest.fixture(params=invalid_lengths(settings.strokes_per_figure))
        def invalid_figure_length(self, request):
            "return an invalid length for a Figure"
            return request.param

        def test_with_figure_of_invalid_length(self, get_figure, invalid_figure_length):
            "confirm error raised for figure of invalid length"
            invalid_length_figure = fit_to_length(get_figure(), invalid_figure_length)
            entries = numerals_from_figures([invalid_length_figure])
            pytest.raises(ValueError, list, entries)

        some_non_strokes = {'\t', '-', 'I', 'l', '/', '\\', '\r'}
        all_valid_strokes = settings.valid_strokes
        strokes_in_common = some_non_strokes.intersection(all_valid_strokes)
        assert set() == strokes_in_common

        @pytest.mark.parametrize('non_stroke', some_non_strokes)
        def test_with_figure_containing_invalid_stroke(self, get_figure, non_stroke):
            "confirm error raised for figure containing an invalid stroke"
            adulterated_figure = replace_element(get_figure(), non_stroke)
            entries = numerals_from_figures([adulterated_figure])
            e = pytest.raises(TypeError, list, entries)
            message = 'Figure "%s" contains unexpected element "%s" at index'
            message = message % (adulterated_figure, non_stroke)
            assert message in e.value.message

    class TestOutput:
        "confirm expected output from known valid input"

        def test_parses_known_figures_to_numerals(self):
            "confirm known figures recognized correctly"
            figures, numerals = zip(*settings.figures.items())
            expected = numerals
            found = tuple(numerals_from_figures(figures))
            assert expected == found

        @pytest.fixture
        def unknown_figure(self):
            " return Figure of valid length & Strokes, but no matching Numeral "
            for i in range(100):
                valid_figures = settings.figures.keys()
                strokes = list(random.choice(valid_figures))
                random.shuffle(strokes)
                figure = ''.join(strokes)
                if figure not in valid_figures:
                    return figure
            raise ValueError('Failed to generate an unknown figure')

        def test_parses_unknown_figures_to_illegible_numeral(self, unknown_figure):
            "confirm unknown figure yields illegible numeral"
            expected = [settings.illegible_numeral]
            found = list(numerals_from_figures([unknown_figure]))
            assert expected == found
