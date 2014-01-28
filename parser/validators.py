" functions that raise errors on invalid input "

from errors import InputLengthError, InputTypeError

def validate_input_length(value, expected, name='Input'):
    " confirm value has expected length or raise InputLengthError "
    length = len(value)
    if len(value) != expected:
        raise(InputLengthError(name, expected, len(value)))

def validate_input_type(value, expected, name='Input'):
    " confirm value has expected type or raise InputTypeError "
    if not isinstance(value, expected):
        raise(InputTypeError(name, expected, type(value)))
