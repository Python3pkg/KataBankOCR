"test the results module"

import pytest

from parse.results import results_from_accounts as generator

from fixtures import Accounts
import check_generator

account = Accounts.get_random()
adulterants = ['\t', '-', 'I', 'l', '/', '\\', '\r']

test_iterability = check_generator.raises_on_non_iterable(generator)
test_element_type = check_generator.raises_on_bad_element_type(generator, account)
test_element_length = check_generator.raises_on_bad_element_length(generator, account)
test_element_composition = check_generator.raises_on_bad_element_composition(generator, 
                                                                             account,
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
    found = list(generator([account]))
    assert expected == found
