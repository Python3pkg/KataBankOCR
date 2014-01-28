import pytest
import random

import settings
from parser.errors import InputError, InputTypeError, InputLengthError
from parser.entry import Entry

from common_tools import entry_list_from_account_string
from common_tools import invalid_lengths, fit_string_to_length, adulterate_string

def altered_list_altered_index_its_value(target_list, alteration_function):
    """ alter a list element and return tuple of
    (altered list, altered index,  new value) """
    target_index = random.choice(range(len(target_list)))
    new_value = alteration_function(target_list[target_index])
    target_list[target_index] = new_value
    return (target_list, target_index, new_value)

class TestEntry:
    " test the Entry class "

    @pytest.fixture
    def entry_list(self, get_account_string):
        " return a list of strings that represents a random account string "
        return entry_list_from_account_string(get_account_string())

    class TestInit:
        " test Entry initialization "

        def test_instantiation_with_no_argument(self):
            " confirm Entry requires more than zero arguments "
            pytest.raises(TypeError, Entry, *())

        @pytest.mark.parametrize('arg_count', range(2, 20))
        def test_instantiation_with_multiple_arguments(self, arg_count):
            " confirm Entry requires fewer than 2 arguments "
            pytest.raises(TypeError, Entry, *range(arg_count))

    class TestInputType:
        " confirm Entry validates the type of its input "

        @pytest.fixture(params=(0, 1, -10, False, True,
                                'foo', '', (), {}, set(), 3.14159))
        def non_list(self, request):
            " return an arbitrary non-list value "
            return request.param

        def test_instantiation_with_non_list(self, non_list):
            " confirm Entry requires a list as its argument "
            e = pytest.raises(InputError, Entry, non_list)
            assert e.value.message == "Entry input of unexpected type. " +\
                "expected:<type 'list'>. found:%s." % type(non_list)

    class TestInputLength:
        " confirm Entry validates the length of its input "

        @pytest.fixture(params=invalid_lengths(settings.lines_per_entry))
        def invalid_length_entry_list(self, request, entry_list):
            " return an entry list of invalid length "
            return [entry_list[0] for i in range(request.param)]

        def test_with_list_of_invalid_length(self, invalid_length_entry_list):
            " confirm Entry detects an invalid length list "
            e = pytest.raises(InputError,Entry, invalid_length_entry_list)
            assert e.value.message == \
                "Entry list of lines of unexpected length. " +\
                "expected:%d. " % settings.lines_per_entry +\
                "found:%d." % len(invalid_length_entry_list)

    class TestElementType:
        " confirm Entry validates the type of each element in its input list "

        @pytest.fixture(params=(0, 1, -10, False, True, 
                                [], (), {}, set(), 3.14159))
        def non_string_value(self, request):
            " return an arbitrary non-string value "
            return request.param

        @pytest.fixture
        def entry_list_with_non_string_its_index_and_value(
            self, non_string_value, entry_list):
            """ return a tuple used to test an entry list containing a non-string.
            Create valid entry list, replace a random line with a non-string, &
            return a tuple of (adulterated list, altered index, non-string value).
            """
            alteration_function = lambda x: non_string_value 
            return altered_list_altered_index_its_value(entry_list, 
                                                        alteration_function)

        def test_with_list_containing_a_non_string(
            self, entry_list_with_non_string_its_index_and_value):
            " confirm Entry detects non-string in list "
            bad_list, index, value = \
                entry_list_with_non_string_its_index_and_value
            e = pytest.raises(InputError, Entry, bad_list)
            assert e.value.message == "Entry list element %d " % index +\
                "of unexpected type. expected:<type 'str'>. " +\
                "found:%s." % type(value)

    class TestLineLength:
        " confirm Entry validates the length of each line in its entry list "

        @pytest.fixture(params=invalid_lengths(settings.line_length))
        def invalid_line_length(self, request):
            " return an invalid length for a line (in an entry list) "
            return request.param

        @pytest.fixture
        def invalid_length_line(self, entry_list, invalid_line_length):
            " return a line (an entry list element) of invalid length "
            return fit_string_to_length(entry_list[0], invalid_line_length)

        @pytest.fixture
        def entry_list_with_wrong_length_line_its_index_and_value(
            self, invalid_length_line, entry_list):
            " return a tuple of (adulterated_list, altered index, bad_line) "
            alteration_function = lambda s: invalid_length_line
            return altered_list_altered_index_its_value(entry_list,
                                                        alteration_function)

        def test_with_entry_list_containing_line_of_invalid_length(
            self, entry_list_with_wrong_length_line_its_index_and_value):
            " confirm Entry checks length of each line in list  "
            bad_list, index, bad_line =\
                entry_list_with_wrong_length_line_its_index_and_value
            e = pytest.raises(InputError, Entry, bad_list)
            assert e.value.message == \
                "Entry line %d of unexpected length. " % index +\
                "expected:%d. " % settings.line_length +\
                "found:%d." % len(bad_line)

    class TestLastLineEmpty:
        " confirm Entry ensures last line contains only whitespace "

        @pytest.fixture
        def non_whitespace_line(self,):
            " return a line containing at least one non-whitespace character "
            assert not ''.join(settings.valid_figure_characters).isspace()
            get_char = lambda x: random.choice(settings.valid_figure_characters)
            for i in range(10):
                line = ''.join(map(get_char, range(settings.line_length)))
                if not line.isspace():
                    return line
            raise ValueError('Failed to generate a non-whitespace line')

        @pytest.fixture
        def entry_list_with_non_whitespace_last_line(
            self, entry_list, non_whitespace_line):
            " return entry list with a non whitespace character in the last line "
            entry_list[settings.lines_per_entry - 1] = non_whitespace_line
            return entry_list

        def test_with_entry_list_containing_a_non_empty_last_line(
            self, entry_list_with_non_whitespace_last_line):
            " confirm Entry verifies last line in list as empty "
            if settings.last_line_empty:
                bad_list = entry_list_with_non_whitespace_last_line
                e = pytest.raises(InputError, Entry, bad_list)
                assert e.value.message == 'Last line in list not empty'

    class TestFunctionality:
        " confirm Entry parses entry_list to figures to correct account string "

        def test_correctly_parses_entry_list(self, get_account_string):
            " confirm Entry parses valid entry lines into correct account string "
            account_string = get_account_string()
            entry_list = entry_list_from_account_string(account_string)
            assert Entry(entry_list).account_string == account_string

    class TestProblem:
        " confirm Entry marks each account string as valid/invalid/illegible "

        @pytest.fixture
        def valid_account_string(self, get_account_string):
            " return a valid account string "
            # brutish
            while True:
                account_string = get_account_string()
                if settings.checksum(account_string):
                    return account_string

        def test_with_valid_account_string(self, valid_account_string):
            " confirm Entry has no problem with a valid account string "
            entry_list = entry_list_from_account_string(valid_account_string)
            assert Entry(entry_list).problem == None

        @pytest.fixture
        def invalid_account_string(self, get_account_string):
            " return a invalid account string "
            # brutish
            while True:
                account_string = get_account_string()
                if not settings.checksum(account_string):
                    return account_string

        def test_with_invalid_account_string(self, invalid_account_string):
            " confirm Entry marks an invalid account string as such"
            entry_list = entry_list_from_account_string(invalid_account_string)
            assert Entry(entry_list).problem == settings.invalid_account_marker

        @pytest.fixture
        def illegible_account_string(self, get_account_string):
            " return account string containing the illegible account character "
            return adulterate_string(get_account_string(),
                                     settings.illegible_account_character)

        def test_with_illegible_account_string(self, illegible_account_string):
            " confirm Entry marks an illegible account string as such"
            entry_list = entry_list_from_account_string(illegible_account_string)
            assert Entry(entry_list).problem == settings.illegible_account_marker
