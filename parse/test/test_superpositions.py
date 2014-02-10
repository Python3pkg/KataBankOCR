"test the superpositions module"

import pytest
import random

from parse import settings
from parse.superpositions import superpositions_from_figures

from common_tools import invalid_lengths, fit_to_length, replace_element

class TestSuperpositionsFromFigures:
    "exercise the superpositions_from_figures function"

    class TestInput:
        "confirm invalid input raises appropriate error"

        def test_with_non_iterable(self, non_iterable):
            "confirm error raised on non-iterable input"
            entries = superpositions_from_figures(non_iterable)
            pytest.raises(TypeError, list, entries)

        def test_with_non_string(self, non_string):
            "confirm error raised on iterable that yields a non_string"
            figures = [non_string]
            entries = superpositions_from_figures(figures)
            pytest.raises(TypeError, list, entries)

        @pytest.fixture(params=invalid_lengths(settings.strokes_per_figure))
        def invalid_figure_length(self, request):
            "return an invalid length for a Figure"
            return request.param

        def test_with_figure_of_invalid_length(self, get_figure, invalid_figure_length):
            "confirm error raised for figure of invalid length"
            invalid_length_figure = fit_to_length(get_figure(), invalid_figure_length)
            entries = superpositions_from_figures([invalid_length_figure])
            pytest.raises(ValueError, list, entries)

        some_non_strokes = {'\t', '-', 'I', 'l', '/', '\\', '\r'}
        all_valid_strokes = settings.valid_strokes
        strokes_in_common = some_non_strokes.intersection(all_valid_strokes)
        assert set() == strokes_in_common

        @pytest.mark.parametrize('non_stroke', some_non_strokes)
        def test_with_figure_containing_invalid_stroke(self, get_figure, non_stroke):
            "confirm error raised for figure containing an invalid stroke"
            adulterated_figure = replace_element(get_figure(), non_stroke)
            entries = superpositions_from_figures([adulterated_figure])
            e = pytest.raises(TypeError, list, entries)
            message = 'Figure "%s" contains unexpected element "%s" at index'
            message = message % (adulterated_figure, non_stroke)
            assert message in e.value.message

    class TestOutput:
        "confirm valid input results in valid output"

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

        def test_parses_known_figures_to_superpositions(self):
            "confirm known figures yield expected superpositions"
            dict_items = self.figure_partial_superpositions.items()
            figures, partial_superpositions_expected = zip(*dict_items)
            superpositions_found = superpositions_from_figures(figures)
            parial_superpositions_found = map(self._partial_superposition, superpositions_found)
            assert list(partial_superpositions_expected) == list(parial_superpositions_found)

        def _partial_superposition(self, superposition):
            "return superposition limited to 2 or fewer stroke differences"
            return dict([(k, v) for (k, v) in superposition.items() if k <= 2])
