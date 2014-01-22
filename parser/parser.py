#!/usr/bin/env python

" The Parser module "

import settings

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
        self.parse_file()

    def open_file(self):
        " open file at path for reading "
        try:
            return self.path.open('r')
        except:
            raise(InputError('failed to open file at %s'%self.path))

    def lines_to_entries(self,lines):
        " split lines into tuples of entry_lines and return list of entries "
        entries = []
        for line in lines:
            entry_lines = []
            for i in range(settings.lines_per_entry):
                entry_lines.append(line)

        return tuples

    def parse_file(self):
        " read file of entries and identify its account strings "
        F = self.open_file()

        F.close()        

