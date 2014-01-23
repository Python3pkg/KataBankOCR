#!/usr/bin/env python

" The Entry Module "

import settings

from figure import Figure

class EntryError(Exception):
    " Base class for exceptions in this module "
    pass

class InputError(EntryError):
    " Exception raised for errors in the input "
    def __init__(self,msg):
        self.message = msg

def lines_to_figure_strings(lines):
    figure_count = settings.figures_per_entry
    figure_strings = ['' for i in range(figure_count)]
    for line_index in range(len(lines)):
        line = lines[line_index]
        for figure_index in range(figure_count):
            start_char_index = figure_index * settings.figure_width
            end_char_index = start_char_index + settings.figure_width
            substring = line[start_char_index:end_char_index]
            figure_strings[figure_index] += substring
    return figure_strings

class Entry():
    " Lines of characters containing figures that represent an account string "

    def __init__(self,lines):
        self.lines = lines
        self.validate_lines()
        self.parse_lines()

    def validate_lines(self):
        if not isinstance(self.lines,tuple):
            raise(InputError(str(self.lines)+' not a tuple'))
        if len(self.lines) < settings.lines_per_entry:
            raise(InputError('tuple too short'))
        if len(self.lines) > settings.lines_per_entry:
            raise(InputError('tuple too long'))
        if not all(isinstance(line,str) for line in self.lines):
            raise(InputError('non-string in tuple'))
        line_length = settings.figure_width * settings.figures_per_entry
        if any(len(line) < line_length for line in self.lines):
            raise(InputError('string in tuple too short'))
        if any(len(line) > line_length for line in self.lines):
            raise(InputError('string in tuple too long'))
        last_line = self.lines[settings.lines_per_entry-1]
        if settings.last_line_empty and len(last_line.strip()) > 0:
            raise(InputError('last line in tuple not empty'))

    def parse_lines(self):
        figure_strings = lines_to_figure_strings(self.lines)
        self.figures = [Figure(fs) for fs in figure_strings]
        figure_values = [f.value for f in self.figures]
        self.account_string = ''.join(figure_values)
