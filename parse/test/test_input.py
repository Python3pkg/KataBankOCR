"functions that confirm input validation"

import pytest
import random

from parse import settings
from parse.accounts import accounts_from_numerals

from common_tools import flatten, replace_element

class GeneratorRaises:
    "Confirm generator raises expected error on bad input"
    
    @classmethod
    def on_non_iterable(cls, function):
        "confirm error raised on non-iterable input"
        result = function(_get_non_iterable())
        pytest.raises(TypeError, list, result)

    @classmethod
    def on_non_string(cls, function):
        "confirm error raised on iterable that yields a non_string"
        iterable = [_get_non_string()]
        result = accounts_from_numerals(iterable)
        pytest.raises(TypeError, list, result)

    @classmethod
    def on_element_of_unexpected_length(cls, function, valid_element):
        "confirm error raised on iterable yielding unexpected length element"
        valid_length = len(valid_element)
        for invalid_length in _get_invalid_lengths(valid_length):
            invalid_length_element = _fit_to_length(valid_element, invalid_length)
            results = function([invalid_length_element])
            pytest.raises(ValueError, list, results)

def _get_non_string():
    "Return an arbitrary non-string value"
    some_non_strings = (0, 1, -10, False, True, [], (), {}, 3.14159)
    return random.choice(some_non_strings)


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

def _get_non_iterable():
    "return an arbitrary non-iterable value"
    some_non_iterables=(0, 1, -10, False, True, 3.14159)
    return random.choice(some_non_iterables)
