#!/usr/bin/env python

""" Test the entry module"""

import pytest
import random

import settings
from scanner_parser import entry

from testing_tools import repeats, random_account_number
from testing_tools import random_non_blank_valid_character
from entry_testing_tools import entries, arbitrary_non_string_values
from entry_testing_tools import account_number_to_lines
from entry_testing_tools import numeral_to_figure_string
from scanner_parser.entry import Entry, InputError, lines_to_figure_strings

def test_instantiation_with_no_argument():
    " confirm Entry requires more than zero arguments "
    with pytest.raises(TypeError):
        e = Entry()

def test_instantiation_with_multiple_arguments(min=2,max=10):
    " confirm Entry requires fewer than 2 arguments "
    args = min
    while args <= max:
        with pytest.raises(TypeError):
            e = Entry(*range(args))
        args += 1
    
def test_instantiation_with_valid_lines():
    " confirm Entry instantiates with a valid string argument "
    for valid_string in entries.keys():
        e = Entry(valid_string)
        assert isinstance(e,Entry)

def test_instantiation_with_non_tuple():
    " confirm Entry requires a tuple as its argument "
    for non_string in arbitrary_non_string_values:
        with pytest.raises(InputError): # 'not a tuple'
            e = Entry(non_string)

def test_instantiation_with_tuple_of_insufficient_length():
    " confirm Entry checks for minimum tuple length "
    appropriate_length = settings.lines_per_entry
    lines = 1
    while lines < appropriate_length:
        with pytest.raises(InputError): # 'tuple too short'
            e = Entry(range(lines))
        lines += 1

def test_instantiation_with_tuple_of_excessive_length():
    " confirm Entry checks maximum tuple length "
    appropriate_length = settings.lines_per_entry
    lines = appropriate_length + 1
    while lines < appropriate_length * 5:
        with pytest.raises(InputError): # 'tuple too long'
            e = Entry(range(lines))
        lines += 1

@repeats(1000)
def test_instantiation_with_tuple_containing_a_non_string():
    " confirm Entry checks type of all tuple values "
    victim_list = list(random.choice(entries.keys()))
    victim_line_index = random.choice(range(len(victim_list)))
    victim_line = victim_list[victim_line_index]
    non_string_value = random.choice(arbitrary_non_string_values)
    victim_list[victim_line_index] = non_string_value
    adulterated_tuple = tuple(victim_list)
    with pytest.raises(InputError): # 'non-string in tuple'
        e = Entry(adulterated_tuple)

@repeats(1000)
def test_instantiation_with_a_tuple_containing_too_short_a_string():
    " confirm Entry checks minimum string length "
    victim_list = list(random.choice(entries.keys()))
    victim_line_index = random.choice(range(len(victim_list)))
    victim_line = victim_list[victim_line_index]
    new_line_length = random.choice(range(len(victim_line)))
    abbreviated_line = victim_line[:new_line_length]
    victim_list[victim_line_index] = abbreviated_line
    altered_tuple = tuple(victim_list)
    with pytest.raises(InputError): # 'string in tuple too short'
        e = Entry(altered_tuple)

@repeats(1000)
def test_instantiation_with_a_tuple_containing_too_long_a_string():
    " confirm Entry checks maximum string length "
    victim_list = list(random.choice(entries.keys()))
    victim_line_index = random.choice(range(len(victim_list)))
    victim_line = victim_list[victim_line_index]
    additional_length = random.choice(range(len(victim_line))) + 1
    additional_text = victim_line[:additional_length]
    excessively_long_line = victim_line + additional_text
    victim_list[victim_line_index] = excessively_long_line
    altered_tuple = tuple(victim_list)
    with pytest.raises(InputError): # 'string in tuple too long'
        e = Entry(altered_tuple)


@repeats(1000)
def test_instantiation_with_a_tuple_containing_a_non_empty_last_line():
    " confirm Entry veryify last line in tuple as empty "
    if settings.last_line_empty:
        victim_list = list(random.choice(entries.keys()))
        victim_line_index = settings.lines_per_entry-1
        victim_line = victim_list[victim_line_index]
        additional_character = random_non_blank_valid_character()
        replaced_character_position = random.choice(range(len(victim_line)))
        char,pos = additional_character, replaced_character_position
        altered_line = victim_line[:pos] + char + victim_line[pos+1:]
        victim_list[victim_line_index] = altered_line
        altered_tuple = tuple(victim_list)
        with pytest.raises(InputError): # 'last line in tuple not empty'
            e = Entry(altered_tuple)

@repeats(1000)
def test_lines_to_figure_strings():
    " confirm lines_to_figure_strings properly parses some known values "
    account_number = random_account_number()
    entry_lines = account_number_to_lines(account_number)
    figure_strings = [numeral_to_figure_string(n) for n in account_number]
    assert lines_to_figure_strings(entry_lines) == figure_strings

ideas="""

concat figure values into account number

"""


#lines_per_entry
#figures_per_entry
#figure_width
#characters_per_figure
#valid_figure_characters
#figures
#last_line_empty

