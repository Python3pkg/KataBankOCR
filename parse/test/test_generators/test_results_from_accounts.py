"test the results_from_accounts generator"

from parse.generators.results_from_accounts import results_from_accounts

import check_generator
import fixtures

test_iterability = check_generator.raises_on_non_iterable(generator=results_from_accounts)

test_element_type = \
    check_generator.raises_on_bad_element_type(generator=results_from_accounts,
                                               value_or_type=basestring)

test_element_length = \
    check_generator.raises_on_bad_element_length(generator=results_from_accounts,
                                                 valid_element=fixtures.Accounts.get_random())

test_element_composition = check_generator.raises_on_bad_element_composition(
    generator=results_from_accounts,
    valid_element=fixtures.Accounts.get_random(),
    adulterants=fixtures.ArbitraryValues.invalid_numerals()
    )

def test_parses_known_accounts_to_results():
    "confirm known account recognized correctly"
    expected_results = fixtures.Results.of_example_accounts()
    iterator = results_from_accounts(fixtures.Accounts.of_example_accounts())
    found_results = list(iterator)
    assert expected_results == found_results

def test_parses_account_with_errors_to_expected_result():
    "confirm superpositions with flawed figures yield expected accounts"
    expected_results = fixtures.Results.of_flawed_accounts()
    iterator = results_from_accounts(fixtures.Accounts.of_flawed_accounts())
    found_results = list(iterator)
    assert expected_results == found_results

