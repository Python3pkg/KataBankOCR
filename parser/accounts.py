" generator that yields Accounts and the functions that support it "

import settings
from validators import Validate

def accounts_from_numerals(numerals):
    " generator that consumes Numerals and yields Accounts "
    account = []
    for numeral in numerals:
        _validate_numeral(numeral)
        account.append(numeral)
        if len(account) == settings.figures_per_entry:
            account = ''.join(account)
            yield account
            account = []

def _validate_numeral(numeral):
    " confirm numeral type, length, and composition or raise ValueError "
    Validate.type(basestring, numeral, 'Numeral')
    Validate.length(1, numeral, 'Numeral')
    expected_numerals = settings.valid_numerals | set(settings.illegible_numeral)
    Validate.composition(expected_numerals, numeral, 'Numeral')


