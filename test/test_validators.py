" test validators "
import pytest

from parser.errors import InputTypeError, InputLengthError
from parser.validators import validate_type, validate_length
from parser.validators import validate_element_types, validate_element_lengths

@pytest.mark.parametrize("validator, error, args", [
        (validate_length, InputLengthError, (1, '')),
        (validate_length, InputLengthError, (4, [1,2,3])),
        (validate_length, InputLengthError, (5, 'abcd')),
        (validate_type, InputTypeError, (list, '')),
        (validate_type, InputTypeError, (str, ['',])),
        (validate_type, InputTypeError, (int, '')),
        (validate_element_types, InputTypeError, (list, ['',])),
        (validate_element_types, InputTypeError, (str, ('', 1))),
        (validate_element_types, InputTypeError, (int, ('', 1))),
        (validate_element_types, InputTypeError, (tuple, ['', 1])),
        (validate_element_types, InputTypeError, (tuple, ('', 1))),
        (validate_element_lengths, InputLengthError, (2, ['a',])),
        (validate_element_lengths, InputLengthError, (1, ('ab', [1,2]))),
        (validate_element_lengths, InputLengthError, (1, ((),[1]))),
        (validate_element_lengths, InputLengthError, (1, ['',()])),
        (validate_element_lengths, InputLengthError, (3, ['abc',[0,1,2,3]])),
        ])
def test_validator_raises_appropriate_error_type(validator, error, args):
    " confirm each validator raises the appropriate error "
    assert pytest.raises(error, validator, *args)

@pytest.mark.parametrize("arguments, message", (
        ( (2, 'A'), "Input of unexpected length. Expected:2. Found:1."),
        ( (1, [], 'Given name'), "Given name of unexpected length. Expected:1. Found:0."),
        ))
def test_length_error_includes_expected_message(arguments, message):
    " confirm InputLengthError contains information helpful to the caller "
    e = pytest.raises(InputLengthError, validate_length, *arguments)
    assert e.value.message == message

@pytest.mark.parametrize("arguments, message", (
        ((list, 'foo'), "Input of unexpected type. Expected:<type 'list'>. Found:<type 'str'>."),
        ((list, 'foo', 'FooBar'), 
         "FooBar of unexpected type. Expected:<type 'list'>. Found:<type 'str'>."),
        ))
def test_type_error_includes_expected_message(arguments, message):
    " confirm InputTypeError contains information helpful to the caller "
    e = pytest.raises(InputTypeError, validate_type, *arguments)
    assert e.value.message == message

@pytest.mark.parametrize("arguments, message", (
        ((str, ['', 1]), 
         "Input Element 1 of unexpected type. Expected:<type 'str'>. Found:<type 'int'>."),
        ((list, ([],[1,2],1), 'BumBuz'), 
         "BumBuz 2 of unexpected type. Expected:<type 'list'>. Found:<type 'int'>."),
        ((int, ['a', 2, 1], 'BilBoe'), 
         "BilBoe 0 of unexpected type. Expected:<type 'int'>. Found:<type 'str'>."),
        ))
def test_type_error_includes_expected_message(arguments, message):
    " confirm InputElementLengthError contains information helpful to the caller "
    e = pytest.raises(InputTypeError, validate_element_types, *arguments)
    assert e.value.message == message

@pytest.mark.parametrize("validator, args", [
        (validate_type, (str, 'foo')),
        (validate_type, (list, [])),
        (validate_type, (tuple, ())),
        (validate_type, (str, 'foo', 'Named input')),
        (validate_length, (0, '')),
        (validate_length, (0, [])),
        (validate_length, (0, ())),
        (validate_length, (1, 'A')),
        (validate_length, (2, [1, 2])),
        (validate_length, (3, (1, 2, 3))),
        (validate_length, (0, '', 'Named input')),
        (validate_element_types, (str, 'foo')),
        (validate_element_types, (list, ([],[1]))),
        (validate_element_types, (tuple, [('a',)])),
        (validate_element_types, (str, ['foo',''], 'Named input')),
        (validate_element_lengths, (1, ['a',])),
        (validate_element_lengths, (2, ('ab', [1,2]))),
        (validate_element_lengths, (1, (('a'),[1]))),
        (validate_element_lengths, (0, ['',()])),
        (validate_element_lengths, (3, ['abc',[0,1,2]])),
        ])
def test_validator_passes_silently_on_good_input(validator, args):
    " confirm validator returns nothing when given valid input "
    assert None == validator(*args)
