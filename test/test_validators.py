" test validators "
import pytest

from parser.errors import InputTypeError, InputLengthError
from parser.validators import Validate

@pytest.mark.parametrize("validator, error, args", [
        (Validate.length, InputLengthError, (1, '')),
        (Validate.length, InputLengthError, (4, [1,2,3])),
        (Validate.length, InputLengthError, (5, 'abcd')),
        (Validate.type, InputTypeError, (list, '')),
        (Validate.type, InputTypeError, (str, ['',])),
        (Validate.type, InputTypeError, (int, '')),
        (Validate.element_types, InputTypeError, (list, ['',])),
        (Validate.element_types, InputTypeError, (str, ('', 1))),
        (Validate.element_types, InputTypeError, (int, ('', 1))),
        (Validate.element_types, InputTypeError, (tuple, ['', 1])),
        (Validate.element_types, InputTypeError, (tuple, ('', 1))),
        (Validate.element_lengths, InputLengthError, (2, ['a',])),
        (Validate.element_lengths, InputLengthError, (1, ('ab', [1,2]))),
        (Validate.element_lengths, InputLengthError, (1, ((),[1]))),
        (Validate.element_lengths, InputLengthError, (1, ['',()])),
        (Validate.element_lengths, InputLengthError, (3, ['abc',[0,1,2,3]])),
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
    e = pytest.raises(InputLengthError, Validate.length, *arguments)
    assert e.value.message == message

@pytest.mark.parametrize("arguments, message", (
        ((list, 'foo'), "Input of unexpected type. Expected:<type 'list'>. Found:<type 'str'>."),
        ((list, 'foo', 'FooBar'), 
         "FooBar of unexpected type. Expected:<type 'list'>. Found:<type 'str'>."),
        ))
def test_type_error_includes_expected_message(arguments, message):
    " confirm InputTypeError contains information helpful to the caller "
    e = pytest.raises(InputTypeError, Validate.type, *arguments)
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
    e = pytest.raises(InputTypeError, Validate.element_types, *arguments)
    assert e.value.message == message

@pytest.mark.parametrize("validator, args", [
        (Validate.type, (str, 'foo')),
        (Validate.type, (list, [])),
        (Validate.type, (tuple, ())),
        (Validate.type, (str, 'foo', 'Named input')),
        (Validate.length, (0, '')),
        (Validate.length, (0, [])),
        (Validate.length, (0, ())),
        (Validate.length, (1, 'A')),
        (Validate.length, (2, [1, 2])),
        (Validate.length, (3, (1, 2, 3))),
        (Validate.length, (0, '', 'Named input')),
        (Validate.element_types, (str, 'foo')),
        (Validate.element_types, (list, ([],[1]))),
        (Validate.element_types, (tuple, [('a',)])),
        (Validate.element_types, (str, ['foo',''], 'Named input')),
        (Validate.element_lengths, (1, ['a',])),
        (Validate.element_lengths, (2, ('ab', [1,2]))),
        (Validate.element_lengths, (1, (('a'),[1]))),
        (Validate.element_lengths, (0, ['',()])),
        (Validate.element_lengths, (3, ['abc',[0,1,2]])),
        ])
def test_validator_passes_silently_on_good_input(validator, args):
    " confirm validator returns nothing when given valid input "
    assert None == validator(*args)
