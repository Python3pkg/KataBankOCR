"generator that yields Accounts and the functions that support it"

from itertools import product

from toolz import pipe, curry, partition_all
from toolz.curried import map as cmap

from parse import settings
from parse.validators import Validate

_superpositions_per_entry = settings.figures_per_entry
_maximum_possible_errors_in_an_entry = settings.strokes_per_figure * settings.figures_per_entry

def accounts_from_superpositions(superpositions):
    "generator that consumes Superpositions and yields Accounts"
    for superpositions_of_entry in partition_all(_superpositions_per_entry, superpositions):
        for superposition in superpositions_of_entry:
            Validate.type(dict, superposition, 'Superposition')
        yield _account(superpositions_of_entry)

def _account(superpositions):
    "return a single [in]valid Account"
    valid_accounts = _valid_accounts(superpositions)
    if len(valid_accounts) == 1:
        return valid_accounts.pop()
    return _invalid_or_illegible_account(superpositions)

def _invalid_or_illegible_account(superpositions):
    "return the invalid or illegible Account represented by Superpositions"
    return pipe(superpositions, cmap(_numeral), ''.join)

def _numeral(superposition):
    "return Numeral represented by Superposition"
    try:
        error_count = 0
        numerals = superposition[error_count]
        numeral = numerals.pop()
        return numeral
    except KeyError:
        return settings.illegible_numeral

def _valid_accounts(superpositions):
    "return valid Accounts with fewest errors (omitted/added strokes)"
    for error_count in range(_maximum_possible_errors_in_an_entry):
        accounts = _valid_accounts_by_error_count(superpositions, error_count)
        if accounts:
            return accounts

def _valid_accounts_by_error_count(superpositions, error_count):
    "return valid Accounts containing exactly error_count errors"
    valid_accounts = set()
    for distribution in _error_distributions(superpositions, error_count):
        numeral_sets = _numeral_sets_by_error_distribution(superpositions, distribution)
        accounts = list(map(''.join, product(*numeral_sets)))
        valid_accounts |= set(filter(settings.checksum, accounts))
    return valid_accounts

def _error_distributions(superpositions, total_errors):
    "return lists of error_counts each list with exactly total_errors"
    ECs_by_sup = curry(_error_counts_by_superposition, total_errors)
    error_distributions = product(*list(map(ECs_by_sup, superpositions)))
    return [dist for dist in error_distributions if sum(dist) == total_errors]

def _error_counts_by_superposition(max_error_count, superposition):
    "return list of error counts <= max_error_count"
    return [error_count for error_count in list(superposition.keys()) if error_count <= max_error_count]

def _numeral_sets_by_error_distribution(superpositions, distribution):
    "return sets of numerals with error counts matching distribution"
    return [sup[err_count] for sup, err_count in zip(superpositions, distribution)]
