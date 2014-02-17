"functions used by multiple test modules"

import random

def invalid_lengths(valid_length, multiplier=4):
    "return ints 0 to (valid_length * multiplier) excluding valid_length"
    maximum_length_to_test = valid_length * multiplier
    lengths = range(maximum_length_to_test + 1)
    return [L for L in lengths if L != valid_length]

def fit_to_length(value, length):
    "return duplicated & abbreviated value such that len(value) == length"
    if len(value) == length:
        return value
    elif len(value) > length:
        return value[:length]
    # Still too short. Double it and recurse.
    return fit_to_length(value + value, length)

def adulterate_iterable(target, new_element, index=None):
    "return string or list after replacing a [random] element"
    assert isinstance(target, (list, basestring))
    if index is None:
        index = random.randrange(0, len(target))
    if isinstance(target, basestring):
        return ''.join((target[:index], new_element, target[index + 1:]))
    elif isinstance(target, list):
        target[index] = new_element
        return target

def get_one_or_more(function, count=None):
    "return just one or a list of function's return values"
    if count is None:
        return function()
    return [function() for _ in range(count)]
