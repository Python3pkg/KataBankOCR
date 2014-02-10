"generator that yields Figures and the functions that support it"

from functools import partial

import settings
from validators import Validate

def figures_from_entries(entries):
    "generator that consumes Entries and yields figures"
    Validate.iterable(entries)
    for entry in entries:
        _validate_entry(entry)
        for figure in _figures_in_entry(entry):
            yield figure

def _figures_in_entry(entry):
    "return Figures within Entry"
    lists_of_substrings_by_line = map(_substrings_in_line, entry)
    figure_strings = zip(*lists_of_substrings_by_line)
    figures = map(''.join, figure_strings)
    return figures

def _validate_entry(entry):
    "confirm type, length, and composition of entry and its elements"
    Validate.type(list, entry, 'Entry')
    Validate.length(settings.lines_per_entry, entry, 'Entry')
    Validate.elements('type', basestring, entry, 'Entry Line')
    Validate.elements('length', settings.strokes_per_line, entry, 'Entry Line')
    Validate.elements('composition', settings.valid_strokes, entry, 'Entry Line')

def _substrings_in_line(line):
    "return list of Substrings within a single Line"
    substring = partial(_figure_substring_from_line, line=line)
    return map(substring, range(settings.figures_per_entry))

def _figure_substring_from_line(figure_index, line):
    "return the Strokes of a figure found within a Line"
    start_index = figure_index * settings.strokes_per_substring
    end_index = start_index + settings.strokes_per_substring
    return line[start_index:end_index]