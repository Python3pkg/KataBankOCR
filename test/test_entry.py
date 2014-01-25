#!/usr/bin/env python

""" Test the entry module"""

import pytest
import random

import settings

from tools.decorators import repeats
from tools.makers.entry_lines import MakeEntryLines
from tools.makers.account_string import MakeAccountString
from tools.translators import account_string_to_lines
from parser.errors import InputError, InputTypeError, InputLengthError
from parser.entry import Entry

def test_instantiation_with_no_argument():
    " confirm Entry requires more than zero arguments "
    pytest.raises(TypeError, Entry, *())

@pytest.mark.parametrize('arg_count', range(2, 20))
def test_instantiation_with_multiple_arguments(arg_count):
    " confirm Entry requires fewer than 2 arguments "
    pytest.raises(TypeError, Entry, *range(arg_count))
    
@pytest.mark.parametrize('non_list', 
                         (0, 1, -10, False, True, '', (), {}, set(), 3.14159))
def test_instantiation_with_non_list(non_list):
    " confirm Entry requires a list as its argument "
    e = pytest.raises(InputError, Entry, non_list)
    assert e.value.message == "Entry input of unexpected type. " +\
        "expected:<type 'list'>. found:%s." % type(non_list)

def invalid_lengths(valid_length, multiplier=5):
    " the list of ints 0 to (valid_length * multiplier) excluding valid_length "
    maximum_length_to_test = valid_length * multiplier
    lengths = range(maximum_length_to_test + 1)
    return [L for L in lengths if L != valid_length]

@pytest.mark.parametrize('invalid_length', 
                         invalid_lengths(settings.lines_per_entry))
def test_instantiation_with_list_of_invalid_length(invalid_length):
    " confirm Entry detects an invalid length list "
    lines = [MakeEntryLines.random()[0] for i in range(invalid_length)]
    e = pytest.raises(InputError,Entry, lines)
    assert e.value.message == "Entry list of lines of unexpected length. " +\
        "expected:%d. found:%d." % (settings.lines_per_entry, invalid_length)

def params_to_test_entry_lists_containing_a_non_string():
    """ generate list of tuples to use as parameters 

    tuple format: (bad_list, index_of_modified_element, new_bad_value)
    """
    arbitrary_non_string_values = ((0, 1, -10, False, True, 
                                    [], (), {}, set(), 3.14159))
    parameters = []
    for value in arbitrary_non_string_values:
        victim_list = MakeEntryLines.random()
        victim_line_index = random.choice(range(len(victim_list)))
        victim_list[victim_line_index] = value
        parameters.append((victim_list, victim_line_index, value))
    return parameters

@pytest.mark.parametrize('bad_list, index, value', 
                         params_to_test_entry_lists_containing_a_non_string())
def test_instantiation_with_list_containing_a_non_string(bad_list, index, value):
    " confirm Entry detects non-string in list "
    e = pytest.raises(InputError, Entry, bad_list)
    assert e.value.message == "Entry list element %d " % index +\
        "of unexpected type. expected:<type 'str'>. found:%s." % type(value)

def fit_string_to_length(string, length):
    " abbreviate or duplicate string as necessary so that len(string) == length "
    if len(string) == length:
        return string
    elif len(string) > length:
        return string[:length]
    # Still too short. Double it and try again.
    return fit_string_to_length(string+string, length)

def params_to_test_entry_lists_containing_an_invalid_length_line():
    parameters = []
    for target_length in invalid_lengths(settings.line_length):
        victim_list = MakeEntryLines.random()
        victim_index = random.choice(range(len(victim_list)))
        victim_line = victim_list[victim_index]
        invalid_length_line = fit_string_to_length(victim_line, target_length)
        victim_list[victim_index] = invalid_length_line
        parameters.append((victim_list, victim_index, invalid_length_line))
    return parameters

@pytest.mark.parametrize('bad_list, index, line', 
    params_to_test_entry_lists_containing_an_invalid_length_line())
def test_entry_list_containing_invalid_length_line(bad_list, index, line):
    " confirm Entry checks length of each line in list  "
    e = pytest.raises(InputError, Entry, bad_list)
    assert e.value.message == "Entry line %d of unexpected length. " % index +\
        "expected:%d. found:%d." % (settings.line_length, 
                                            len(line))

@repeats(100)
def test_instantiation_with_a_list_containing_a_non_empty_last_line():
    " confirm Entry verifies last line in list as empty "
    if settings.last_line_empty:
        lines = MakeEntryLines.non_empty_last_line()
        e = pytest.raises(InputError, Entry, lines)
        assert e.value.message == 'last line in list not empty'

@repeats(1000)
def test_correctly_parses_lines():
    " confirm Entry parses random entry lines into correct account strings "
    account_string = MakeAccountString.random()
    entry_lines = account_string_to_lines(account_string)
    e = Entry(list(entry_lines))
    assert e.account_string == account_string

future = """
@repeats(1000)
def test_recognition_of_non_figure_containing_lines():
    " confirm Entry rejects lines not containing only known figures "
    entry_lines = account_string_to_lines(account_string)
    adulterate lines
    e = Entry(adulterated_entry_lines)
    assert '?' in e.account_string
"""
