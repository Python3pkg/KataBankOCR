" Test the Entry module "

import pytest

import settings
from parser.errors import InputError, InputTypeError, InputLengthError
from parser.entry import Entry

from common_tools import figure_from_numeral, entry_from_account
from common_tools import invalid_lengths, fit_to_length, replace_element

@pytest.fixture
def entry(get_account):
    " Return an Entry that represents a random Account "
    return entry_from_account(get_account())

class TestCheck:
    " test the Entry.check method "

    class TestType:
        " confirm Entry.check validates type "

        @pytest.fixture(params=(0, 1, -10, False, True, 'foo', '', (1,2,), {'a',}, set(), 3.14159))
        def non_list(self, request):
            " return an arbitrary non-list value "
            return request.param

        def test_with_non_list(self, non_list):
            " confirm Entry.check detects a non_list "
            pytest.raises(InputTypeError, Entry.check, non_list)

    class TestLength:
        " confirm Entry.check validates length "

        @pytest.fixture(params=invalid_lengths(settings.lines_per_entry))
        def invalid_length_entry(self, request, entry):
            " return an entry of invalid length "
            return fit_to_length(entry, request.param)

        def test_with_input_of_invalid_length(self, invalid_length_entry):
            " confirm Entry.check detects an invalid length "
            pytest.raises(InputError, Entry.check, invalid_length_entry)

    class TestElementTypes:
        " confirm Entry.check validates the type of each element "

        def test_with_list_containing_a_non_string(self, entry, non_string):
            " confirm Entry.check detects a non-string in its input "
            entry = replace_element(entry, non_string)
            pytest.raises(InputError, Entry.check, entry)

    class TestLineLengths:
        " confirm Entry.check validates the length of each line "

        @pytest.fixture(params=invalid_lengths(settings.strokes_per_line))
        def invalid_stroke_count(self, request):
            " return an invalid length for a line "
            return request.param

        def test_with_entry_containing_line_of_invalid_length(self, entry, invalid_stroke_count):
            " confirm Entry.check detects an invalid length line "
            first_line = entry[0]
            line_of_invalid_length = fit_to_length(first_line, invalid_stroke_count)
            entry = replace_element(entry, line_of_invalid_length)
            pytest.raises(InputLengthError, Entry.check, entry)

class TestFiguresFromEntry:
    " test the Entry.figures_from_entry method "

    def test_correctly_parses_figures_from_entry(self, get_account):
        " confirm Entry.figures_from_entry splits an Entry into its Figures "
        account = get_account()
        numerals = list(account)
        figures = map(figure_from_numeral, numerals)
        expected = figures
        entry = entry_from_account(account)
        found = Entry.figures_from_entry(entry)
        assert expected == found

class TestAccountFromNumerals:
    " test the Entry.account_from_numerals method "

    def test_correctly_joins_numerals(self, get_account):
        " confirm Entry.account_from_numerals correctly joins numerals "
        account = get_account()
        expected = account
        numerals = list(account)
        found = Entry.account_from_numerals(numerals)
        assert expected == found

class TestResultFromNumerals:
    " test the Entry.result_from_numerals "

    class TestInvalid:
        " test Entry.result_from_numerals with an invalid account "

        @pytest.fixture
        def invalid_account(self, get_account):
            " Return a bad Account by [in|dec]rementing until invalid "
            account = get_account()
            delta = self._get_delta(account)
            while settings.checksum(account):
                account = self._modify_account(account, delta)
            return account

        def _get_delta(self, account):
            " return whether we raise or lower account "
            if int(account) > settings.checksum_divisor:
                return -1
            return 1

        def test_with_invalid_account(self, invalid_account):
            " confirm Entry.result_from_numerals marks an invalid Account as such"
            entry = entry_from_account(invalid_account)
            expected = account + settings.invalid_status
            found = Entry.result_from_numerals(invalid_account)
            assert expected == found

    class TestInvalid:
        " test Entry.result_from_numerals with an valid account "

        @pytest.fixture
        def valid_account(self, get_account):
            " Return a good Account by [in|dec]rementing until valid "
            account = get_account()
            delta = self._get_delta(account)
            while not settings.checksum(account):
                account = self._modify_account(account, delta)
            return account

        def _modify_account(self, account, delta):
            " Return Account after having added or subtracted 1 "
            account = str(int(account) + delta)
            return account.zfill(settings.figures_per_entry)

        def test_with_valid_account(self, valid_account):
            " confirm Entry.result_from_numerals leaves a valid account unmarked "
            expected = valid_account
            found = Entry.result_from_numerals(valid_account)
            assert expected == found

    class TestInvalid:
        " test Entry.result_from_numerals with an illegible account "

        @pytest.fixture
        def illegible_account(self, get_account):
            " return Account containing the illegible Numeral "
            return replace_element(get_account(), settings.illegible_numeral)

        def test_with_illegible_account(self, illegible_account):
            " confirm Entry.result_from_numerals marks an illegible Account as such"
            entry = entry_from_account(illegible_account)
            expected = illegible_account + settings.illegible_status
            found = Entry.result_from_numerals(illegible_account)
            assert expected == found
