"test the accounts_from_superpositions generator"

import pytest

from parse.generators.accounts_from_superpositions import accounts_from_superpositions

import check_generator
import fixtures

test_iterability = check_generator.raises_on_non_iterable(generator=accounts_from_superpositions)
test_element_type = \
    check_generator.raises_on_bad_element_type(generator=accounts_from_superpositions,
                                               value_or_type=dict)

accounts = (
    fixtures.Accounts.of_example_accounts()
    + fixtures.Accounts.of_flawed_accounts()
    )
superpositions = (
    fixtures.Superpositions.of_example_accounts()
    + fixtures.Superpositions.of_flawed_accounts()
    )

@pytest.mark.parametrize('expected_account, superpositions', (zip(accounts, superpositions)))
def test_parses_superpositions_to_expected_accounts(expected_account, superpositions):
    "confirm known superpositions yield expected accounts"
    found_accounts = list(accounts_from_superpositions(superpositions))
