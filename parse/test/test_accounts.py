"test the accounts_from_superpositions generator"
import pytest

from parse.accounts import accounts_from_superpositions as generator

import check_generator
from fixtures import AccountSets, Superpositions

test_iterability = check_generator.raises_on_non_iterable(generator)
test_element_type = check_generator.raises_on_bad_element_type(generator, dict())

@pytest.mark.parametrize('accountset, superpositions', zip(AccountSets.from_example_accounts(),
                                                           Superpositions.from_example_accounts()))
def test_parses_known_superpositions_to_expected_accounts(accountset, superpositions):
    "confirm known superpositions yield expected accounts"
    expected_accounts = accountset
    found_accounts = tuple(generator(superpositions))
    assert expected_accounts == found_accounts

def test_parses_known_superpositions_to_expected_accounts():
    "confirm known superpositions yield expected accounts"
    for index, superpositions in enumerate(Superpositions.from_example_accounts()):
        expected = [AccountSets.from_example_accounts()[index]]
        found = list(generator(superpositions))
        assert expected == found

