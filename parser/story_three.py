#!/usr/bin/env python

import settings
from parser import Parser
from figure import Figure
from entry import Entry
from file import File


def main():
    " Parse input from standard in to a list of Accounts " 

    numeral_from_figure = Parser(Figure.validate_input, None, None, Figure.numeral_from_figure)
    result_from_entry = Parser(Entry.validate_input, Entry.figures_from_entry, 
                               numeral_from_figure, Entry.result_from_numerals)
    results_from_lines = Parser(File.validate_iterator, File.entries_from_lines, 
                                result_from_entry, None)

    lines = File.lines_from_path()
    results = results_from_lines(lines)
    print results

if __name__ == "__main__":
    main()
