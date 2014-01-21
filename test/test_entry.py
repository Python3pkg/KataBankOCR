#!/usr/bin/env python

""" Test the entry module"""

import pytest
import random

import settings

from makers import MakeFigureCharacter, MakeAccountString, MakeEntryLines
from decorators import repeats
from translators import account_number_to_lines, numeral_to_figure_string
from entry_testing_tools import entries, arbitrary_non_string_values
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

@repeats(50)
def test_instantiation_with_tuple_containing_a_non_string():
    " confirm Entry checks type of all tuple values "
    with pytest.raises(InputError): # 'non-string in tuple'
        e = Entry(MakeEntryLines.containing_non_string())

@repeats(1000)
def test_instantiation_with_a_tuple_containing_too_short_a_string():
    " confirm Entry checks minimum string length "
    with pytest.raises(InputError): # 'string in tuple too short'
        e = Entry(MakeEntryLines.abbreviated_string())

@repeats(1000)
def test_instantiation_with_a_tuple_containing_too_long_a_string():
    " confirm Entry checks maximum string length "
    with pytest.raises(InputError): # 'string in tuple too long'
        e = Entry(MakeEntryLines.extended_string())

@repeats(1000)
def test_instantiation_with_a_tuple_containing_a_non_empty_last_line():
    " confirm Entry verifies last line in tuple as empty "
    if settings.last_line_empty:
        with pytest.raises(InputError): # 'last line in tuple not empty'
            e = Entry(MakeEntryLines.non_empty_last_line())

@repeats(1000)
def test_lines_to_figure_strings():
    " confirm lines_to_figure_strings properly parses some known values "
    account_number = MakeAccountString.valid()
    entry_lines = account_number_to_lines(account_number)
    figure_strings = [numeral_to_figure_string(n) for n in account_number]
    assert lines_to_figure_strings(entry_lines) == figure_strings

@repeats(1000)
def test_recognition_of_numbers_in_valid_lines():
    " confirm Entry parses valid entry lines into correct account number "
    account_number = MakeAccountString.valid()
    entry_lines = account_number_to_lines(account_number)
    e = Entry(tuple(entry_lines))
    assert e.account_number == account_number

future = """
@repeats(1000)
def test_recognition_of_non_figure_containing_lines():
    " confirm Entry rejects lines not containing only known figures "
    entry_lines = account_number_to_lines(account_number)
    adulterate lines
    e = Entry(tuple(adulterated_entry_lines))
    assert '?' in e.account_number
"""
