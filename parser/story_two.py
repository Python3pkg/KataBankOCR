#!/usr/bin/env python

"parse input into output per User Story 2 in kata.txt and settings.py"

import settings
from lines import lines_from_path
from entries import entries_from_lines
from figures import figures_from_entries
from numerals import numerals_from_figures
from accounts import accounts_from_numerals

def parse(path):
    "return valid and invalid Accounts from input file at path"
    lines = lines_from_path(path)
    entries = entries_from_lines(lines)
    figures = figures_from_entries(entries)
    numerals = numerals_from_figures(figures)
    accounts = accounts_from_numerals(numerals)
    accounts = list(accounts)
    valid_accounts = filter(settings.checksum, accounts)
    invalid_accounts = filter(lambda a: not settings.checksum(a), accounts)
    print str(valid_accounts)
    print str(invalid_accounts)

if __name__ == "__main__":
    path = '-'  # TODO: take input and output paths from docopt
    parse(path)
