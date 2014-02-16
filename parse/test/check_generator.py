"functions that return tests to show a generator validates its input"

import pytest

from common_tools import invalid_lengths, fit_to_length, adulterate_iterable
from fixtures import ArbitraryValues

def raises_on_non_iterable(generator):
    "return test of error raised on non-iterable input"
    def non_iterable_test():
        for non_iterable_value in ArbitraryValues.non_iterables():
            iterator = generator(non_iterable_value)
            error = pytest.raises(TypeError, list, iterator)
            assert 'not iterable' in error.value.message
    return non_iterable_test

def raises_on_bad_element_type(generator, value_or_type):
    "return test of error raised on element of unexpected type"
    def element_type_test():
        for bad_element in ArbitraryValues.of_different_type(value_or_type):
            iterator = generator([bad_element])
            error = pytest.raises(TypeError, list, iterator)
            assert 'unexpected type' in error.value.message
    return element_type_test

def raises_on_bad_element_length(generator, valid_element):
    "return test of error raised on element of unexpected length"
    valid_length = len(valid_element)
    def element_length_test():
        for invalid_length in invalid_lengths(valid_length):
            invalid_length_element = fit_to_length(valid_element, invalid_length)
            iterator = generator([invalid_length_element])
            error = pytest.raises(ValueError, list, iterator)
            assert 'unexpected length' in error.value.message
    return element_length_test

def raises_on_bad_element_composition(generator, valid_element, adulterants):
    "return test of error raised when element contains invalid element"
    def element_composition_test():
        for adulterant in adulterants:
            adulterated_element = adulterate_iterable(valid_element, adulterant)
            iterator = generator([adulterated_element])
            error = pytest.raises(TypeError, list, iterator)
            assert 'unexpected element' in error.value.message
    return element_composition_test
