"functions that return tests showing that generator functions validate their input"

import pytest
from common_tools import replace_element
import fixtures

def raises_on_non_iterable(generator):
    "return test of error raised on non-iterable input"
    def non_iterable_test():
        for non_iterable_value in fixtures.ArbitraryValues.non_iterable():
            iterator = generator(non_iterable_value)
            pytest.raises(TypeError, list, iterator)
    return non_iterable_test

def raises_on_bad_element_type(generator, value_or_type):
    "return test of error raised on element of unexpected type"
    def element_type_test():
        for bad_element in fixtures.ArbitraryValues.of_different_type(value_or_type):
            iterator = generator([bad_element])
            pytest.raises(TypeError, list, iterator)
    return element_type_test

def raises_on_bad_element_length(generator, valid_element):
    "return test of error raised on element of unexpected length"
    valid_length = len(valid_element)
    def element_length_test():
        for invalid_length in _get_invalid_lengths(valid_length):
            invalid_length_element = _fit_to_length(valid_element, invalid_length)
            iterator = generator([invalid_length_element])
            pytest.raises(ValueError, list, iterator)
    return element_length_test

def raises_on_bad_element_composition(generator, valid_element, adulterants):
    "return test of error raised when element contains invalid element"
    def element_composition_test():
        for adulterant in adulterants:
            adulterated_element = replace_element(valid_element, adulterant)
            iterator = generator([adulterated_element])
            pytest.raises(TypeError, list, iterator)
    return element_composition_test

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

