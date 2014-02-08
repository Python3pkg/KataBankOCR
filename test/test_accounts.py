" test the accounts module "

import pytest
import random

import settings
from parser.accounts import accounts_from_numerals
from parser.validators import Validate

from common_tools import flatten

class TestAccountsFromNumerals:
    " exercise the accounts_from_numerals function "

    class TestInput:
        " confirm invalid input raises appropriate error "

        def test_with_non_iterable(self, non_iterable):
            " confirm error raised on non-iterable input "
            accounts = accounts_from_numerals(non_iterable)
            pytest.raises(TypeError, list, accounts)

        def test_with_non_string(self, non_string):
            " confirm error raised on iterable that yields a non_string "
            numerals = [non_string,]
            accounts = accounts_from_numerals(numerals)
            pytest.raises(TypeError, list, accounts)

        def test_with_numeral_of_invalid_length(self, get_numeral):
            " confirm error raised for account of invalid length "
            doublewide_numeral = get_numeral() + get_numeral()
            accounts = accounts_from_numerals([doublewide_numeral,])
            pytest.raises(ValueError, list, accounts)

        some_non_numerals = {'\t', '-', 'I', 'l', '/', '\\', '\r'}
        in_common = some_non_numerals.intersection(settings.valid_numerals)
        assert set() == in_common
        @pytest.mark.parametrize('bad_numerals', some_non_numerals)
        def test_with_non_numeral(self, bad_numerals):
            " confirm error raised for non_numeral "
            accounts = accounts_from_numerals(bad_numerals)
            e = pytest.raises(TypeError, list, accounts)
            message = 'contains unexpected element'
            assert message in e.value.message

    class TestOutput:
        " confirm valid input results in valid output "

        def test_returns_iterable(self, get_numerals):
            " confirm iterable "
            accounts = accounts_from_numerals(get_numerals())
            Validate.iterable(accounts)

        def test_element_types(self, get_numerals):
            " confirm iterable yields strings "
            accounts = accounts_from_numerals(get_numerals())
            Validate.elements('type', basestring, accounts, 'Account')

        def test_element_lengths(self, get_numerals):
            " confirm iterable yields elements of correct length "
            accounts = accounts_from_numerals(get_numerals())
            expected_length = settings.figures_per_entry
            Validate.elements('length', expected_length, accounts, 'Account')

        def test_parses_known_numerals_to_accounts(self, get_accounts):
            " confirm known numerals recognized correctly "
            accounts = get_accounts()
            expected = list(accounts)
            numerals = flatten(accounts)
            found = list(accounts_from_numerals(numerals))
            assert expected == found

