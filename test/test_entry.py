import pytest
import random

import settings
from parser.errors import InputError, InputTypeError, InputLengthError
from parser.entry import Entry

from tools.builders import entry_list_from_account_string
from tools.helpers import invalid_lengths, fit_string_to_length

class TestEntry:
    " test the Entry class "

    class TestInit:
        " test Entry initialization "

        def test_instantiation_with_no_argument(self):
            " confirm Entry requires more than zero arguments "
            pytest.raises(TypeError, Entry, *())

        @pytest.mark.parametrize('arg_count', range(2, 20))
        def test_instantiation_with_multiple_arguments(self, arg_count):
            " confirm Entry requires fewer than 2 arguments "
            pytest.raises(TypeError, Entry, *range(arg_count))

    class TestInputValidation:
        " confirm Entry validates its input "

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

        @pytest.fixture(params=invalid_lengths(settings.lines_per_entry))
        def invalid_entry_list_length(self, request):
            " return an in invalid length for an entry list "
            return request.param

        @pytest.fixture
        def entry_list(self):
            " return a list of strings that represents a random account string "
            figure_indexes = range(settings.figures_per_entry)
            get_figure_string = lambda: random.choice(settings.figures.keys())
            figure_strings = [get_figure_string() for i in figure_indexes]
            lines = []
            for line_index in range(settings.lines_per_entry):
                line = ''
                for figure_index in figure_indexes:
                    figure_string = figure_strings[figure_index]
                    first_char_index = line_index * settings.figure_width
                    last_char_index = first_char_index + settings.figure_width
                    substring = figure_string[first_char_index:last_char_index]
                    line += substring
                lines.append(line)
            return lines


        @pytest.fixture
        def entry_list(self, get_account_string):
            " return a list of strings that represents a random account string "
            return entry_list_from_account_string(get_account_string())

        @pytest.fixture
        def invalid_length_entry_list(self, entry_list, 
                                      invalid_entry_list_length):
            " return an entry list of invalid length "
            return [entry_list[0] for i in range(invalid_entry_list_length)]

        def test_with_list_of_invalid_length(self, invalid_length_entry_list):
            " confirm Entry detects an invalid length list "
            e = pytest.raises(InputError,Entry, invalid_length_entry_list)
            assert e.value.message == \
                "Entry list of lines of unexpected length. " +\
                "expected:%d. " % settings.lines_per_entry +\
                "found:%d." % len(invalid_length_entry_list)

        @pytest.fixture(params=(0, 1, -10, False, True, 
                                [], (), {}, set(), 3.14159))
        def arbitrary_non_string_value(self, request):
            " return a non-string value "
            return request.param

        def altered_list_altered_index_its_value(self, target_list,
                                                 alteration_function):
            """ alter a list element and return tuple of
            (altered list, altered index,  new value) """
            target_index = random.choice(range(len(target_list)))
            new_value = alteration_function(target_list[target_index])
            target_list[target_index] = new_value
            return (target_list, target_index, new_value)

        @pytest.fixture
        def entry_list_with_non_string_its_index_and_value(
            self, arbitrary_non_string_value, entry_list):
            """ return a tuple used to test an entry list containing a non-string
            create valid entry list, replace a random line with a non-string,
            return tuple of (adulterated list, altered index, non-string value)
            """
            alteration_function = lambda s: arbitrary_non_string_value 
            return self.altered_list_altered_index_its_value(entry_list, 
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
            return self.altered_list_altered_index_its_value(entry_list,
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

        @pytest.fixture
        def non_whitespace_line(self,):
            " return a line containing at least one non-whitespace character "
            assert not ''.join(settings.valid_figure_characters).isspace()
            get_char = lambda x: random.choice(settings.valid_figure_characters)
            while True:
                line = ''.join(map(get_char, range(settings.line_length)))
                if not line.isspace():
                    return line

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
                assert e.value.message == 'last line in list not empty'

    class TestFunctionality:
        " confirm Entry resolves list of known figgure strings to an acc. string "

        def test_correctly_parses_entry_list(self, get_account_string):
            " confirm Entry parses valid entry lines into correct account string "
            account_string = get_account_string()
            entry_list = entry_list_from_account_string(account_string)
            assert Entry(entry_list).account_string == account_string


