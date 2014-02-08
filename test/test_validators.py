" test validators "

import pytest
import random

from parser.validators import Validate

@pytest.fixture
def name():
    " return an arbitrary name "
    some_arbitrary_names = ('Thing', 'This', 'an ITEM', 'some name')
    return random.choice(some_arbitrary_names)

class TestType():
    " exercise the Validate.type classmethod "

    matched_type_value_pairs = ((basestring, 'foo'), (list, []), (tuple, ()), (basestring, 'foo',))
    @pytest.mark.parametrize("expected_type, value", matched_type_value_pairs)
    def test_with_valid_type(self, expected_type, value, name):
        " confirm passes silently on value of valid type "
        assert None == Validate.type(expected_type, value, name)

    mismatched_type_value_pairs = ((int, 'A',), (tuple, [],), (basestring, (1,)))
    @pytest.mark.parametrize("expected_type, value", mismatched_type_value_pairs)
    def test_with_invalid_type(self, expected_type, value, name):
        " confirm raises correctly on invalid type "
        message = '%s "%s" of unexpected type. Expected:%s. Found:%s.'
        message = message % (name, value, expected_type, str(type(value)))
        arguments = (expected_type, value, name)
        e = pytest.raises(TypeError, Validate.type, *arguments)
        assert message == e.value.message

class TestLength():
    " exercise the Validate.length classmethod "

    matched_length_value_pairs = ((0, ''), (0, []),  (0, ()), (1, 'A'), 
                                  (2, 'ab'), (2, [1, 2]), (3, (1, 2, 3)))
    @pytest.mark.parametrize("length, value", matched_length_value_pairs)
    def test_with_valid_length(self, length, value, name):
        " confirm passes silently on value of valid length "
        assert None == Validate.length(length, value, name)


    mismatched_length_value_pairs = ((2, 'A',), (1, []), (0, (1,)))
    @pytest.mark.parametrize("expected_length, value", mismatched_length_value_pairs)
    def test_with_invalid_length(self, expected_length, value, name):
        " confirm raises correctly on invalid length "
        message = '%s "%s" of unexpected length. Expected:%d. Found:%d.'
        message = message % (name, value, expected_length, len(value))
        arguments = (expected_length, value, name)
        e = pytest.raises(ValueError, Validate.length, *arguments)
        assert message == e.value.message

class TestComposition():
    " exercise the Validate.composition classmethod "

    matched_components_value_pairs = (
        (['a','b','c'], 'baabccab'),
        (['ab','XY','zz'], ('XY','ab','ab')),
        ((10,20,30), [20,10,10,]),
        ([0,1,2,3], (1,2,2,1,0)),
        ([1,2,3], ()),
        )
    @pytest.mark.parametrize("allowed_components, value", matched_components_value_pairs)
    def test_with_valid_composition(self, allowed_components, value, name):
        " confirm passes silently on value with allowed components "
        assert None == Validate.composition(allowed_components, value, name)

    mismatched_components_value_index_triads = (
        (['a','b','c'], 'abcd', 3),
        ((10,20,30), [1,2], 0),
        ([0,1,2,3], (2,4,6), 1),
        )
    @pytest.mark.parametrize("allowed_components, value, bad_index",
                             mismatched_components_value_index_triads)
    def test_with_invalid_composition(self, allowed_components, value, bad_index, name):
        " confirm detection of value containing an unexpected element "
        element = value[bad_index]
        message = '%s "%s" contains unexpected element "%s" at index %d'
        message = message % (name, value, element, bad_index)
        arguments = (allowed_components, value, name)
        e = pytest.raises(TypeError, Validate.composition, *arguments)
        assert message == e.value.message


class TestElements():
    " exercise the Validate.elements classmethod "

    nearly_all_lists = (['foo',], [], [1,2,], 'not_a_list', ['a',''])
    nearly_all_tuples = ((), ('foo',), ['non_tuple',], (1,2,), ('a',''))
    nearly_all_length_zero = ('', (), [], {}, 'x')
    nearly_all_length_one = ('a', '', [3,], ('b',), '1')
    nearly_all_composed_of_a_b_or_c = ('abc', 'bad', ['b',], ('c', 'a'), (), [])
    nearly_all_composed_of_1_2_or_3 = ((1,2), (1,), [2,3], (), [4], [])
    @pytest.mark.parametrize("validator_name, error, expectation, iterable, bad_index", (
            ('type', TypeError, list, nearly_all_lists, 3),
            ('type', TypeError, tuple, nearly_all_tuples, 2),
            ('length', ValueError, 0, nearly_all_length_zero, 4),
            ('length', ValueError, 1, nearly_all_length_one, 1),
            ('composition', TypeError, 'abc', nearly_all_composed_of_a_b_or_c, 1),
            ('composition', TypeError, (1,2,3), nearly_all_composed_of_1_2_or_3, 4),
            ))
    def test_elemts(self, validator_name, error, expectation, iterable, bad_index, name):
        " confirm validation of iterable containing faulty element "
        arguments = (validator_name, expectation, iterable, name)
        e = pytest.raises(error, Validate.elements, *arguments)
        item = iterable[bad_index]
        msg = '%s %d "%s"' % (name, bad_index, item)
        assert msg in e.value.message

class TestIterable():
    " exercise the Validate.iterable classmethod "

    some_iterables = ('', (), [], {}, 'abcde', (1,2,3), [1,2,3], {1,2,3})
    @pytest.mark.parametrize("iterable", some_iterables)
    def test_with_iterable(self, iterable):
        " confirm passes silently on iterable value "
        assert None == Validate.iterable(iterable)

    def test_with_non_iterable(self, non_iterable):
        " confirm raises correctly on invalid type "
        e = pytest.raises(TypeError, Validate.iterable, non_iterable)
        message = '"%s" not iterable' % str(non_iterable)
        assert message == e.value.message

