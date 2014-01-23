#!/usr/bin/env python

from input_lines import MakeInputLines

class MakeInputFile:
    " methods to create an input file and return its path "

    @classmethod
    def write(cls,tmpdir,lines):
        " write lines to temp file and return path "
        path = tmpdir.join('input_file.txt')
        F = path.open('w')
        for line in lines:
            F.write(line+'\n')
        F.close()
        return path

    @classmethod
    def from_account_strings(cls,tmpdir,account_strings):
        " generate lines from account strings, write them to file, return path "
        lines = MakeInputLines.from_account_strings(account_strings)
        return cls.write(tmpdir,lines)

    @classmethod
    def random(cls,tmpdir):
        " generate random valid lines, write them to file, and return path "
        lines = MakeInputLines.random()
        return cls.write(tmpdir,lines)

