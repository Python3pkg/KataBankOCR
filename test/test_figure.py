import pytest
import random 

import settings
from parser.errors import InputError, InputTypeError, InputLengthError
from parser.figure import Figure

from common_tools import invalid_lengths, fit_string_to_length, adulterate_string
from common_tools import get_unknown_figure_string

class TestFigure:
    " test the Figure class "

    class TestInit:
        " test figure instantiation "
        
        def test_with_no_argument(self):
            " confirm Figure require more than zero arguments "
            pytest.raises(TypeError, Figure)

        @pytest.mark.parametrize('arg_count', range(2, 20))
        def test_with_multiple_arguments(self, arg_count):
            " confirm Figure requires fewer than 2 arguments "
            pytest.raises(TypeError, Figure, *range(arg_count))

        def test_with_valid_string(self):
            " confirm Figure instantiates with a valid string argument "
            figure_string = random.choice(settings.figures.keys())
            assert isinstance(Figure(figure_string), Figure)

    class TestInputType:
        " confirm Figure validates the type of its input "

        @pytest.mark.parametrize('non_string',(0, 1, -10, False, True,
                                               [], (), {}, set(), 3.14159))
        def test_with_non_string(self, non_string):
            " confirm Figure requires a string as its argument "
            e = pytest.raises(InputTypeError, Figure, non_string)
            assert e.value.message == "Figure input of unexpected type. " +\
                "expected:<type 'str'>. found:%s." % type(non_string)

    class TestInputLength:
        " confirm Figure validates the length of its input "

        @pytest.fixture(params=invalid_lengths(settings.figure_length))
        def invalid_figure_string_length(self, request):
            " return an invalid length for a figure string "
            return request.param

        @pytest.fixture
        def invalid_length_figure_string(self, invalid_figure_string_length):
            " return a figure string of invalid length "
            return fit_string_to_length(random.choice(settings.figures.keys()),
                                        invalid_figure_string_length)

        def test_with_invalid_length_string(self, invalid_length_figure_string):
            " confirm Figure detects an invalid length string "
            e = pytest.raises(InputLengthError,
                              Figure, invalid_length_figure_string)
            assert e.value.message == "Figure string of unexpected length. " +\
                "expected:%d. " % settings.figure_length +\
                "found:%d." % len(invalid_length_figure_string)

    class TestUnknown:
        " confirm Figure identifies unknown strings "

        def test_with_unknown_string(self):
            " confirm Figure identifies unknown strings "
            assert Figure(get_unknown_figure_string()).account_character == \
                settings.illegible_account_character

    class TestAdulterated:
        " confirm Figure identifies adulterated strings "

        some_non_figure_characters = ('\t', '-', 'I', 'l', '/', '\\', '\r')
        char_valid = lambda char: char in settings.valid_figure_characters
        assert not any(map(char_valid, some_non_figure_characters))
        @pytest.fixture(params=some_non_figure_characters)
        def non_figure_character(self, request):
            " return arbitrary character not in settings.valid_figure_charcters "
            return request.param

        @pytest.fixture
        def adulterated_figure_string(self, non_figure_character):
            " return figure string containing an invalid character "
            figure_string = random.choice(settings.figures.keys())
            return adulterate_string(figure_string, non_figure_character)

        def test_with_adulterated_string(self, adulterated_figure_string):
            " confirm Figure checks input string for inappropriate characters "
            valid_chars = set(settings.valid_figure_characters)
            invalid_chars = set(adulterated_figure_string) - valid_chars
            invalid_chars = sorted(list(invalid_chars))
            e = pytest.raises(InputError, Figure, adulterated_figure_string)
            assert e.value.message == \
                'Figure string "%s" ' % adulterated_figure_string +\
                "contains non-figure character(s): %s" % ''.join(invalid_chars)

    class TestFunctionality:
        " confirm Figure resolves a known figure_string to its account character "

        def test_with_known_string(self):
            " confirm Figure correctly identifies known strings "
            figure_string = random.choice(settings.figures.keys())
            account_character = Figure(figure_string).account_character
            assert account_character == settings.figures[figure_string]
