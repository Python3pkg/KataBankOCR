#!/usr/bin/env python

" Test the figure module "

import pytest

import settings

from tools.decorators import repeats
from tools.makers.figure_string import MakeFigureString
from parser.figure import Figure, InputError

def test_instantiation_with_no_argument():
    " confirm Figure require more than zero arguments "
    pytest.raises(TypeError,Figure)

def test_instantiation_with_multiple_arguments(min=2,max=10):
    " confirm Figure requires fewer than 2 arguments "
    for arg_count in range(min,max+1):
        pytest.raises(TypeError, Figure, *range(arg_count))
    
def test_instantiation_with_valid_string():
    " confirm Figure instantiates with a valid string argument "
    for valid_string in settings.figures.keys():
        f = Figure(valid_string)
        assert isinstance(f,Figure)

def test_instantiation_with_non_string():
    " confirm Figure requires a string as its argument "
    arbitrary_non_string_values = (0,1,-10,False,True,3.14,(),[],{},set())
    for non_string in arbitrary_non_string_values:
        e = pytest.raises(InputError, Figure, non_string)
        assert str(e.value.message) == 'not a string'

@repeats(100)
def test_instantiation_with_insufficient_string_length():
    " confirm Figure checks minimum string length "
    e = pytest.raises(InputError, Figure, MakeFigureString.too_short())
    assert e.value.message == 'figure string too short'

@repeats(100)
def test_instantiation_with_excessive_string_length():
    " confirm Figure checks maximum string length "
    e = pytest.raises(InputError, Figure, MakeFigureString.too_long())
    assert e.value.message == 'figure string too long'

@repeats(100)
def test_instantiation_with_adulterated_string():
    " confirm Figure checks for inappropriate characters in its input string "
    e = pytest.raises(InputError, Figure, MakeFigureString.adulterated())
    assert e.value.message == 'invalid figure characters'

@repeats(1000)
def test_instantiation_with_unknown_string():
    " confirm Figure refuses unknown strings "
    e = pytest.raises(InputError, Figure, MakeFigureString.unknown())
    assert e.value.message == 'unknown figure'

@repeats(1000)
def test_instantiation_with_known_string():
    " confirm Figure correctly identifies known strings "
    known_string = MakeFigureString.known()
    f = Figure(known_string)
    expected = settings.figures[known_string]
    actual = f.value
    assert actual == expected
