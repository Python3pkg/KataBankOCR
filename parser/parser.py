#!/usr/bin/env python

" The Parser module "

import settings

from entry import Entry

class ParserError(Exception):
    " Base class for exceptions in this module "
    pass

class InputError(ParserError):
    " Exception raised for errors in the input "
    def __init__(self,msg):
        self.message = msg

class Parser():
    " Parses file at path into account strings "

    def __init__(self,path):
        self.path = path
        self.account_strings = []
        self.parse_file()

    def parse_file(self):
        " read file of entries and identify its account strings "
        lpe = settings.lines_per_entry
        with open(str(self.path)) as input_file:
            entry_lines = [input_file.readline()[:-1] for i in range(lpe)]
            entry = Entry(tuple(entry_lines))
            self.account_strings.append(entry.account_string)

