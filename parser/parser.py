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
        self.account_strings = []

class Parser():
    " Parses file at path into account strings "

    def __init__(self,path):
        self.path = path
#        self.parse_file()

    def parse_file(self):
        " read file of entries and identify its account strings "
        lpe = settings.lines_per_entry
        with open(str(self.path)) as input_file:
            entry = Entry(tuple(input_file.read() for i in range(lpe)))
            self.account_strings.append(entry.account_string)



