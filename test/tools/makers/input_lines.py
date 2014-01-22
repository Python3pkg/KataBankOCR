#!/usr/bin/env python

import random

from tools.makers.entry_lines import MakeEntryLines

class MakeInputLines:
    " methods that create an input file worth of lines "

    @classmethod
    def random(cls):
        " return lines representing 500 random account numbers "
        a_files_worth_of_lines = []
        for account_number_index in range(500):
            for line in MakeEntryLines.valid():
                a_files_worth_of_lines.append(line)
        return a_files_worth_of_lines

    @classmethod
    def abbreviated(cls):
        " return one line less than a full file worth of lines "
        return cls.random()[:-1]

