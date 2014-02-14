"test the accounts_from_superpositions generator"
import pytest

from parse.generators.accounts_from_superpositions import accounts_from_superpositions

import check_generator
import fixtures

test_iterability = check_generator.raises_on_non_iterable(generator=accounts_from_superpositions)
test_element_type = \
    check_generator.raises_on_bad_element_type(generator=accounts_from_superpositions,
                                               value_or_type=dict)

@pytest.mark.parametrize('accountset, superpositions', 
                         zip(fixtures.AccountSets.from_example_accounts(),
                             fixtures.Superpositions.from_example_accounts()))
def test_parses_known_superpositions_to_expected_accounts(accountset, superpositions):
    "confirm known superpositions yield expected accounts"
    expected_accounts = accountset
    found_accounts = tuple(accounts_from_superpositions(superpositions))
    assert expected_accounts == found_accounts

def test_parses_known_superpositions_to_expected_accounts():
    "confirm known superpositions yield expected accounts"
    for index, superpositions in enumerate(fixtures.Superpositions.from_example_accounts()):
        expected = [fixtures.AccountSets.from_example_accounts()[index]]
        found = list(accounts_from_superpositions(superpositions))
        assert expected == found

