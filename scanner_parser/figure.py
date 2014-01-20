#!/usr/bin/env python

import settings

class FigureError(Exception):
    " Base class for exceptions in this module "
    pass

class InputError(FigureError):
    " Exception raised for errors in the input "
    def __init__(self,value):
        self.value = value

class Figure():
    """ A multi-character string that represents a single character """

    def __init__(self,figure_string):
        self.figure_string = figure_string
        self.validate_string()
        self.parse_string()

    def validate_string(self):
        if not isinstance(self.figure_string,str):
            raise(InputError('not a string'))
        valid_characters = settings.valid_figure_characters
        if not set(self.figure_string).issubset(valid_characters):
            raise(InputError('invalid figure characters'))
        if len(self.figure_string) < settings.characters_per_figure:
            raise(InputError('figure string too short'))
        if len(self.figure_string) > settings.characters_per_figure:
            raise(InputError('figure string too long'))

    def parse_string(self):
        if self.figure_string in settings.figures:
            self.value = settings.figures[self.figure_string]
        else:
            raise(InputError('unrecognized figure'))

