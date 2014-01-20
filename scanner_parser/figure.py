#!/usr/bin/env python

import settings

class Figure():
    """ A multi-character string that represents a single character """

    def __init__(self,figure_string):
        self.figure_string = figure_string
        self.validate_string()
        self.parse_string()
    
    def validate_string(self):
        if not isinstance(self.figure_string,str):
            raise('not a string')
        valid_characters = settings.valid_figure_characters
        if not set(self.figure_string).issubset(valid_characters):
            raise('invalid_figure_characters')
        if len(self.figure_string) < settings.characters_per_figure:
            raise('figure_string_too_short')
        if len(self.figure_string) > settings.characters_per_figure:
            raise('figure_string_too_long')

    def parse_string(self):
        if self.figure_string in settings.figures:
            self.value = settings.figures[self.figure_string]
        else:
            raise('unrecognized_figure')
