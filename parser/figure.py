#!/usr/bin/env python

from settings import figures, valid_figure_characters, figure_length
from validators import validate_input_type, validate_input_length
from errors import InputError

class Figure():
    " A multi-character string that represents a single account character "

    def __init__(self, input):
        " validate input as figure string and identify account character "
        fs = self.validate_input_as_figure_string(input)
        self.value = self.parse_figure_string_to_account_character(fs)

    def validate_input_as_figure_string(self, input):
        " confirm type, length, and character composition or raise an error "
        validate_input_type(input, str, 'Figure input')
        validate_input_length(input, figure_length, 'Figure input')
        self.validate_input_composition(input)
        return input
        
    def validate_input_composition(self, input):
        " confirm figure string contains only valid characters or raise an error "
        if not set(input).issubset(valid_figure_characters):
            msg = 'Figure input "%s" contains non-figure character(s): "%s"'
            invalid_characters = set(input) - set(valid_figure_characters)
            raise(InputError(msg % (input, str(invalid_characters))))

    def parse_figure_string_to_account_character(self, figure_string):
        " find figure string in settings dict or raise InputError "
        if figure_string in figures:
            return figures[figure_string]
        else:
            raise(InputError('unknown figure "%s"' % figure_string))

