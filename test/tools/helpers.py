" Functions used to prepare pytest fixtures "

import pytest
import random

def invalid_lengths(valid_length, multiplier=4):
    " the list of ints 0 to (valid_length * multiplier) excluding valid_length "
    maximum_length_to_test = valid_length * multiplier
    lengths = range(maximum_length_to_test + 1)
    return [L for L in lengths if L != valid_length]

def fit_string_to_length(string, length):
    " return duplicated & abbreviated string such that len(string) == length "
    if len(string) == length:
        return string
    elif len(string) > length:
        return string[:length]
    # Still too short. Double it and recurse.
    return fit_string_to_length(string+string, length)

