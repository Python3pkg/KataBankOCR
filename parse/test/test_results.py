"test the results module"

import pytest
import random

from parse import settings
from parse.results import results_from_accounts

import check_function

function = results_from_accounts
a_numeral = lambda _: random.choice(list(settings.valid_numerals))
an_account = ''.join(map(a_numeral, range(settings.figures_per_entry)))
adulterants = ['\t', '-', 'I', 'l', '/', '\\', '\r']

test_iterability = check_function.raises_on_non_iterable(function)
test_element_type = check_function.raises_on_bad_element_type(function, an_account)
test_element_length = check_function.raises_on_bad_element_length(function, an_account)
test_element_composition = check_function.raises_on_bad_element_composition(function, 
                                                                            an_account,
                                                                            adulterants)

@pytest.mark.parametrize('account, result', (
        ('000000000', '000000000',),
        ('111111111', '111111111 ERR'),
        ('222222222', '222222222 ERR'),
        ('333333333', '333333333 ERR'),
        ('444444444', '444444444 ERR'),
        ('555555555', '555555555 ERR'),
        ('666666666', '666666666 ERR'),
        ('777777777', '777777777 ERR'),
        ('888888888', '888888888 ERR'),
        ('999999999', '999999999 ERR'),
        ('123456789', '123456789'),
        ))
def test_parses_known_accounts_to_results(account, result):
    "confirm known accounts recognized correctly"
    expected = [result]
    found = list(results_from_accounts([account]))
    assert expected == found
