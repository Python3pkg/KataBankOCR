import settings
from validators import Validate

def account_from_superpositions(superpositions):
    "return accounts string represented by superpositions"
    numerals = []
    for superposition in superpositions:
        Validate.type(dict, superposition, 'Superposition')
        numeral_set = superposition.setdefault(0, set())
        if numeral_set == set():
            numeral = settings.illegible_numeral
        else:
            numeral = numeral_set.pop()
        numerals.append(numeral)
    return ''.join(numerals)
