"generator that yields lists of valid Accounts"

import settings
from validators import Validate

def valid_accounts_from_superpositions(superpositions):
    "generator that consumes Superpositions and yields Accounts"
    account_worth_of_superpositions = []
    for superposition in superpositions:
        Validate.type(dict, superposition, 'Superposition')
        account_worth_of_superpositions.append(superposition)
        if len(account_worth_of_superpositions) == settings.figures_per_entry:
            accounts = _valid_accounts_from_superpositions(account_worth_of_superpositions)
            yield accounts
            account_worth_of_superpositions = []

def _valid_accounts_from_superpositions(superpositions):
    "returns list of valid Accounts closest to superpositions"
    maximum_differences_per_numeral = 0
    return []


