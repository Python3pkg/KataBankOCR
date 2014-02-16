"test the accounts_from_superpositions generator"

import pytest
import random

from parse.generators.accounts_from_superpositions import accounts_from_superpositions

import check_generator
import fixtures
from common_tools import flatten, replace_element

test_iterability = check_generator.raises_on_non_iterable(generator=accounts_from_superpositions)
test_element_type = \
    check_generator.raises_on_bad_element_type(generator=accounts_from_superpositions,
                                               value_or_type=dict)

def test_parses_known_superpositions_to_expected_accounts():
    "confirm known superpositions yield expected accounts"
    accounts = fixtures.Accounts.of_example_accounts()
    for index, account in enumerate(accounts):
        expected = [account]
        superpositions = fixtures.Superpositions.of_example_accounts()[index]
        found = list(accounts_from_superpositions(superpositions))
        assert expected == found

@pytest.mark.parametrize('expected_account, superpositions', (
        zip(fixtures.Accounts.of_flawed_accounts(), fixtures.Superpositions.of_flawed_accounts())
        ))
def test_parses_superpositions_with_errors_to_expected_accounts(expected_account, superpositions):
    "confirm superpositions with flawed figures yield expected accounts"
    found_accounts = list(accounts_from_superpositions(superpositions))
    assert [expected_account] == found_accounts
