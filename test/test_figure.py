#!/usr/bin/env python

" Test the figure module "

import pytest
import random

import settings
from scanner_parser.figure import Figure
from figure_testing_tools import with_each, gen_strings
from figure_testing_tools import StringType


def test_instantiation_with_no_argument():
    with pytest.raises(TypeError):
        f = Figure()

@with_each(settings.figures.keys())
def test_instantiation_with_valid_string(fs):
    Figure(fs)

@with_each(gen_strings(50,StringType.too_short))
def test_insufficient_string_length(short_string):
    with pytest.raises('figure_string_too_short'):
        f = Figure(short_string)

@with_each(gen_strings(50,StringType.too_long))
def test_excessive_string_length(long_string):
    with pytest.raises('figure_string_too_long'):
        f = Figure(long_string)

@with_each(gen_strings(50,StringType.adulterated))
def test_adulterated_string(bad_string):
    with pytest.raises('invalid_figure_characters'):
        f = Figure(bad_string)

@with_each((1,False,True,3.14359,[]))
def test_non_string(non_string):
    with pytest.raises('not a string'):
        f = Figure(non_string)

@with_each(gen_strings(50,StringType.unrecognized))
def test_unrecognized_figures(unrecognized_string):
    with pytest.raises('unrecognized_figure'):
        f = Figure(unrecognized_string)

@with_each(gen_strings(50,StringType.recognized))
def test_recognized_figures(recognized_string):
    f = Figure(recognized_string)
    assert Figure.value == settings.figures[recognized_string]


#lines_per_entry
#figures_per_entry
#figure_width
#characters_per_figure
#valid_figure_characters
#figures
#last_line_empty
