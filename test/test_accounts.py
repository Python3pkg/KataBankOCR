"test the accounts module"

import pytest
import random

import settings
from parser.accounts import accounts_from_numerals

from common_tools import flatten, replace_element

class TestAccountsFromNumerals:
    "exercise the accounts_from_numerals function"

    class TestInput:
        "confirm invalid input raises appropriate error"

        def test_with_non_iterable(self, non_iterable):
            "confirm error raised on non-iterable input"
            accounts = accounts_from_numerals(non_iterable)
            pytest.raises(TypeError, list, accounts)

        def test_with_non_string(self, non_string):
            "confirm error raised on iterable that yields a non_string"
            numerals = [non_string]
            accounts = accounts_from_numerals(numerals)
            pytest.raises(TypeError, list, accounts)

        def test_with_numeral_of_invalid_length(self, get_numeral):
            "confirm error raised for Numeral of invalid length"
            doublewide_numeral = get_numeral() + get_numeral()
            accounts = accounts_from_numerals([doublewide_numeral])
            pytest.raises(ValueError, list, accounts)

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
