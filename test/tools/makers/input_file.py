#!/usr/bin/env python

import os
import operator
import random

import settings

from tools.makers.entry_lines import MakeEntryLines
from tools.translators import account_number_to_lines


class MakeInputFile:
    " methods that each returns an input file "

    @classmethod
    def _lines(cls,account_number_count):
        " return lines representing random account numbers "
        assert isinstance(account_number_count,int)
        assert 0 < account_number_count < 1000
        a_files_worth_of_lines = []
        for account_number_index in range(account_number_count):
            for line in MakeEntryLines.valid():
                a_files_worth_of_lines.append(line)
        return a_files_worth_of_lines

    @classmethod
    def _write(cls,path,lines):
        " write lines to path "
        F = path.open('w')
        for line in lines:
            F.write(line+'\n')
        F.close()

    @classmethod
    def valid(cls,path,account_number_count=500):
        " write entry lines representing random account numbers to path "
        cls._write(path,cls._lines(account_number_count))

    @classmethod
    def _altered(cls,func,victim_line_index=None):
        " make a valid tuple of lines, func a [random] line, return tuple "
        victim_list = list(cls.valid())
        if victim_line_index is None:
            victim_line_index = random.choice(range(len(victim_list)))
        altered_line = func(victim_list[victim_line_index])
        victim_list[victim_line_index] = altered_line
        return tuple(victim_list)


