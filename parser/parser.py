#!/usr/bin/env python
"parse input into output as described by kata.txt and settings.py"

from __future__ import print_function
from functools import partial

from lines import lines_from_path
from entries import entries_from_lines
from figures import figures_from_entries
from numerals import numerals_from_figures
from accounts import accounts_from_numerals
from results import results_from_accounts
from options import in_path_and_out_path
# Awaiting Story 4
#from superpositions import superpositions_from_figures
#from results import results_from_superpositions

def parse(input_path, output_path):
    "return Results from Lines within File at Path"

    lines = lines_from_path(input_path)
    entries = entries_from_lines(lines)
    figures = figures_from_entries(entries)
    numerals = numerals_from_figures(figures)
    accounts = accounts_from_numerals(numerals)
    results = results_from_accounts(accounts)
# Awaiting Story 4
#    superpositions = superpositions_from_figures(figures)
#    results = results_from_superpositions(superpositions)
    output(results, output_path)

def output(results, path):
    "print results to path or (default of) StdOut"
    if path is None:
        for result in results:
            print(result)
    else:
        with open(path, 'w') as out_file:
            for result in results:
                print(result, file=out_file)

if __name__ == '__main__':
    parse(*in_path_and_out_path())

