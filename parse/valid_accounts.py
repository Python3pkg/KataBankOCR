"generator that yields lists of valid Accounts"

from itertools import product, chain

import settings
from validators import Validate

def valid_accounts_from_superpositions(superpositions):
    "generator that consumes Superpositions and yields valid Account sets"
    account_worth_of_superpositions = []
    for superposition in superpositions:
        Validate.type(dict, superposition, 'Superposition')
        account_worth_of_superpositions.append(superposition)
        if len(account_worth_of_superpositions) == settings.figures_per_entry:
            accounts = _valid_accounts_from_superpositions(account_worth_of_superpositions)
            yield accounts
            account_worth_of_superpositions = []

def _valid_accounts_from_superpositions(superpositions):
    "returns valid Accounts with fewest differences from their Entries"
    numeral_sets = _initial_numeral_sets(superpositions)
    accounts = _valid_accounts_from_numeral_sets(numeral_sets, superpositions)
    if accounts:
        lowest_difference_count = min(accounts.keys())
        best_accounts = accounts[lowest_difference_count]
        return best_accounts
    allowed_differences_per_numeral = 0
    while allowed_differences_per_numeral <= settings.figures_per_entry:
        for index, superposition in enumerate(superpositions):
            numeral_set = _numerals_within_difference_count(superposition,
                                                            allowed_differences_per_numeral)
            numeral_sets[index].update(numeral_set)
        accounts = _valid_accounts_from_numeral_sets(numeral_sets, superpositions)
        if accounts:
            lowest_difference_count = min(accounts.keys())
            best_accounts = accounts[lowest_difference_count]
            return best_accounts
        allowed_differences_per_numeral += 1

def _initial_numeral_sets(superpositions):
    "return list of least-different numeral_sets"
    numeral_sets = []
    for superposition in superpositions:
        lowest_difference_count = min(superposition.keys())
        numeral_set = superposition[lowest_difference_count]
        numeral_sets.append(numeral_set)
    return numeral_sets

def _valid_accounts_from_numeral_sets(numeral_sets, superpositions):
    "return all possible valid accounts assemblable from numeral sets"
    accounts = map(''.join, product(*numeral_sets))
    valid_accounts = set(filter(settings.checksum, accounts))
    d = {}
    for account in valid_accounts:
        difference_count = _account_differences(account, superpositions)
        d.setdefault(difference_count, set()).add(account)
    return d

def _account_differences(account, superpositions):
    "return a count of the differences in an account"
    differences = 0
    for index, numeral in enumerate(account):
        for dif, num in superpositions[index].items():
            if numeral in num:
                differences += dif
    return differences

def _numerals_within_difference_count(superposition, count):
    "returns set of numerals with <= count of differences from figure"
    numeral_sets = [nums for difs, nums in superposition.items() if difs <= count]
    return chain.from_iterable(numeral_sets)

def _numerals_from_superpositon(superposition):
    "generator that yields 2-tuples of (difference_count, numeral_set)"
    difference_counts = superposition.keys()
    for difference_count in sorted(difference_counts):
        numeral_set = superposition[difference_count]
        return (difference_count, numeral_set)

