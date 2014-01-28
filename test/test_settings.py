import pytest

import settings

from common_tools import invalid_lengths
from types import FunctionType

class TestSettings:
    " Test the settings file "

    class TestDefinedType:
        " confirm all settings defined and of correct type "
    
        @pytest.fixture(params=(('lines_per_entry',int),
                                ('figures_per_entry',int),
                                ('figure_width',int),
                                ('figure_length',int),
                                ('valid_figure_characters',tuple),
                                ('some_known_valid_account_strings',tuple),
                                ('some_known_invalid_account_strings',tuple),
                                ('valid_figure_characters',tuple),
                                ('figures',dict),
                                ('checksum',FunctionType),
                                ('last_line_empty',bool),))
        def setting_name_and_type(self, request):
            " return (setting_name, setting_type) "
            return request.param

        def test_setting_defined(self, setting_name_and_type):
            """ confirm setting defined """
            assert settings.__dict__.has_key(setting_name_and_type[0])

        def test_setting_of_correct_type(self, setting_name_and_type):
            """ confirm setting has expected type """
            setting_name, setting_type = setting_name_and_type
            setting_value = settings.__dict__[setting_name]
            assert isinstance(setting_value, setting_type)

    class TestSingularity:
        " confirm uniqueness of all figures and account characters "

        def test_figure_string_singularity(self):
            " confirm no duplicate figures exist "
            figure_characters = settings.figures.keys()
            assert len(set(figure_characters)) == len(figure_characters)

        def test_account_character_singularity(self):
            " confirm no duplicate account_characters exist "
            account_characters = settings.figures.keys()
            assert len(set(account_characters)) == len(account_characters)

    class TestConstruction:
        " confirm length and composition of all figures and account characters "

        @pytest.fixture(params=settings.figures.keys())
        def figure_string(self, request):
            " return a figure string that represents an account character "
            return request.param

        def test_figure_string_has_correct_length(self, figure_string):
            " confirm figure string contains the correct number of characters "
            assert len(figure_string) == settings.figure_length

        def test_figure_composed_of_valid_components(self, figure_string):
            " confirm figure composed only of valid figure characters "
            assert set(figure_string).issubset(settings.valid_figure_characters)

        @pytest.fixture(params=settings.figures.values())
        def account_character(self, request):
            " return an account character represented by a figure string "
            return request.param

        def test_account_character_validitity(self, account_character):
            " confirm account character validitiy "
            assert account_character in settings.valid_account_characters

    class TestChecksumArgumentCount:
        " confirm checksum accepts exactly one argument "
        
        def test_with_no_argument(self):
            " confirm checksum requires more than zero arguments "
            pytest.raises(TypeError, settings.checksum)

        @pytest.mark.parametrize('arg_count', range(2, 20))
        def test_with_multiple_arguments(self, arg_count):
            " confirm checksum requires fewer than 2 arguments "
            pytest.raises(TypeError, settings.checksum, *range(arg_count))

    class TestChecksumFunctionality:
        " confirm checksum correct categorizes known account strings "
        
        @pytest.mark.parametrize('account_string',
                                 settings.some_known_valid_account_strings)
        def test_with_known_good_string(self, account_string):
            " confirm checksum reports a known good account string as valid "
            assert settings.checksum(account_string) == True

        @pytest.mark.parametrize('account_string',
                                 settings.some_known_invalid_account_strings)
        def test_with_known_bad_string(self, account_string):
            " confirm checksum reports a known bad account string as invalid "
            assert settings.checksum(account_string) ==  False
