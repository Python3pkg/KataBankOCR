#!/usr/bin/env python

import settings

class EntryError(Exception):
    " Base class for exceptions in this module "
    pass

class InputError(EntryError):
    " Exception raised for errors in the input "
    def __init__(self,value):
        self.value = value

class Entry():
    " Lines of characters containing figures that represent an account number "
    def __init__(self,lines):
        self.lines = lines
        self.validate_lines()
        self.parse_lines()

    def validate_lines(self):
        if not isinstance(self.lines,tuple):
            raise(InputError('not a tuple'))
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
        pass

