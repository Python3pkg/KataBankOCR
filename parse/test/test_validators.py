"test the validators module"

import pytest
import random

from parse.validators import Validate
import fixtures

@pytest.fixture
def name():
    "return an arbitrary name"
    some_arbitrary_names = ('Thing', 'This', 'an ITEM', 'some name')
    return random.choice(some_arbitrary_names)

class TestType():
    "exercise the Validate.type classmethod"

    matched_type_value_pairs = ((basestring, 'foo'), (list, []), (tuple, ()), (int, 1))
    @pytest.mark.parametrize("expected_type, value", matched_type_value_pairs)
    def test_with_valid_type(self, expected_type, value, name):
        "confirm passes silently on value of valid type"
        assert None == Validate.type(expected_type, value, name)

    mismatched_type_value_pairs = ((int, 'A',), (tuple, [],), (basestring, (1,)))
    @pytest.mark.parametrize("expected_type, value", mismatched_type_value_pairs)
    def test_with_invalid_type(self, expected_type, value, name):
        "confirm raises correctly on invalid type"
        message = '%s "%s" of unexpected type. Expected:%s. Found:%s.'
        message = message % (name, value, expected_type, str(type(value)))
        arguments = (expected_type, value, name)
        e = pytest.raises(TypeError, Validate.type, *arguments)
        assert message == e.value.message

class TestLength():
    "exercise the Validate.length classmethod"

    matched_length_value_pairs = ((0, ''), (0, []), (0, ()), (1, 'A'),
                                  (2, 'ab'), (2, [1, 2]), (3, (1, 2, 3)))
    @pytest.mark.parametrize("length, value", matched_length_value_pairs)
    def test_with_valid_length(self, length, value, name):
        "confirm passes silently on value of valid length"
        assert None == Validate.length(length, value, name)

    mismatched_length_value_pairs = ((2, 'A',), (1, []), (0, (1,)))
    @pytest.mark.parametrize("expected_length, value", mismatched_length_value_pairs)
    def test_with_invalid_length(self, expected_length, value, name):
        "confirm raises correctly on invalid length"
        message = '%s "%s" of unexpected length. Expected:%d. Found:%d.'
        message = message % (name, value, expected_length, len(value))
        arguments = (expected_length, value, name)
        e = pytest.raises(ValueError, Validate.length, *arguments)
        assert message == e.value.message

class TestComposition():
    "exercise the Validate.composition classmethod"

    matched_components_value_pairs = ((['a', 'b', 'c'], 'baabccab'),
                                      (['ab', 'XY', 'zz'], ('XY', 'ab', 'ab')),
                                      ((10, 20, 30), [20, 10, 10]),
                                      ([0, 1, 2, 3], (1, 2, 2, 1, 0)),
                                      ([1, 2, 3], ()),)
    @pytest.mark.parametrize("allowed_components, value", matched_components_value_pairs)
    def test_with_valid_composition(self, allowed_components, value, name):
        "confirm passes silently on value with allowed components"
        assert None == Validate.composition(allowed_components, value, name)

    mismatched_components_value_index_triads = ((['a', 'b', 'c'], 'abcd', 3),
                                                ((10, 20, 30), [1, 2], 0),
                                                ([0, 1, 2, 3], (2, 4, 6), 1),)
    @pytest.mark.parametrize("allowed_components, value, bad_index",
                             mismatched_components_value_index_triads)
    def test_with_invalid_composition(self, allowed_components, value, bad_index, name):
        "confirm raises correctly on value containing an unexpected element"
        element = value[bad_index]
        message = '%s "%s" contains unexpected element "%s" at index %d'
        message = message % (name, value, element, bad_index)
        arguments = (allowed_components, value, name)
        e = pytest.raises(TypeError, Validate.composition, *arguments)
        assert message == e.value.message

class TestIterable():
    "exercise the Validate.iterable classmethod"

    @pytest.mark.parametrize("iterable", fixtures.ArbitraryValues.iterables())
    def test_with_iterable(self, iterable):
        "confirm passes silently on iterable value"
        assert None == Validate.iterable(iterable)

    @pytest.mark.parametrize("non_iterable", fixtures.ArbitraryValues.non_iterables())
    def test_with_non_iterable(self, non_iterable):
        "confirm raises correctly on non-iterable value"
        e = pytest.raises(TypeError, Validate.iterable, non_iterable)
        message = '"%s" not iterable' % str(non_iterable)
        assert message == e.value.message
