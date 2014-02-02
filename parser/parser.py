#!/usr/bin/env python

import fileinput
import settings

from errors import InputError
from entry import Entry
from figure import Figure

class Parser():
    " Parses file at path into Accounts. If no path, uses StdIn. "

    def __init__(self,path=None):
        " parse file or std-in into Accounts "
        lines = self._get_lines(path)
        self._validate_line_count(len(lines))
        self.accounts = self._accounts_from_lines(lines)

    def _get_lines(self, path):
        " read all lines from either path or standard input "
        if path:
            with open(str(path)) as input_file:
                return list(input_file)
        return list(fileinput.input())

    def _validate_line_count(self, count):
        " confirm appropriate number of lines read "
        if count == 0: 
            raise(InputError('nothing to parse'))
        elif count.__mod__(settings.lines_per_entry) != 0:
            raise(InputError('file ended mid entry'))

    def _accounts_from_lines(self, lines):
        " parse lines into entries and return their accounts "
        entry_start_indexes = range(0, len(lines), settings.lines_per_entry)
        accounts = []
        for index in entry_start_indexes:
            entry = lines[index:index + settings.lines_per_entry]
            entry = self._trim_line_feeds_from_lines_as_necessary(lines)
            Entry.check(entry)
            figures = Entry.figures_from_entry(entry)
            for figure in figures:
                Figure.check(figure)
            numerals = map(Figure.get_numeral, figures)
            account = Entry.account_from_numerals(numerals)
            accounts.append(account)
        return accounts

    def _trim_line_feeds_from_lines_as_necessary(self, lines):
        return map(self._trim_line_feed_if_necessary, lines)

    def _trim_line_feed_if_necessary(self, line):
        return line[:-1] if self._line_needs_trimmed(line) else line

    def _line_needs_trimmed(self, line):
        line_ends_in_line_feed = line[-1:] == '\n'
        line_one_char_too_long = len(line) == settings.strokes_per_line + 1
        return line_ends_in_line_feed and line_one_char_too_long

def main():
    print Parser().accounts

if __name__ == "__main__":
    main()

