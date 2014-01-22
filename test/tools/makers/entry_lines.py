#!/usr/bin/env python

import random

import settings

from tools.translators import account_string_to_lines

from tools.makers.account_string import MakeAccountString
from tools.makers.figure_character import MakeFigureCharacter

class MakeEntryLines:
    "  methods that return a tuple of lines representing an account string "

    @classmethod
    def valid(cls):
        " return a tuple of lines representing a random account string "
        account_string = MakeAccountString.random()
        return account_string_to_lines(account_string)

    @classmethod
    def from_account_string(cls, account_string):
        " return a tuple of lines representing the provided account string "
        account_string = MakeAccountString.random()
        return account_string_to_lines(account_string)

    @classmethod
    def _altered(cls,func,victim_line_index=None):
        " make a valid tuple of lines, func a [random] line, return tuple "
        victim_list = list(cls.valid())
        if victim_line_index is None:
            victim_line_index = random.choice(range(len(victim_list)))
        victim_list[victim_line_index] = func(victim_list[victim_line_index])
        return tuple(victim_list)

    @classmethod
    def containing_non_string(cls):
        " return (an otherwise valid) tuple containing one non-string "
        arbitrary_non_string_values = (0,1,-10,False,True,3.14,(),[],{},set())
        non_string_value = random.choice(arbitrary_non_string_values)
        return cls._altered(lambda L:non_string_value)

    @classmethod
    def abbreviated_string(cls):
        " return (an otherwise valid) tuple containing one abbreviated string "
        line_length = settings.figures_per_entry * settings.figure_width
        new_line_length = random.choice(range(line_length))
        return cls._altered(lambda L:L[new_line_length])

    @classmethod
    def extended_string(cls):
        " return (an otherwise valid) tuple containing one extended string "
        def extend_line(line):
            additional_length = random.choice(range(len(line))) + 1
            additional_text = line[:additional_length]
            return line + additional_text
        return cls._altered(extend_line)

    @classmethod
    def non_empty_last_line(cls):
        " return (an otherwise valid) tuple containing a non-empty last line "
        def adulterate_line(line):
            if len(line.strip()) == 0:
                new_char = MakeFigureCharacter.non_blank_valid()
                char_index = random.choice(range(len(line)))
                line = line[:char_index] + new_char + line[char_index+1:]
            return line
        return cls._altered(adulterate_line, settings.lines_per_entry - 1)

