"generator that yields Figures and the functions that support it"

from toolz import curry, pipe, partition
from toolz.curried import map as cmap

from parse import settings
from parse.validators import Validate

def figures_from_entries(entries):
    "generator that consumes Entries and yields figures"
    for entry in entries:
        _validate_entry(entry)
        for figure in _figures_in_entry(entry):
            yield figure

def _validate_entry(entry):
    "confirm type, length, and composition of entry and its elements"
    Validate.type(tuple, entry, 'Entry')
    Validate.length(settings.lines_per_entry, entry, 'Entry')
    for line in entry:
        Validate.type(str, line, 'Entry Line')
        Validate.length(settings.strokes_per_line, line, 'Entry Line')
        Validate.composition(settings.valid_strokes, line, 'Entry Line')

def _figures_in_entry(entry):
    "return Figures within Entry"
    figure_strings = list(zip(*list(map(_substrings_in_line, entry))))
    return list(map(''.join, figure_strings))

def _substrings_in_line(line):
    "return list of Substrings within a single Line"
    splitter = curry(partition, settings.strokes_per_substring)
    return pipe(line, splitter, cmap(''.join))
