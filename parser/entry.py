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

    def validate_lines_type(self):
        " confirm lines references of a tuple of strings "
        if not isinstance(self.lines, tuple):
            msg = '"%s" not a tuple.'
            raise(InputError(msg % str(self.lines)))
        for line in self.lines:
            if not isinstance(line,str):
                raise(InputError('non-string in tuple'))


    def validate_line_count(self):
        " confirm tuple has appropriate length "
        count = len(self.lines)
        expected = settings.lines_per_entry
        if count != expected:
            msg = 'tuple wrong length. counted %s and expected %d.'
            raise(InputError(msg % (expected, count)))

    def validate_line_lengths(self):
        " confirm each line in tuple has appropriate length "
        valid_line_length = settings.figure_width * settings.figures_per_entry
        for line in self.lines:
            if len(line) < valid_line_length:
                raise(InputError('string too short: "%s"' % line))
            if len(line) > valid_line_length:
                raise(InputError('string too long: "%s"' % line))

    def validate_lines(self):
        self.validate_lines_type()
        self.validate_line_count()
        self.validate_line_lengths()

        last_line = self.lines[settings.lines_per_entry-1]
        if settings.last_line_empty and len(last_line.strip()) > 0:
            raise(InputError('last line in tuple not empty'))

    def parse_lines(self):
        figure_strings = lines_to_figure_strings(self.lines)
        self.figures = [Figure(fs) for fs in figure_strings]
        figure_values = [f.value for f in self.figures]
        self.account_string = ''.join(figure_values)
