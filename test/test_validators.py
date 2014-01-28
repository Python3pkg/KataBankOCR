" test validators "
import pytest

from parser.errors import InputTypeError
from parser.errors import InputLengthError
from parser.validators import validate_input_length
from parser.validators import validate_input_type

@pytest.mark.parametrize("validator, args", [
        (validate_input_length, ('', 0)),
        (validate_input_length, ([], 0)),
        (validate_input_length, ((), 0)),
        (validate_input_length, ('A', 1)),
        (validate_input_length, ([1, 2], 2)),
        (validate_input_length, ((1, 2, 3), 3)),
        (validate_input_length, ('', 0, 'Named input')),
        (validate_input_type, ('foo', str)),
        (validate_input_type, ([], list)),
        (validate_input_type, ((), tuple)),
        (validate_input_type, ('foo', str, 'Named input')),
        ])
def test_validator_passes_silently_on_good_input(validator, args):
    " confirm validator returns nothing when given valid input "
    assert None == validator(*args)

@pytest.mark.parametrize("validator, error, args", [
        (validate_input_length, InputLengthError, ('', 1)),
        (validate_input_type, InputTypeError, ('', list)),
        ])
def test_validator_raises_appropriate_error_type(validator, error, args):
    " confirm each validator raises the appropriate error "
    assert pytest.raises(error, validator, *args)

@pytest.mark.parametrize("validator, error, args, message", [
        (validate_input_length, InputLengthError, ('A', 2), 
         "Input of unexpected length. expected:2. found:1."),
        (validate_input_length, InputLengthError, ([], 1, 'Given name'),
         "Given name of unexpected length. expected:1. found:0."),
        (validate_input_type, InputTypeError, ('foo', list), 
         "Input of unexpected type. expected:<type 'list'>. found:<type 'str'>."),
        (validate_input_type, InputTypeError, ('foo', list, 'Provided value'),
         "Provided value of unexpected type. " +
         "expected:<type 'list'>. found:<type 'str'>."),
        ])
def test_raised_errors_include_helpful_message(validator, error, args, message):
    " confirm a raised error contains information helpful to the caller "
    e = pytest.raises(error, validator, *args)
    assert e.value.message == message

