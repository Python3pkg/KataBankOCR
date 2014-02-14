"test the accounts_from_superpositions generator"

from parse.generators.accounts_from_superpositions import accounts_from_superpositions

import check_generator
import fixtures

test_iterability = check_generator.raises_on_non_iterable(generator=accounts_from_superpositions)
test_element_type = \
    check_generator.raises_on_bad_element_type(generator=accounts_from_superpositions,
                                               value_or_type=dict)

def test_parses_known_superpositions_to_expected_accounts():
    "confirm known superpositions yield expected accounts"
    expected_account_sets = fixtures.AccountSets.from_example_accounts()
    superpositions = fixtures.Superpositions.from_example_accounts()
    found_account_sets = tuple(accounts_from_superpositions(superpositions))
    assert expected_accounts == found_account_sets

def test_parses_known_superpositions_to_expected_accounts():
    "confirm known superpositions yield expected accounts"
    for index, superpositions in enumerate(fixtures.Superpositions.from_example_accounts()):
        expected = [fixtures.AccountSets.from_example_accounts()[index]]
        found = list(accounts_from_superpositions(superpositions))
        assert expected == found

