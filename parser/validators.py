from errors import InputLengthError, InputTypeError

class Validate():
    " methods that raise errors on invalid input "

    @classmethod
    def iterable(cls, lines):
        " confirm we can iterate over value "
        try:
            iterator = iter(lines)
        except TypeError:
            message = '"%s" not an interator' % str(lines)
            raise(InputTypeError(message))

    @classmethod
    def type(cls, expected_type, value, name='Input'):
        " confirm value of expected type or raise InputTypeError "
        if not isinstance(value, expected_type):
            message = _build_message('type', expected_type, type(value), name)
            raise(InputTypeError(message))

    @classmethod
    def length(cls, expected_length, value, name='Input'):
        " confirm value has expected length or raise InputLengthError "
        length = len(value)
        if len(value) != expected_length:
            message = _build_message('length', expected_length, len(value), name)
            raise(InputLengthError(message))

    @classmethod
    def element_types(cls, expected_type, value, name='Input Element'):
        " validate type of each element "
        for index, element in enumerate(value):
            element_name = name + ' ' + str(index)
            cls.type(expected_type, element, element_name)

    @classmethod
    def element_lengths(cls, expected_length, value, name='Input Element'):
        " validate length of each element "
        for index, element in enumerate(value):
            element_name = name + ' ' + str(index)
            cls.length(expected_length, element, element_name)

def _build_message(error, expected, value, name):
    msg = '%s of unexpected %s. Expected:%s. Found:%s.'
    return msg % (name, error, str(expected), str(value))

