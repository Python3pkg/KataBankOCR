"test the accounts module"

import pytest
import random

from parse import settings
from parse.accounts import accounts_from_numerals

from common_tools import flatten
import check_function
 
function = accounts_from_numerals
valid_numeral = random.choice(list(settings.valid_numerals))
adulterants = ['\t', '-', 'I', 'l', '/', '\\', '\r']

test_iterability = check_function.raises_on_non_iterable(function)
test_element_type = check_function.raises_on_bad_element_type(function, valid_numeral)
test_element_length = check_function.raises_on_bad_element_length(function, valid_numeral)
test_element_composition = check_function.raises_on_bad_element_composition(function, 
                                                                            valid_numeral,
                                                                            adulterants)

def test_parses_known_numerals_to_accounts(get_accounts):
    "confirm known numerals recognized correctly"
    accounts = get_accounts()
    expected = list(accounts)
    numerals = flatten(accounts)
    found = list(accounts_from_numerals(numerals))
    assert expected == found
