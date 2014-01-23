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
            a_files_worth_of_lines.extend(MakeEntryLines.valid())
        return a_files_worth_of_lines

    @classmethod
    def from_account_strings(cls, account_strings):
        " return lines representing the provided account_strings "
        a_files_worth_of_lines = []
        for account_string in account_strings:
            entry_lines = MakeEntryLines.from_account_string(account_string)
            a_files_worth_of_lines.extend(entry_lines)
        return a_files_worth_of_lines


