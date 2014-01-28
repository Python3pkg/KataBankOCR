import pytest

import settings

class TestSettings:
    " Test the settings file "

    class TestDefinedType:
        " confirm all settings defined and of correct type "
    
        @pytest.fixture(params=(('lines_per_entry',int),
                                ('figures_per_entry',int),
                                ('figure_width',int),
                                ('figure_length',int),
                                ('valid_figure_characters',tuple),
                                ('figures',dict),
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

