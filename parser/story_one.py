#!/usr/bin/env python

from parser import Parser
from figure import Figure
from entry import Entry
from file import File


def main():
    " Parse input from standard in to a list of Accounts " 

    numeral_from_figure = Parser(Figure.validate_input, None, None, Figure.numeral_from_figure)
    account_from_entry = Parser(Entry.validate_input, Entry.figures_from_entry, 
                                numeral_from_figure, Entry.account_from_numerals)
    accounts_from_lines = Parser(File.validate_iterator, File.entries_from_lines, 
                                 account_from_entry, None)

    lines = File.lines_from_path()
    print accounts_from_lines(lines)

if __name__ == "__main__":
    main()
