#!/usr/bin/env python

" Test the validators module "

import pytest

from parser.errors import InputTypeError as TypErr
from parser.errors import InputLengthError as LenErr
from parser.validators import validate_input_length as val_len
from parser.validators import validate_input_type as val_typ

@pytest.mark.parametrize("validator, args", [
        (val_len, ('', 0)),
        (val_len, ([], 0)),
        (val_len, ((), 0)),
        (val_len, ('A', 1)),
        (val_len, ([1,2], 2)),
        (val_len, ((1,2,3), 3)),
        (val_len, ('', 0, 'Named input')),
        (val_typ, ('foo', str)),
        (val_typ, ([], list)),
        (val_typ, ((), tuple)),
        (val_typ, ('foo', str, 'Named input')),
        ])
def test_validator_passes_silently_on_good_input(validator, args):
    " confirm validator successfully returns nothing when given valid input "
    assert None == validator(*args)

@pytest.mark.parametrize("validator, error, args", [
        (val_len, LenErr, ('', 1)),
        (val_typ, TypErr, ('', list)),
        ])
def test_validators_raise_appropriate_error_type(validator, error, args):
    " confirm each validator raises the appropriate error "
    assert pytest.raises(error, validator, *args)

@pytest.mark.parametrize("validator, error, args, message", [
        (val_len, LenErr, ('A', 2), 
         "Input of unexpected length. expected:2. found:1."),
        (val_len, LenErr, ([], 1, 'Given name'),
         "Given name of unexpected length. expected:1. found:0."),
        (val_typ, TypErr, ('foo', list), 
         "Input of unexpected type. expected:<type 'list'>. found:<type 'str'>."),
        (val_typ, TypErr, ('foo', list, 'Provided value'),
         "Provided value of unexpected type. " +
         "expected:<type 'list'>. found:<type 'str'>."),
        ])
def test_raised_errors_include_helpful_message(validator, error, args, message):
    " confirm a raised error contains information helpful to the caller "
    e = pytest.raises(error, validator, *args)
    assert e.value.message == message

