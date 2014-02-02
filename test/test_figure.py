import pytest
import random 
import copy
import mock

import settings
from parser.errors import InputError, InputTypeError, InputLengthError
from parser.figure import Figure
from parser import figure

from common_tools import invalid_lengths, fit_to_length, adulterate_string
from common_tools import get_unknown_figure

class TestFigure:
    " test the Figure class "

    @pytest.fixture
    def figure(self):
        " Return a randomly selected valid Figure "
        all_valid_figures = settings.figures.keys()
        return random.choice(all_valid_figures)

    class TestInit:
        " test figure instantiation "
        
        def test_instantiation_with_no_argument(self):
            " confirm Figure require more than zero arguments "
            pytest.raises(TypeError, Figure)

        @pytest.mark.parametrize('arg_count', range(2, 20))
        def test_instantiation_with_multiple_arguments(self, arg_count):
            " confirm Figure requires fewer than 2 arguments "
            pytest.raises(TypeError, Figure, *range(arg_count))

        def test_instantiation_with_single_non_string_argument(self, non_string):
            " confirm Figure instantiates with a single argument "
            with mock.patch.object(Figure, '_validate_input'):
                with mock.patch.object(Figure, '_to_numeral'):
                     assert isinstance(Figure(non_string), Figure)

        def test_with_non_string(self, non_string):
            " confirm Figure requires a string as its argument "
            pytest.raises(InputTypeError, Figure, non_string)

    class TestLength:
        " confirm Figure validates the length of its input "

        @pytest.fixture(params=invalid_lengths(settings.strokes_per_figure))
        def invalid_figure_length(self, request):
            " return an invalid length for a Figure "
            return request.param

        @pytest.fixture
        def invalid_length_figure(self, figure, invalid_figure_length):
            " return a Figure of invalid length "
            return fit_to_length(figure, invalid_figure_length)

        def test_with_invalid_length_string(self, invalid_figure_length):
            " confirm Figure detects an invalid length input string "
            invalid_length_figure = '.' * invalid_figure_length
            pytest.raises(InputLengthError, Figure, invalid_length_figure)

    class TestUnknown:
        " confirm Figure identifies unknown input "

        def test_with_unknown_input(self):
            " confirm Figure identifies an unknown string as illegible "
            assert Figure(get_unknown_figure()).numeral == settings.illegible_numeral

    class TestStrokes:
        " confirm Figure only accepts valid Strokes as input "

        some_non_strokes = ('\t', '-', 'I', 'l', '/', '\\', '\r')
        all_valid_strokes = settings.valid_strokes
        assert set(some_non_strokes).intersection(all_valid_strokes) == set()
        @pytest.fixture(params=some_non_strokes)
        def non_stroke(self, request):
            " return arbitrary non-stroke "
            return request.param

        @pytest.fixture
        def adulterated_figure(self, figure, non_stroke):
            " return Figure containing an invalid stroke "
            return adulterate_string(figure, non_stroke)

        def test_with_adulterated_string(self, adulterated_figure):
            " confirm Figure checks input for invalid Strokes "
            invalid_strokes = set(adulterated_figure) - set(settings.valid_strokes)
            invalid_strokes = sorted(list(invalid_strokes))
            e = pytest.raises(InputError, Figure, adulterated_figure)
            assert e.value.message == \
                'Figure "%s" ' % adulterated_figure +\
                "contains non-Stroke element(s): %s" % ''.join(invalid_strokes)

    class TestFunctionality:
        " confirm Figure resolves a known figure to its numeral "

        def test_parse_known_figure_to_numeral(self, figure):
            expected = settings.figures[figure]
            found = Figure(figure).numeral
            assert expected == found

