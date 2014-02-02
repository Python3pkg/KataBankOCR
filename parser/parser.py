#!/usr/bin/env python

import fileinput
import settings

from errors import InputError
from entry import Entry

class Parser():
    " Parses file at path into Accounts. If no path, uses StdIn. "

    def __init__(self,path=None):
        " parse file or std-in into Accounts "
        lines = self._get_lines(path)
        self._validate_line_count(len(lines))
        self.accounts = self._lines_from_accounts(lines)

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

    def _lines_from_accounts(self, lines):
        " parse lines into entries and return their accounts "
        entry_start_indexes = range(0, len(lines), settings.lines_per_entry)
        entry = lambda index: lines[index:index + settings.lines_per_entry]
        get_account = lambda index:Entry(entry(index)).account
        return map(get_account, entry_start_indexes)

def main():
    print Parser().accounts

if __name__ == "__main__":
    main()

    
