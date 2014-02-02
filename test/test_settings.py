import pytest

import settings

from common_tools import invalid_lengths
from types import FunctionType

class TestSettings:
    " Test the settings module "

    class TestDefinition:
        """ confirm settings file defined exactly the expected setting
        names with their expected types """

        expected_setting_types = (('lines_per_entry',int),
                                  ('figures_per_entry',int),
                                  ('strokes_per_substring',int),
                                  ('strokes_per_figure',int),
                                  ('strokes_per_line',int),
                                  ('approximate_entries_per_file',int),
                                  ('checksum_divisor',int),
                                  ('some_known_valid_accounts',tuple),
                                  ('some_known_invalid_accounts',tuple),
                                  ('valid_strokes',tuple),
                                  ('valid_numerals',tuple),
                                  ('figures',dict),
                                  ('illegible_numeral',str),
                                  ('illegible_flag',str),
                                  ('invalid_flag',str),
                                  ('checksum',FunctionType),
                                  )

        @pytest.fixture(params=expected_setting_types)
        def setting_name_and_type(self, request):
            " return (setting_name, setting_type) "
            return request.param

        def test_setting_defined(self, setting_name_and_type):
            """ confirm setting got defined """
            assert settings.__dict__.has_key(setting_name_and_type[0])

        def test_setting_of_correct_type(self, setting_name_and_type):
            """ confirm setting has expected type """
            setting_name, setting_type = setting_name_and_type
            setting_value = settings.__dict__[setting_name]
            assert isinstance(setting_value, setting_type)

        def test_setting_count_matches_expectations(self):
            " confirm settings contains exactly as many entries as expected "
            attributes_of_settings = settings.__dict__.keys()
            builtins_of_settings = filter(lambda k: '__' in k, attributes_of_settings)
            defined_settings = set(attributes_of_settings) - set(builtins_of_settings)
            found = len(defined_settings)
            expected = len(self.expected_setting_types)
            assert expected == found

    class TestUniqueness:
        " confirm no duplicate Figures, Numerals, or Strokes "

        def test_uniqueness_of_figures(self):
            all_valid_figures = settings.figures.keys()
            assert len(set(all_valid_figures)) == len(all_valid_figures)

        def test_uniqueness_of_valid_numerals(self):
            numerals = settings.valid_numerals
            assert len(set(numerals)) == len(numerals)

        def test_uniqueness_of_represented_numerals(self):
            numerals = settings.figures.values()
            assert len(set(numerals)) == len(numerals)

        def test_uniqueness_of_valid_strokes(self):
            strokes = settings.valid_strokes
            assert len(set(strokes)) == len(strokes)

    class TestRepresentation:
        " confirm a Figure exists that represents each Numeral "

        def test_numeral_representation(self):
            assert set(settings.figures.values()) == set(settings.valid_numerals)

    class TestStringConstruction:
        " confirm length and composition strings "

        class TestFigureConstruction:
            " confirm length and composition of all figures "

            @pytest.fixture(params=settings.figures.keys())
            def figure(self, request):
                " return a figure that represents a numeral "
                return request.param

            def test_length_of_figure(self, figure):
                " confirm figure contains the correct stroke count "
                assert len(figure) == settings.strokes_per_figure

            def test_figure_composed_only_of_valid_strokes(self, figure):
                " confirm figure composed only of valid Strokes "
                assert set(figure).issubset(settings.valid_strokes)

        class TestAccountConstruction:
            " confirm length and composition of all Accounts "

            @pytest.fixture(params=list(settings.some_known_valid_accounts) +\
                                list(settings.some_known_invalid_accounts))
            def account(self, request):
                " return an Account "
                return request.param

            def test_length_of_account(self, account):
                assert len(account) == settings.figures_per_entry

            def test_account_of_valid_numerals(self, account):
                assert set(account).issubset(set(settings.valid_numerals))


        class TestNumeralConstruction:
            " confirm length and composition of all Numerals "

            @pytest.fixture(params=settings.figures.values())
            def numeral(self, request):
                " return a Numeral "
                return request.param

            def test_length_of_numeral(self, numeral):
                " confirm numeral exactly one character long "
                assert len(numeral) == 1

            def test_numeral_validity(self, numeral):
                assert numeral in settings.valid_numerals

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
        " confirm checksum correct categorizes known Accounts "
        
        @pytest.mark.parametrize('account', settings.some_known_valid_accounts)
        def test_with_known_good_account(self, account):
            " confirm checksum reports a known good Account as valid "
            assert settings.checksum(account) == True

        @pytest.mark.parametrize('account', settings.some_known_invalid_accounts)
        def test_with_known_bad_account(self, account):
            " confirm checksum reports a known bad Account as invalid "
            assert settings.checksum(account) ==  False

    class TestIllegibleNumeral:
        " confirm illegible_numeral's characteristics "
        
        def test_length_of_illegible_numeral(self):
            " confirm llegible_numeral exactly one character long "
            assert len(settings.illegible_numeral) == 1

        def test_illegible_numeral_distinct_from_valid_numerals(self):
            " confirm llegible_numeral not in valid_numerals "
            assert settings.illegible_numeral \
                not in settings.valid_numerals

    class TestIntegerValues:
        " confirm integer settings have reasonable values "

        @pytest.mark.parametrize('setting_name', (
                'strokes_per_line', 'figures_per_entry', 'approximate_entries_per_file', 
                'lines_per_entry', 'approximate_entries_per_file', 
                'checksum_divisor', 'strokes_per_substring'))
        def test_integer_not_negative(self, setting_name):
            " confirm each integer setting has value of at least zero "
            assert settings.__dict__[setting_name] >= 0

        @pytest.mark.parametrize('setting_name, arbitrary_maximum',(
                ('approximate_entries_per_file', 100000),
                ('lines_per_entry', 50),
                ('figures_per_entry', 50),
                ('strokes_per_substring', 50),
                ('strokes_per_figure', 250),
                ('strokes_per_line', 1000),
                ))
        def test_integer_value_below_arbitrary_maximum(self, setting_name, arbitrary_maximum):
            " confirm value does not exceed an arbitrary maximum "
            assert settings.__dict__[setting_name] <= arbitrary_maximum

        
