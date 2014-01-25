#!/usr/bin/env python

import random

import settings

from tools.translators import account_string_to_lines

from tools.makers.account_string import MakeAccountString
from tools.makers.figure_character import MakeFigureCharacter

class MakeEntryLines:
    "  methods that each return a list of lines representing an account string "

    @classmethod
    def random(cls):
        " return a list of lines representing a random account string "
        account_string = MakeAccountString.random()
        return account_string_to_lines(account_string)

    @classmethod
    def from_account_string(cls, account_string):
        " return a list of lines representing the provided account string "
        return account_string_to_lines(account_string)

    @classmethod
    def _altered(cls,func, victim_line_index):
        " make a valid list of lines, func a [random] line, return list "
        victim_list = list(cls.random())
        if victim_line_index is None:
            victim_line_index = random.choice(range(len(victim_list)))
        victim_list[victim_line_index] = func(victim_list[victim_line_index])
        return victim_list

    @classmethod
    def non_empty_last_line(cls):
        " return (an otherwise valid) list containing a non-empty last line "
        def adulterate_line(line):
            if len(line.strip()) == 0:
                new_char = MakeFigureCharacter.non_blank_valid()
                char_index = random.choice(range(len(line)))
                line = line[:char_index] + new_char + line[char_index+1:]
            return line
        return cls._altered(adulterate_line, settings.lines_per_entry - 1)

