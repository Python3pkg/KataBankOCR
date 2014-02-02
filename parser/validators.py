" functions that raise errors on invalid input "

from errors import InputLengthError, InputTypeError

def validate_length(expected, found, name='Input'):
    " confirm found has expected length or raise InputLengthError "
    length = len(found)
    if len(found) != expected:
        message = _build_message('length', expected, len(found), name)
        raise(InputLengthError(message))

def validate_type(expected, found, name='Input'):
    " confirm found of expected type or raise InputTypeError "
    if not isinstance(found, expected):
        message = _build_message('type', expected, type(found), name)
        raise(InputTypeError(message))

def validate_element_types(expected, found, name='Input Element'):
    " raise InputTypeError if found has element of unexpected type "
    for element_index in range(len(found)):
        found_element = found[element_index]
        element_name = name + ' ' + str(element_index)
        validate_type(expected, found_element, element_name)

def validate_element_lengths(expected, found, name='Input Element'):
    " raise InputTypeError if found has element of unexpected length "
    for element_index in range(len(found)):
        found_element = found[element_index]
        element_name = name + ' ' + str(element_index)
        validate_length(expected, found_element, element_name)

def _build_message(error, expected, found, name):
    msg = '%s of unexpected %s. Expected:%s. Found:%s.'
    return msg % (name, error, str(expected), str(found))

