" Test the Entry module "

import pytest
import mock
import random

import settings
from parser.errors import InputError, InputTypeError, InputLengthError
from parser.entry import Entry

from common_tools import entry_from_account
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

        def test_instantiation_with_non_list(self, non_list):
            " confirm Entry requires a list as its argument "
            pytest.raises(InputTypeError, Entry, non_list)

    class TestLength:
        " confirm Entry.check validates length "

        @pytest.fixture(params=invalid_lengths(settings.lines_per_entry))
        def invalid_length_entry(self, request, entry):
            " return an entry of invalid length "
            return fit_to_length(entry, request.param)

        def test_with_input_of_invalid_length(self, invalid_length_entry):
            " confirm Entry.check detects input of invalid length "
            pytest.raises(InputError,Entry, invalid_length_entry)

    class TestElementTypes:
        " confirm Entry.check validates the type of each element "

        def test_with_list_containing_a_non_string(self, entry, non_string):
            " confirm Entry detects a non-string in its input "
            entry = replace_element(entry, non_string)
            pytest.raises(InputError, Entry, entry)

    class TestLineLengths:
        " confirm Entry.check validates the length of each line "

        @pytest.fixture(params=invalid_lengths(settings.strokes_per_line))
        def invalid_entry_length(self, request):
            " return an invalid length for a line "
            return request.param

        def test_with_entry_containing_line_of_invalid_length(self, entry, invalid_entry_length):
            " confirm Entry checks length of each line "
            first_line = entry[0]
            line_of_invalid_length = fit_to_length(first_line, invalid_entry_length)
            entry = replace_element(entry, line_of_invalid_length)
            pytest.raises(InputLengthError, Entry, entry)

    class TestLastLineEmpty:
        " confirm Entry ensures last line contains only whitespace "

        @pytest.fixture
        def non_whitespace_line(self,):
            " return a line containing at least one non-whitespace stroke "
            assert not ''.join(settings.valid_strokes).isspace()
            get_stroke = lambda x: random.choice(settings.valid_strokes)
            stroke_indexes = range(settings.strokes_per_line)
            arbitrary_maximum_attempt_count = 5
            for i in range(arbitrary_maximum_attempt_count):
                line = ''.join(map(get_stroke, stroke_indexes))
                if not line.isspace():
                    return line
            raise ValueError('Failed to generate a non-whitespace line')

        def test_with_entry_containing_a_non_empty_last_line(self, entry, non_whitespace_line):
            " confirm Entry verifies last line as empty "
            if settings.last_line_empty:
                index_of_last_line = -1
                entry = replace_element(entry, non_whitespace_line, index_of_last_line)
                e = pytest.raises(InputError, Entry, entry)
                assert e.value.message == 'Last line not empty'

class TestGetFigures:
    " test the Entry.get_figures method "

    def test_correctly_parses_entry_to_account(self, get_account):
        " confirm Entry parses valid Entry into correct Account "
        account = get_account()
        entry = entry_from_account(account)
        assert Entry(entry).account == account

class TestJoinNumeral:
    " test the Entry.join_numerals "


    class TestProblem:
        " confirm Entry appropriately includes valid/invalid/illegible flags "

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
            " confirm Entry marks an invalid Account as such"
            entry = entry_from_account(invalid_account)
            assert Entry(entry).problem == settings.invalid_flag

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
            " confirm Entry has no problem with a valid Account "
            entry = entry_from_account(valid_account)
            assert Entry(entry).problem == None

        @pytest.fixture
        def illegible_account(self, get_account):
            " return Account containing the illegible Numeral "
            return replace_element(get_account(), settings.illegible_numeral)

        def test_with_illegible_account(self, illegible_account):
            " confirm Entry marks an illegible Account as such"
            entry = entry_from_account(illegible_account)
            assert Entry(entry).problem == settings.illegible_flag
