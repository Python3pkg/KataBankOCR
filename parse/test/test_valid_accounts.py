"test the valid_accounts module"

import pytest
import random

from parse import settings
from parse.valid_accounts import valid_accounts_from_superpositions

import check_function
from test_superpositions import figure_superpositions
 
function = valid_accounts_from_superpositions

test_iterability = check_function.raises_on_non_iterable(function)
test_element_type = check_function.raises_on_bad_element_type(function, dict())

@pytest.mark.parametrize('account, expected_valid_accounts', (
        ('123456789', {'123456789'}),
        ('111111111', {'711111111'}),
        ('777777777', {'777777177'}),
        ('200000000', {'200800000'}),
        ('333333333', {'333393333'}),
        ('555555555', {'555655555', '559555555'}),
        ('666666666', {'666566666', '686666666'}),
        ('888888888', {'888886888', '888888880', '888888988'}),
        ('999999999', {'899999999', '993999999', '999959999'}),
        ('490067715', {'490067115', '490067719', '490867715'}),
        ))
def test_parses_known_accounts_to_expected_valid_accounts(account, expected_valid_accounts):
    "confirm known accounts yield expected valid account lists"
    superpositions = _superpositions_from_account(account)
    found_accounts = valid_accounts_from_superpositions(superpositions)
    assert expected_valid_accounts == found_accounts

def _superpositions_from_account(account):
    "return Superpositions from Figures in Account's Numerals"
    return map(_superposition_from_numeral, account)

def _superposition_from_numeral(numeral):
    "return Superposition from Figure representing Numeral"
    for fig, num in settings.figures.items():
        if numeral == num:
            return figure_superpositions[fig]

superposition_a = figure_superpositions['   ' +
                                        ' _|' +
                                        '  |' +
                                        '   ']
superposition_b = figure_superpositions['   ' +
                                        '| |' +
                                        '|_|' +
                                        '   ']
superposition_c = figure_superpositions[' _ ' +
                                        ' _ ' +
                                        ' _|' +
                                        '   ']
superpositions_a = [superposition_a] + _superpositions_from_account('23456789')
superpositions_b = (_superpositions_from_account('0')
                    + [superposition_b]
                    + _superpositions_from_account('0000051'))
superpositions_c = _superpositions_from_account('49086771') + [superposition_c]

@pytest.mark.parametrize('superpositions, expected_valid_accounts', (
        (superposition_a, {'123456789'}),
        (superposition_a, {'000000051'}),
        (superposition_c, {'490867715'}),
        ))
def test_parses_known_superpositions_to_expected_valid_accounts(superpositions, 
                                                                expected_valid_accounts):
    "confirm known superpositions yield expected valid accounts"
    found_accounts = valid_accounts_from_superpositions(superpositions)
    assert expected_valid_accounts == found_accounts
