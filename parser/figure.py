import settings
from errors import InputError
from validators import validate_input_type, validate_input_length

class Figure():
    " A multi-character string that represents a single account character "

    def __init__(self, input):
        " validate input as figure string and identify account character "
        fs = self._validate_input_as_figure_string(input)
        self.account_character = self._figure_string_to_account_character(fs)

    def _validate_input_as_figure_string(self, input):
        " confirm type, length, and character composition or raise an error "
        validate_input_type(input, str, 'Figure input')
        validate_input_length(input, settings.figure_length, 'Figure string')
        self._validate_string_composition(input)
        return input
        
    def _validate_string_composition(self, input):
        " confirm figure string contains only valid characters or raise an error "
        valid_chars = settings.valid_figure_characters
        if not set(input).issubset(valid_chars):
            msg = 'Figure string "%s" contains non-figure character(s): %s'
            invalid_characters = sorted(list(set(input) - set(valid_chars)))
            raise(InputError(msg % (input, ''.join(invalid_characters))))

    def _figure_string_to_account_character(self, figure_string):
        " find figure string in settings dict or raise InputError "
        if figure_string in settings.figures:
            return settings.figures[figure_string]
        return '?'

