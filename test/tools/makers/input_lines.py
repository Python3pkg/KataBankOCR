#!/usr/bin/env python

import random

from tools.makers.entry_lines import MakeEntryLines

class MakeInputLines:
    " methods that create an input file worth of lines "

    @classmethod
    def random(cls,account_number_count=500):
        " return lines representing random account numbers "
        assert isinstance(account_number_count,int)
        assert 0 < account_number_count < 1000
        a_files_worth_of_lines = []
        for account_number_index in range(account_number_count):
            for line in MakeEntryLines.valid():
                a_files_worth_of_lines.append(line)
        return a_files_worth_of_lines

    @classmethod
    def abbreviated(cls):
        " return one line less than a full file worth of lines "
        return cls.random()[:-1]

