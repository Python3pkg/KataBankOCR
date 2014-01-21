#!/usr/bin/env python

" Test the figure module "

import pytest

import settings

from testing_tools import repeats
from figure_testing_tools import gen_strings
from figure_testing_tools import StringGenerators as StrGen
from scanner_parser.figure import Figure, InputError

def test_instantiation_with_no_argument():
    " confirm Figure require more than zero arguments "
    with pytest.raises(TypeError):
        f = Figure()

def test_instantiation_with_multiple_arguments(min=2,max=10):
    " confirm Figure requires fewer than 2 arguments "
    args = min
    while args <= max:
        with pytest.raises(TypeError):
            f = Figure(*range(args))
        args += 1
    
def test_instantiation_with_valid_string():
    " confirm Figure instantiates with a valid string argument "
    for valid_string in settings.figures.keys():
        f = Figure(valid_string)
        assert isinstance(f,Figure)

def test_instantiation_with_non_string():
    " confirm Figure requires a string as its argument "
    arbitrary_non_string_values = (0,1,-10,False,True,3.14359,(),[],{},set())
    for non_string in arbitrary_non_string_values:
        with pytest.raises(InputError): # 'not a string'
            f = Figure(non_string)

@repeats(1000)
def test_instantiation_with_insufficient_string_length():
    " confirm Figure checks minimum string length "
    with pytest.raises(InputError): # 'figure string too short'
        f = Figure(StrGen.too_short())

@repeats(1000)
def test_instantiation_with_excessive_string_length():
    " confirm Figure checks maximum string length "
    with pytest.raises(InputError): # 'figure string too long'
        f = Figure(StrGen.too_long())

def test_instantiation_with_adulterated_string():
    " confirm Figure checks for inappropriate characters in its input string "
    for bad_string in gen_strings(50,StrGen.adulterated):
        with pytest.raises(InputError): # 'invalid figure characters'
            f = Figure(bad_string)

def test_instantiation_with_unknown_string():
    " confirm Figure refuses unknown strings "
    for unknown_string in gen_strings(50,StrGen.unknown):
        with pytest.raises(InputError): # 'unknown figure'
            f = Figure(unknown_string)

def test_instantiation_with_known_string():
    " confirm Figure correctly identifies known strings "
    for known_string in gen_strings(50,StrGen.known):
        f = Figure(known_string)
        expected = settings.figures[known_string]
        actual = f.value
        assert actual == expected
