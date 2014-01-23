#!/usr/bin/env python

import settings

class FigureError(Exception):
    " Base class for exceptions in this module "
    pass

class InputError(FigureError):
    " Exception raised for errors in the input "
    def __init__(self,msg):
        self.message = msg

class Figure():
    """ A multi-character string that represents a single character """

    def __init__(self,figure_string):
        self.figure_string = figure_string
        self.validate_string()
        self.parse_string()

    def validate_string(self):
        fs = self.figure_string
        if not isinstance(fs, str):
            raise(InputError(str(fs)+' not a string'))
        valid_characters = settings.valid_figure_characters
        if not set(fs).issubset(valid_characters):
            raise(InputError('"%s" contains invalid figure characters'%fs))
        length = settings.characters_per_figure
        if len(fs) < length:
            raise(InputError('"%s" too short. correct length: %d'%(fs,length)))
        if len(fs) > length:
            raise(InputError('"%s" too long. correct length: %d'%(fs,length)))

    def parse_string(self):
        if self.figure_string in settings.figures:
            self.value = settings.figures[self.figure_string]
        else:
            raise(InputError('unknown figure "%s"'%self.figure_string))

