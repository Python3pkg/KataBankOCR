#!/usr/bin/env python

" The Parser module "

import fileinput

import settings

from errors import InputError
from entry import Entry

class Parser():
    " Parses file at path into account strings. If no path, uses StdIn. "

    def __init__(self,path=None):
        self.path = path
        self.account_strings = []
        self.get_lines()
        self.validate_lines()
        self.parse_lines()

    def lines_from_stdin(self):
        " read and return all lines from standard input "
        return list(fileinput.input())

    def lines_from_path(self):
        " read and return all lines from file at path "
        with open(str(self.path)) as input_file:
            return list(input_file)

    def get_lines(self):
        " read all lines from either path or standard input "
        if self.path:
            self.lines = self.lines_from_path()
        else:
            self.lines = self.lines_from_stdin()

    def validate_lines(self):
        " parse lines into entries and decipher their account strings "
        if not self.lines: 
            raise(InputError('nothing to parse'))
        elif len(self.lines).__mod__(settings.lines_per_entry) != 0:
            raise(InputError('file ended mid entry'))

    def parse_lines(self):
        " parse lines into entries and decipher their account strings "
        lpe = settings.lines_per_entry
        for line_index in range(0, len(self.lines), lpe):
            entry_lines = self.lines[line_index:line_index + lpe]
            account_string = Entry(entry_lines).account_string
            self.account_strings.append(account_string)

def main():
    print Parser().account_strings

if __name__ == "__main__":
    main()

