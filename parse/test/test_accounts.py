"test the accounts module"

import pytest
import random

from parse import settings
from parse.accounts import accounts_from_numerals

from common_tools import flatten, replace_element
from test_input import GeneratorRaises

class TestAccountsFromNumerals:
    "exercise the accounts_from_numerals function"

    class TestInput:
        "confirm invalid input raises appropriate error"

        test_non_iterable = GeneratorRaises.on_non_iterable(accounts_from_numerals)
        test_non_string = GeneratorRaises.on_non_string(accounts_from_numerals)
        valid_numeral = random.choice(list(settings.valid_numerals))
        test_numeral_if_invalid_length = GeneratorRaises.on_element_of_unexpected_length(
            accounts_from_numerals, valid_numeral)

        def test_with_non_numeral(self, get_account, non_numeral):
            "confirm error raised for non_numeral"
            adulterated_account = replace_element(get_account(), non_numeral)
            accounts = accounts_from_numerals(adulterated_account)
            e = pytest.raises(TypeError, list, accounts)
            message = 'Numeral "%s" contains unexpected element "%s" at index 0'
            message = message % (non_numeral, non_numeral)
            assert message == e.value.message

    class TestOutput:
        "confirm valid input results in valid output"

        def test_parses_known_numerals_to_accounts(self, get_accounts):
            "confirm known numerals recognized correctly"
            accounts = get_accounts()
            expected = list(accounts)
            numerals = flatten(accounts)
            found = list(accounts_from_numerals(numerals))
            assert expected == found
