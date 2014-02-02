" Test the Figure module "

import pytest
import random

import settings
from parser.errors import InputError, InputTypeError, InputLengthError
from parser.new_figure import NewFigure

from common_tools import invalid_lengths, fit_to_length, adulterate_string
from common_tools import get_unknown_figure

@pytest.fixture(params=settings.figures.keys())
def all_figures(request):
    " Return a valid Figure "
    return request.param

@pytest.fixture
def a_figure(request):
    " Return a valid Figure "
    return random.choice(settings.figures.keys())

figure = a_figure      # Run each test with a random valid Figure
#figure = all_figures  # Run each test with every valid Figure

class TestCheck:
    " test the Figure.check method "

    class TestLength:
        " test the Figure.check method "

        @pytest.fixture(params=invalid_lengths(settings.strokes_per_figure))
        def invalid_figure_length(self, request):
            " return an invalid length for a Figure "
            return request.param

        def test_with_invalid_length_string(self, figure, invalid_figure_length):
            " confirm Figure detects an invalid length input string "
            invalid_length_figure = fit_to_length(figure, invalid_figure_length)
            pytest.raises(InputLengthError, NewFigure.check, invalid_length_figure)

    class TestStrokes:
        " confirm Figure only accepts valid Strokes as input "

        def test_with_non_string(self, non_string):
            " confirm Figure requires a string as its argument "
            pytest.raises(InputTypeError, NewFigure.check, non_string)

        some_non_strokes = ('\t', '-', 'I', 'l', '/', '\\', '\r')
        all_valid_strokes = settings.valid_strokes
        assert set(some_non_strokes).intersection(all_valid_strokes) == set()

        @pytest.fixture(params=some_non_strokes)
        def non_stroke(self, request):
            " return arbitrary non-stroke "
            return request.param

        def test_with_adulterated_string(self, figure, non_stroke):
            " confirm Figure checks input for invalid Strokes "
            adulterated_figure = adulterate_string(figure, non_stroke)
            found_strokes = set(adulterated_figure)
            invalid_strokes = found_strokes - set(settings.valid_strokes)
            sorted_invalid_strokes = sorted(list(invalid_strokes))
            e = pytest.raises(InputError, NewFigure.check, adulterated_figure)
            assert e.value.message == \
                'Figure "%s" ' % adulterated_figure +\
                "contains non-Stroke element(s): %s" % ''.join(sorted_invalid_strokes)

class TestGetNumeral:
    " test the Figure.get_numeral method "

    def test_parses_known_figure_to_numeral(self, figure):
        expected = settings.figures[figure]
        found = NewFigure.get_numeral(figure)
        assert expected == found

    def test_with_unknown_input(self):
        " confirm Figure identifies an unknown string as illegible "
        bad_figure = get_unknown_figure()
        found = NewFigure.get_numeral(bad_figure)
        expected = settings.illegible_numeral
        assert expected == found
        
