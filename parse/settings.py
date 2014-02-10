" Static values that restate kata.txt "

# All Input Files consist of _approximately_ the same number of Entries
approximate_entries_per_file = 500
# An Entry consists of a defined number of Lines
lines_per_entry = 4
# An Entry represents an Account composed of Numerals
# The four Lines in this example Entry represent the Account '123456789'
# an_example_entry = ['    _  _     _  _  _  _  _ ',
#                     '  | _| _||_||_ |_   ||_||_|',
#                     '  ||_  _|  | _||_|  ||_| _|',
#                     '                           ',]
# All Entries contain the same number of Figures
figures_per_entry = 9
# A Figure consist of Strokes that represents a Numeral
# A Figure results from the joining of vertically adjacent Substrings within an Entry
# All Substrings have a known length
strokes_per_substring = 3
# All Lines have a known length
strokes_per_line = strokes_per_substring * figures_per_entry
# All Figures have a known length
strokes_per_figure = strokes_per_substring * lines_per_entry
# Every Figure is composed only of valid Strokes
valid_strokes = set('_ |')
# The Figure in this example represents the Numeral '5'
# an_example_figure =\
#    ' _ '+\
#    '|_ '+\
#    ' _|'+\
#    '   '
# Every Numeral consists of a single digit string
valid_numerals = set('0123456789')
# Every Figure uniquely represents a unique Numeral
figures = {' _ ' +
           '| |' +
           '|_|' +
           '   ': '0',
           '   ' +
           '  |' +
           '  |' +
           '   ': '1',
           ' _ ' +
           ' _|' +
           '|_ ' +
           '   ': '2',
           ' _ ' +
           ' _|' +
           ' _|' +
           '   ': '3',
           '   ' +
           '|_|' +
           '  |' +
           '   ': '4',
           ' _ ' +
           '|_ ' +
           ' _|' +
           '   ': '5',
           ' _ ' +
           '|_ ' +
           '|_|' +
           '   ': '6',
           ' _ ' +
           '  |' +
           '  |' +
           '   ': '7',
           ' _ ' +
           '|_|' +
           '|_|' +
           '   ': '8',
           ' _ ' +
           '|_|' +
           ' _|' +
           '   ': '9'}
# All other Figures yield the illegible Numeral
illegible_numeral = '?'

# The Checksum function differentiates between a 'valid' and an 'invalid' Account
# The Checksum function divides by a constant
checksum_divisor = 11
# The Checksum function takes an Account and returns True or False
def checksum(account):
    """ return True for a valid Acount and False for an invalid Account
    account number:  3  4  5  8  8  2  8  6  5
    position names:  d9 d8 d7 d6 d5 d4 d3 d2 d1
    checksum calculation: (d1+2*d2+3*d3 +..+9*d9) mod 11 = 0 """
    values = [int(numeral) * (9 - index) for index, numeral in enumerate(account)]
    return sum(values).__mod__(checksum_divisor) == 0
# The Checksum will return True for each of these Accounts
some_known_valid_accounts = ('123456789', '490867715', '899999999',
                             '000000051', '686666666', '559555555')
# The Checksum will return False for each of these Accounts
some_known_invalid_accounts = ('490067715', '888888888', '555555555',
                               '333333333', '111111111', '777777777')

# A Result includes an Account and, if appropriate, a Status
# The Result for an Entry with an illegible Figure will include the Illegible Status
illegible_status = ' ILL'
# The Result for an Entry representing with an invalid Account will include the Invalid Status
invalid_status = ' ERR'
