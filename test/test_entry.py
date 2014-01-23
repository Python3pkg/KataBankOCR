#!/usr/bin/env python

""" Test the entry module"""

import pytest
import random

import settings

from tools.decorators import repeats
from tools.makers.account_string import MakeAccountString
from tools.makers.entry_lines import MakeEntryLines
from tools.translators import account_string_to_lines, numeral_to_figure_string
from parser.entry import Entry, InputError, lines_to_figure_strings

def test_instantiation_with_no_argument():
    " confirm Entry requires more than zero arguments "
    pytest.raises(TypeError, Entry)

def test_instantiation_with_multiple_arguments(min=2,max=10):
    " confirm Entry requires fewer than 2 arguments "
    for arg_count in range(min,max+1):
        pytest.raises(TypeError, Entry, *range(arg_count))
    
@repeats(1000)
def test_instantiation_with_valid_lines():
    " confirm Entry instantiates with a valid string argument "
    e = Entry(MakeEntryLines.valid())
    assert isinstance(e,Entry)

def test_instantiation_with_non_tuple():
    " confirm Entry requires a tuple as its argument "
    arbitrary_non_string_values = (0,1,-10,False,True,3.14359,'',[],{},set())
    for non_string in arbitrary_non_string_values:
        e = pytest.raises(InputError, Entry, non_string)
        assert 'not a tuple' in e.value.message

def test_instantiation_with_tuple_of_insufficient_length():
    " confirm Entry checks for minimum tuple length "
    tuple_length = 1
    while tuple_length < settings.lines_per_entry:
        lines = MakeEntryLines.valid()[:tuple_length]
        e = pytest.raises(InputError, Entry, lines)
        assert 'tuple wrong length' in e.value.message
        tuple_length += 1

def test_instantiation_with_tuple_of_excessive_length():
    " confirm Entry checks maximum tuple length "
    tuple_length = settings.lines_per_entry + 1
    repeated_line = MakeEntryLines.valid()[0]
    lines = tuple(repeated_line for i in range(tuple_length))
    while tuple_length < settings.lines_per_entry * 5:
        e = pytest.raises(InputError,Entry, lines)
        assert 'tuple wrong length' in e.value.message
        tuple_length += 1

@repeats(50)
def test_instantiation_with_tuple_containing_a_non_string():
    " confirm Entry checks type of all tuple values "
    e = pytest.raises(InputError, Entry, MakeEntryLines.containing_non_string())
    assert e.value.message == 'non-string in tuple'

@repeats(100)
def test_instantiation_with_a_tuple_containing_too_short_a_string():
    " confirm Entry checks minimum string length "
    e = pytest.raises(InputError, Entry, MakeEntryLines.abbreviated_string())
    assert 'string too short: ' in e.value.message

@repeats(100)
def test_instantiation_with_a_tuple_containing_too_long_a_string():
    " confirm Entry checks maximum string length "
    e = pytest.raises(InputError, Entry, MakeEntryLines.extended_string())
    assert 'string too long: ' in e.value.message

@repeats(100)
def test_instantiation_with_a_tuple_containing_a_non_empty_last_line():
    " confirm Entry verifies last line in tuple as empty "
    if settings.last_line_empty:
        lines = MakeEntryLines.non_empty_last_line()
        e = pytest.raises(InputError, Entry, lines)
        assert 'last line in tuple not empty' == e.value.message

@repeats(1000)
def test_lines_to_figure_strings():
    " confirm lines_to_figure_strings properly parses random entry lines "
    account_string = MakeAccountString.random()
    entry_lines = account_string_to_lines(account_string)
    figure_strings = [numeral_to_figure_string(n) for n in account_string]
    assert lines_to_figure_strings(entry_lines) == figure_strings

@repeats(1000)
def test_correctly_parses_lines():
    " confirm Entry parses random entry lines into correct account strings "
    account_string = MakeAccountString.random()
    entry_lines = account_string_to_lines(account_string)
    e = Entry(tuple(entry_lines))
    assert e.account_string == account_string

future = """
@repeats(1000)
def test_recognition_of_non_figure_containing_lines():
    " confirm Entry rejects lines not containing only known figures "
    entry_lines = account_string_to_lines(account_string)
    adulterate lines
    e = Entry(tuple(adulterated_entry_lines))
    assert '?' in e.account_string
"""
