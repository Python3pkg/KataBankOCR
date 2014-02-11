"functions that return tests showing other funcs validate their input"

import pytest

def raises_on_non_iterable(function):
    "return test of error raised on non-iterable input"
    some_non_iterables=(0, 1, -10, False, True, 3.14159)
    def non_iterable_test():
        for value in some_non_iterables:
            result = function(value)
            pytest.raises(TypeError, list, result)
    return non_iterable_test

def raises_on_bad_element_type(function, valid_element):
    "return test of error raised on iterable that yields a non_string"
    def element_type_test():
        for bad_element in _get_values_of_different_type(valid_element):
            iterable = [bad_element]
            result = function(iterable)
            pytest.raises(TypeError, list, result)
    return element_type_test

def raises_on_bad_element_length(function, valid_element):
    "confirm error raised on iterable yielding unexpected length element"
    valid_length = len(valid_element)
    def element_length_test():
        for invalid_length in _get_invalid_lengths(valid_length):
            invalid_length_element = _fit_to_length(valid_element, invalid_length)
            results = function([invalid_length_element])
            pytest.raises(ValueError, list, results)
    return element_length_test

def _get_values_of_different_type(obj):
    "Return an arbitrary non-string value"
    some_arbitrary_values = (0, 1, -10, False, True, [], (), {}, 3.14159, None,
                             'abc', [1,2,3], '', {1:2}, {0}, -1.1, object)
    avoided_type = type(obj)
    different_type = lambda value: not isinstance(value, avoided_type)
    return filter(different_type, some_arbitrary_values)

def _get_invalid_lengths(valid_length, multiplier=4):
    "return ints 0 to (valid_length * multiplier) excluding valid_length"
    maximum_length_to_test = valid_length * multiplier
    lengths = range(maximum_length_to_test + 1)
    return [L for L in lengths if L != valid_length]

def _fit_to_length(value, length):
    "return duplicated & abbreviated value such that len(value) == length"
    if len(value) == length:
        return value
    elif len(value) > length:
        return value[:length]
    # Still too short. Double it and recurse.
    return _fit_to_length(value + value, length)
