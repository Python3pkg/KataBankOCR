#!/usr/bin/env python

" Test the figure module "

import pytest
import random

import settings
from scanner_parser.figure import Figure

def random_valid_character():
    " return a randomly selected valid figure character "
    return random.choice(settings.valid_figure_characters)

def random_string(length):
    " return a string built of randomly seleced valid figure characters "
    return ''.join(random_valid_character() for c in range(length))

def random_valid_string():
    " return a proper length string of random valid figure characters "
    return random_string(settings.characters_per_figure)

def too_short_strings():
    """ return ever longer random strings

    compose strings strictly of valid figure characters
    begin with a single character string
    give each subsequent string one more character
    stop before returning a string of valid length
    """
    length = 1
    while length < settings.characters_per_figure:
        yield random_string(length)
        length += 1

def too_long_strings():
    """ return ever shorter random strings

    compose strings strictly of valid figure characters
    begin with a string of twice the appropriate length
    give each subsequent string one fewer character
    stop before returning a string of valid length
    """
    length = settings.characters_per_figure * 2
    while length > settings.characters_per_figure:
        yield random_string(length)
        length -= 1


def with_each(items):
    " decorate a function by calling it once for each item in iterable "
    def decorated_function(function):
        for i in items:
            function(i)
    return decorated_function

# Tests

def test_instantiation_with_no_argument():
    with pytest.raises(TypeError):
        f = Figure()

@with_each(settings.figures.keys())
def test_instantiation_with_valid_string(fs):
    Figure(fs)

@with_each(too_short_strings())
def test_insufficient_string_length(short_string):
    with pytest.raises('figure_string_too_short'):
        f = Figure(short_string)

@with_each(too_long_strings())
def test_excessive_string_length(long_string):
    with pytest.raises('figure_string_too_long'):
        f = Figure(long_string)


#lines_per_entry
#figures_per_entry
#figure_width
#characters_per_figure
#valid_figure_characters
#figures
#last_line_empty


