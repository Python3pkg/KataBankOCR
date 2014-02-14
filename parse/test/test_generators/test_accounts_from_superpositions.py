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
    accounts = fixtures.Accounts.of_example_accounts()
    for index, account in enumerate(accounts):
        expected = [account]
        superpositions = fixtures.Superpositions.of_example_accounts()[index]
        found = list(accounts_from_superpositions(superpositions))
        assert expected == found


