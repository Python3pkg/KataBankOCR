from errors import InputLengthError, InputTypeError

class Validate():
    " methods that raise errors on invalid input "

    @classmethod
    def length(cls, expected, found, name='Input'):
        " confirm found has expected length or raise InputLengthError "
        length = len(found)
        if len(found) != expected:
            message = cls._build_message('length', expected, len(found), name)
            raise(InputLengthError(message))

    @classmethod
    def type(cls, expected, found, name='Input'):
        " confirm found of expected type or raise InputTypeError "
        if not isinstance(found, expected):
            message = cls._build_message('type', expected, type(found), name)
            raise(InputTypeError(message))

    @classmethod
    def _build_message(cls, error, expected, found, name):
        msg = '%s of unexpected %s. Expected:%s. Found:%s.'
        return msg % (name, error, str(expected), str(found))

    @classmethod
    def element_types(cls, expected, found, name='Input Element'):
        " validate type of each element "
        for element_index in range(len(found)):
            found_element = found[element_index]
            element_name = name + ' ' + str(element_index)
            cls.type(expected, found_element, element_name)

    @classmethod
    def element_lengths(cls, expected, found, name='Input Element'):
        " validate length of each element "
        for element_index in range(len(found)):
            found_element = found[element_index]
            element_name = name + ' ' + str(element_index)
            cls.length(expected, found_element, element_name)


