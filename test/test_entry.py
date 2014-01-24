#!/usr/bin/env python

""" Test the entry module"""

import pytest
import random

import settings

from tools.decorators import repeats
from tools.makers.account_string import MakeAccountString
from tools.makers.entry_lines import MakeEntryLines
from tools.translators import account_string_to_lines, numeral_to_figure_string
from parser.errors import InputError, InputTypeError, InputLengthError
from parser.entry import Entry

def test_instantiation_with_no_argument():
    " confirm Entry requires more than zero arguments "
    pytest.raises(TypeError, Entry)

def test_instantiation_with_multiple_arguments(min=2,max=10):
    " confirm Entry requires fewer than 2 arguments "
    for arg_count in range(min,max+1):
        pytest.raises(TypeError, Entry, *range(arg_count))
    
@repeats(50)
def test_instantiation_with_valid_lines():
    " confirm Entry instantiates with a valid list of lines "
    e = Entry(MakeEntryLines.random())
    assert isinstance(e,Entry)

def test_instantiation_with_non_list():
    " confirm Entry requires a list as its argument "
    arbitrary_non_list_values = (0,1,-10,False,True,3.14359,'',(),{},set())
    for non_string in arbitrary_non_list_values:
        e = pytest.raises(InputError, Entry, non_string)
        assert 'unexpected type' in e.value.message
#        assert str(type(foo)) in e.value.message
#        assert str(settings.lines_per_entry) in e.value.message

@repeats(50)
def test_instantiation_with_list_of_insufficient_length():
    " confirm Entry recognizes an insufficient length list "
    length = random.choice(range(1, settings.lines_per_entry))
    lines = MakeEntryLines.random()[:length]
    e = pytest.raises(InputError, Entry, lines)
    assert 'unexpected length' in e.value.message
    assert str(length) in e.value.message
    assert str(settings.lines_per_entry) in e.value.message

@repeats(50)
def test_instantiation_with_list_of_excessive_length():
    " confirm Entry recognizes an excessive length list "
    shortest_length_to_test = settings.lines_per_entry + 1
    longest_length_to_test = settings.lines_per_entry * 5 + 1
    length = random.choice(range(shortest_length_to_test, longest_length_to_test))
    lines = [MakeEntryLines.random()[0] for i in range(length)]
    e = pytest.raises(InputError,Entry, lines)
    assert 'unexpected length' in e.value.message
    assert str(length) in e.value.message
    assert str(settings.lines_per_entry) in e.value.message

@repeats(50)
def test_instantiation_with_list_containing_a_non_string():
    " confirm Entry checks type of all list values "
    e = pytest.raises(InputError, Entry, MakeEntryLines.containing_non_string())
    assert 'unexpected type' in e.value.message
#    assert type(foo) in e.value.message
    assert str(type('')) in e.value.message

@repeats(500)
def test_instantiation_with_a_list_containing_too_short_a_string():
    " confirm Entry checks minimum string length "
    e = pytest.raises(InputError, Entry, MakeEntryLines.abbreviated_string())
    assert 'unexpected length' in e.value.message
#    assert str(foo) in e.value.message
#    assert str(foo) in e.value.message

@repeats(500)
def test_instantiation_with_a_list_containing_too_long_a_string():
    " confirm Entry checks maximum string length "
    e = pytest.raises(InputError, Entry, MakeEntryLines.extended_string())
    assert 'unexpected length' in e.value.message
#    assert str(foo) in e.value.message
#    assert str(foo) in e.value.message

@repeats(100)
def test_instantiation_with_a_list_containing_a_non_empty_last_line():
    " confirm Entry verifies last line in list as empty "
    if settings.last_line_empty:
        lines = MakeEntryLines.non_empty_last_line()
        e = pytest.raises(InputError, Entry, lines)
        assert 'last line in list not empty' in e.value.message

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
