#!/usr/bin/env python

import fileinput
import settings

from errors import InputError
from entry import Entry

class Parser():
    " Parses file at path into account strings. If no path, uses StdIn. "

    def __init__(self,path=None):
        " parse file or std-in into account strings "
        lines = self._get_lines(path)
        self._validate_lines(lines)
        self.account_strings = self._lines_from_account_strings(lines)

    def _get_lines(self, path):
        " read all lines from either path or standard input "
        if path:
            with open(str(path)) as input_file:
                return list(input_file)
        return list(fileinput.input())

    def _validate_lines(self, lines):
        " confirm appropriate number of lines read "
        if not lines: 
            raise(InputError('nothing to parse'))
        elif len(lines).__mod__(settings.lines_per_entry) != 0:
            raise(InputError('file ended mid entry'))

    def _lines_from_account_strings(self, lines):
        " parse lines into entries and return their account strings "
        entry_start_indexes = range(0, len(lines), settings.lines_per_entry)
        entry_list = lambda index: lines[index:index + settings.lines_per_entry]
        account_string = lambda index:Entry(entry_list(index)).account_string
        return map(account_string, entry_start_indexes)

def main():
    print Parser().account_strings

if __name__ == "__main__":
    main()

